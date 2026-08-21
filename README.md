# 🚀 TikTok Scraper & Discord Bot

A lightning-fast, self-hosted Discord bot that scrapes TikTok profiles, caches data locally, and filters videos by keywords instantly.

---

## 🛠️ Step 1: Install Python & Requirements

1. Download and install **Python** from [python.org](https://www.python.org/downloads/). 
   * ⚠️ **Important:** During installation, check the box that says **"Add Python to PATH"**.
2. Download this repository by clicking the green **Code** button at the top right, clicking **Download ZIP**, and then extracting/unzipping the folder onto your computer.

---

## ⚙️ Step 2: Install Dependencies

1. Open your computer's search bar, type **PowerShell** (or Command Prompt), and open it.
2. Navigate to your extracted bot folder by typing `cd` followed by the folder path (or just type `cd` and drag and drop the folder into the window), then press Enter.
3. Run the following commands one by one to install the required tools:
   ```bash
   pip install -r requirements.txt
   playwright install chromium

---
 
## 🔑 Step 3: Set Up Your Discord Bot Token
1. Go to the Discord Developer Portal and create a bot application.
2. Copy your bot's Token.
3. Open the bot.py file using a text editor (like Notepad or VS Code).
4. Go to the very bottom of the file, find "YOUR_DISCORD_TOKEN_HERE", and replace it with your actual token inside the quotation marks. Save the file.

---

## 🤖 Step 4: Run the Bot
1. In your PowerShell window, run the bot with this command:
   python bot.py
2. Once it says "TikTok Deep Scraper Bot is ready!", head over to your Discord server!

---

## 🎮 Step 5: Discord Commands
- !update @username

  Opens a browser window to fetch the profile's posts.

  Note: If a browser window pops up, log in or solve any TikTok verification if prompted, then go back to your PowerShell window and press Enter to continue. It uses smart caching so future updates take only seconds!
- !scrape @username keyword

  Instantly searches your saved database for that keyword and sends a text file of matching links right into your Discord channel.
