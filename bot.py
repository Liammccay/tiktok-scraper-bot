import os
import json
import asyncio
import discord
from discord.ext import commands
from playwright.async_api import async_playwright

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("TikTok Deep Scraper Bot is ready!")

@bot.command(name="scrape")
async def scrape_tiktok(ctx, username: str, keyword: str):
    if not username.startswith("@"):
        username = f"@{username}"
    
    clean_username = username.replace("@", "")
    cache_file = f"cache_{clean_username}.json"
    
    if not os.path.exists(cache_file):
        await ctx.send(f"❌ No cache found for `{username}`. Run `!update {username}` first to build the database!")
        return

    await ctx.send(f"⚡ **Memory found!** Loading cached posts for `{username}` instantly...")
    
    collected_urls = set()
    with open(cache_file, "r", encoding="utf-8") as f:
        cached_data = json.load(f)
        collected_urls = set(tuple(item) for item in cached_data)

    await ctx.send(f"🔎 Scanning {len(collected_urls)} posts in memory for keyword: **{keyword.lower()}**...")

    matched_links = [
        url for url, desc in collected_urls 
        if keyword.lower() in desc or keyword.lower() in url.lower()
    ]

    if not matched_links:
        await ctx.send(f"No posts found matching keyword **{keyword}** for profile {username}.")
        return

    file_name = f"deep_scrape_{clean_username}_{keyword}.txt"
    with open(file_name, "w", encoding="utf-8") as out:
        out.write("\n".join(matched_links))

    await ctx.send(
        f"✅ Success! Extracted **{len(matched_links)}** matching links out of {len(collected_urls)} total posts.",
        file=discord.File(file_name)
    )

@bot.command(name="update")
async def update_tiktok(ctx, username: str):
    if not username.startswith("@"):
        username = f"@{username}"
    
    clean_username = username.replace("@", "")
    cache_file = f"cache_{clean_username}.json"
    
    collected_data = {}
    
    # Load existing cache if it exists so we can merge new stuff into it
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            cached_list = json.load(f)
            for item in cached_list:
                full_url, desc = item[0], item[1]
                vid_id = full_url.split("/")[-1]
                collected_data[vid_id] = (full_url, desc)

    existing_ids = set(collected_data.keys())
    found_known_video = False
    
    if existing_ids:
        await ctx.send(f"🔄 **Smart Update active!** Checking `{username}` for new posts... **Check your PowerShell window!**")
    else:
        await ctx.send(f"🔄 Building initial database for `{username}`... **Check your PowerShell window!**")

    profile_url = f"https://www.tiktok.com/{username}"

    try:
        async with async_playwright() as p:
            user_data_dir = os.path.abspath("./tiktok_bot_profile")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = await context.new_page()
            
            async def handle_response(response):
                nonlocal found_known_video
                if "api/recommend/item_list" in response.url or "api/post/item_list" in response.url:
                    try:
                        data = await response.json()
                        items = data.get("itemList", [])
                        for item in items:
                            video_id = item.get("id")
                            desc = item.get("desc", "").lower()
                            if video_id:
                                if video_id in existing_ids:
                                    found_known_video = True
                                
                                full_url = f"https://www.tiktok.com/{username}/video/{video_id}"
                                collected_data[video_id] = (full_url, desc)
                    except Exception:
                        pass

            page.on("response", handle_response)
            await page.goto(profile_url, timeout=60000)
            
            print("\n" + "="*50)
            print("BROWSER IS OPEN! Log in or solve any verification in the browser window.")
            print("Once you are fully logged in and looking at the profile, come back here and PRESS ENTER.")
            print("="*50 + "\n")
            input("Press Enter *only* after you have cleared the verification and are ready to scrape: ")

            print("Scrolling to load posts...")
            no_change_count = 0
            last_height = 0
            
            while True:
                try:
                    if found_known_video:
                        print("🎯 Reached previously cached videos! Stopping scroll early.")
                        break

                    new_height = await page.evaluate("document.body.scrollHeight")
                    if new_height == last_height:
                        no_change_count += 1
                        if no_change_count >= 3:
                            break
                    else:
                        no_change_count = 0
                    last_height = new_height

                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                    await asyncio.sleep(2.5)
                except Exception:
                    await asyncio.sleep(3)
                    continue

            await context.close()
            
            final_list = [[url, desc] for url, desc in collected_data.values()]
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(final_list, f, ensure_ascii=False, indent=2)
            
            await ctx.send(f"✅ **Database updated successfully!** Total posts stored for `{username}`: **{len(final_list)}**.")
            
    except Exception as e:
        await ctx.send(f"❌ Browser automation error: `{e}`")

# Replace this with your actual token only when running it locally on your own machine
bot.run("YOUR_DISCORD_TOKEN_HERE")
