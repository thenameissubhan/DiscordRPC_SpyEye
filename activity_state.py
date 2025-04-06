# activity_state.py

from domain_extractor import extract_domain_name
from image_map import load_image_map

import random

adult_states = [
    "Browsing Adult Content 🔞",
    "Private Mode Activated 🕵️",
    "Exploring Lonely Realms 🌌",
    "NSFW Detected... 👀",
    "Doing Research (Probably) 📚",
    "Studying Human Anatomy 🧠",
    "Incognito Mastermind 🕶️",
    "Lost in the Sauce 🍯",
    "Watching Educational Videos (Trust Me) 🎥",
    "Lonely Adventures Ongoing 🗺️",
    "Exploring Forbidden Lands 🚫",
    "Unlocking Secret Levels 🔓",
    "Engaged in Suspicious Activities 🤔",
    "Exploring NSFW Archives 🗂️",
    "Top Secret Content Detected 🧾",
    "Late Night Exploration 🌙",
    "Caught in 4K 📸",
    "Viewer Discretion Advised ⚠️",
    "Content Warning Zone 🚷",
    "Adult Mode: ON 🔥",
    "Not Safe For Work... Obviously 💻",
    "Certified Lonely Hours 💔",
    "Uncensored Adventure Ahead 🚀",
    "Stay Hydrated Champ 🥤",
]


def get_activity_state_and_image(proc_name, active_title):
    """
    Return the activity state text, details, and image key
    based on the extracted domain from active window title.
    """

    domain = extract_domain_name(active_title)
    image_map = load_image_map()

    # --- Social Media & Communication ---
    if domain == "YouTube":
        details = "Watching YouTube"
        state = active_title
        image_key = "youtube_icon"

    elif domain == "Facebook":
        details = "Browsing Facebook"
        state = active_title
        image_key = "facebook_icon"

    elif domain == "Twitter":
        details = "Browsing Twitter"
        state = active_title
        image_key = "x_icon"

    elif domain == "Instagram":
        details = "Browsing Instagram"
        state = active_title
        image_key = "instagram_icon"

    elif domain == "LinkedIn":
        details = "On LinkedIn"
        state = active_title
        image_key = "linkedin_icon"

    elif domain == "Snapchat":
        details = "On Snapchat"
        state = active_title
        image_key = "snapchat_icon"

    elif domain == "TikTok":
        details = "Watching TikTok"
        state = active_title
        image_key = "tiktok_icon"

    elif domain == "Reddit":
        details = "Browsing Reddit"
        state = active_title
        image_key = "reddit_icon"

    elif domain == "Discord":
        details = "Chatting on Discord"
        state = active_title
        image_key = "discord_icon"

    elif domain == "Telegram":
        details = "Messaging on Telegram"
        state = active_title
        image_key = "telegram_icon"

    elif domain == "WhatsApp":
        details = "Messaging on WhatsApp"
        state = active_title
        image_key = "whatsapp_icon"

    elif domain == "WeChat":
        details = "Messaging on WeChat"
        state = active_title
        image_key = "wechat_icon"

    elif domain == "Quora":
        details = "Reading on Quora"
        state = active_title
        image_key = "quora_icon"

    # --- Entertainment & Streaming ---
    elif domain == "Netflix":
        details = "Watching Netflix"
        state = active_title
        image_key = "netflix_icon"

    elif domain in ["Amazon Prime Video", "Prime Video"]:
        details = "Watching Prime Video"
        state = active_title
        image_key = "primevideo_icon"

    elif domain == "Hotstar":
        details = "Watching Hotstar"
        state = active_title
        image_key = "hotstar_icon"

    elif domain == "Twitch":
        details = "Watching Twitch Stream"
        state = active_title
        image_key = "twitch_icon"

    elif domain == "Spotify":
        details = "Listening on Spotify"
        state = active_title
        image_key = "spotify_icon"

    elif domain == "YouTube Music":
        details = "Listening on YouTube Music"
        state = active_title
        image_key = "ytmusic_icon"

    elif domain == "SoundCloud":
        details = "Listening on SoundCloud"
        state = active_title
        image_key = "soundcloud_icon"

    elif domain == "JioCinema":
        details = "Watching JioCinema"
        state = active_title
        image_key = "jiocinema_icon"

    elif domain == "Disney+":
        details = "Watching Disney+"
        state = active_title
        image_key = "disneyplus_icon"

    elif domain == "Hulu":
        details = "Watching Hulu"
        state = active_title
        image_key = "hulu_icon"

    elif domain == "Crunchyroll":
        details = "Watching Anime on Crunchyroll"
        state = active_title
        image_key = "crunchyroll_icon"

    elif domain == "Gaana":
        details = "Listening on Gaana"
        state = active_title
        image_key = "gaana_icon"

    elif domain == "Wynk Music":
        details = "Listening on Wynk Music"
        state = active_title
        image_key = "wynk_icon"

    elif domain == "MX Player":
        details = "Watching MX Player"
        state = active_title
        image_key = "mxplayer_icon"

        # --- AI Platforms / Chatbots / Generative AI ---
    elif domain in ["ChatGPT", "OpenAI"]:
        details = "Chatting with ChatGPT"
        state = active_title
        image_key = "chatgpt_icon"

    elif domain == "Claude":
        details = "Chatting with Claude AI"
        state = active_title
        image_key = "claude_icon"

    elif domain == "Google Gemini":
        details = "Using Google Gemini"
        state = active_title
        image_key = "gemini_icon"

    elif domain == "Perplexity AI":
        details = "Searching on Perplexity AI"
        state = active_title
        image_key = "perplexity_icon"

    elif domain == "Character AI":
        details = "Chatting on Character AI"
        state = active_title
        image_key = "characterai_icon"

    elif domain == "Hugging Face":
        details = "Exploring Hugging Face"
        state = active_title
        image_key = "huggingface_icon"

    elif domain == "GitHub Copilot":
        details = "Using GitHub Copilot"
        state = active_title
        image_key = "copilot_icon"

    elif domain == "Quora Poe":
        details = "Chatting on Poe by Quora"
        state = active_title
        image_key = "poe_icon"

    elif domain == "Replika AI":
        details = "Chatting with Replika AI"
        state = active_title
        image_key = "replika_icon"

    elif domain == "Grok AI":
        details = "Exploring Grok AI"
        state = active_title
        image_key = "grok_icon"

    elif domain == "Jasper AI":
        details = "Writing with Jasper AI"
        state = active_title
        image_key = "jasper_icon"

    elif domain == "Writesonic":
        details = "Creating with Writesonic"
        state = active_title
        image_key = "writesonic_icon"

    elif domain == "You AI":
        details = "Chatting on You AI"
        state = active_title
        image_key = "youai_icon"

    elif domain == "DeepL Write":
        details = "Writing on DeepL Write"
        state = active_title
        image_key = "deepl_icon"

    elif domain == "Copy AI":
        details = "Writing with Copy AI"
        state = active_title
        image_key = "copyai_icon"

    elif domain == "Rytr AI":
        details = "Writing with Rytr AI"
        state = active_title
        image_key = "rytr_icon"

    elif domain == "Notion AI":
        details = "Using Notion AI"
        state = active_title
        image_key = "notionai_icon"

    elif domain == "Socratic":
        details = "Learning with Socratic"
        state = active_title
        image_key = "socratic_icon"

    elif domain == "AI Dungeon":
        details = "Playing AI Dungeon"
        state = active_title
        image_key = "aidungeon_icon"

        # --- Shopping & Marketplaces ---
    elif domain == "Amazon":
        details = "Browsing Amazon"
        state = active_title
        image_key = "amazon_icon"

    elif domain == "Flipkart":
        details = "Browsing Flipkart"
        state = active_title
        image_key = "flipkart_icon"

    elif domain == "eBay":
        details = "Shopping on eBay"
        state = active_title
        image_key = "ebay_icon"

    elif domain == "AliExpress":
        details = "Browsing AliExpress"
        state = active_title
        image_key = "aliexpress_icon"

    elif domain == "Myntra":
        details = "Browsing Myntra"
        state = active_title
        image_key = "myntra_icon"

    elif domain == "Shein":
        details = "Browsing Shein"
        state = active_title
        image_key = "shein_icon"

    elif domain == "Nykaa":
        details = "Shopping on Nykaa"
        state = active_title
        image_key = "nykaa_icon"

    elif domain == "Meesho":
        details = "Browsing Meesho"
        state = active_title
        image_key = "meesho_icon"

        # --- Productivity & Work ---
    elif domain == "Gmail":
        details = "Checking Gmail"
        state = active_title
        image_key = "gmail_icon"

    elif domain == "Microsoft":
        details = "Using Microsoft Services"
        state = active_title
        image_key = "microsoft_icon"

    elif domain == "Google Drive":
        details = "Browsing Google Drive"
        state = active_title
        image_key = "gdrive_icon"

    elif domain == "Google Docs":
        details = "Editing Google Docs"
        state = active_title
        image_key = "gdocs_icon"

    elif domain == "Slack":
        details = "Chatting on Slack"
        state = active_title
        image_key = "slack_icon"

    elif domain == "Zoom":
        details = "In a Zoom Meeting"
        state = active_title
        image_key = "zoom_icon"

    elif domain == "Notion":
        details = "Working on Notion"
        state = active_title
        image_key = "notion_icon"

    elif domain == "Trello":
        details = "Using Trello Boards"
        state = active_title
        image_key = "trello_icon"

    elif domain == "Dropbox":
        details = "Browsing Dropbox"
        state = active_title
        image_key = "dropbox_icon"

    # --- Developer / Coding Platforms ---
    elif domain == "StackOverflow":
        details = "Browsing StackOverflow"
        state = active_title
        image_key = "stackoverflow_icon"

    elif domain == "GitHub":
        details = "Browsing GitHub"
        state = active_title
        image_key = "github_icon"

    elif domain == "GitLab":
        details = "Browsing GitLab"
        state = active_title
        image_key = "gitlab_icon"

    elif domain == "Replit":
        details = "Coding on Replit"
        state = active_title
        image_key = "replit_icon"

    elif domain == "HackerRank":
        details = "Practicing on HackerRank"
        state = active_title
        image_key = "hackerrank_icon"

    elif domain == "LeetCode":
        details = "Grinding LeetCode"
        state = active_title
        image_key = "leetcode_icon"

    elif domain == "GeeksforGeeks":
        details = "Learning on GeeksforGeeks"
        state = active_title
        image_key = "gfg_icon"

    elif domain == "CodePen":
        details = "Building on CodePen"
        state = active_title
        image_key = "codepen_icon"

    elif domain == "JSFiddle":
        details = "Using JSFiddle"
        state = active_title
        image_key = "jsfiddle_icon"

    elif domain == "W3Schools":
        details = "Learning from W3Schools"
        state = active_title
        image_key = "w3schools_icon"

    elif domain == "Coursera":
        details = "Learning on Coursera"
        state = active_title
        image_key = "coursera_icon"

    elif domain == "Udemy":
        details = "Taking a Udemy Course"
        state = active_title
        image_key = "udemy_icon"

    elif domain == "edX":
        details = "Learning on edX"
        state = active_title
        image_key = "edx_icon"

    elif domain == "FreeCodeCamp":
        details = "Practicing on FreeCodeCamp"
        state = active_title
        image_key = "freecodecamp_icon"

        # --- Search Engines ---
    elif domain == "Google":
        details = "Searching on Google"
        state = active_title
        image_key = "google_icon"

    elif domain == "Bing":
        details = "Searching on Bing"
        state = active_title
        image_key = "bing_icon"

    elif domain == "DuckDuckGo":
        details = "Searching on DuckDuckGo"
        state = active_title
        image_key = "duckduckgo_icon"

    elif domain == "Yahoo":
        details = "Searching on Yahoo"
        state = active_title
        image_key = "yahoo_icon"

    elif domain == "Yandex":
        details = "Searching on Yandex"
        state = active_title
        image_key = "yandex_icon"

    elif domain == "Baidu":
        details = "Searching on Baidu"
        state = active_title
        image_key = "baidu_icon"

    # --- News & Forums ---
    elif domain == "Medium":
        details = "Reading on Medium"
        state = active_title
        image_key = "medium_icon"

    elif domain == "BBC":
        details = "Browsing BBC News"
        state = active_title
        image_key = "bbc_icon"

    elif domain == "CNN":
        details = "Browsing CNN News"
        state = active_title
        image_key = "cnn_icon"

    elif domain == "Hacker News":
        details = "Browsing Hacker News"
        state = active_title
        image_key = "hackernews_icon"

    elif domain == "4chan":
        details = "Browsing 4chan"
        state = active_title
        image_key = "4chan_icon"

    elif domain == "9GAG":
        details = "Browsing 9GAG"
        state = active_title
        image_key = "9gag_icon"

    # --- Meme & Geek/Niche Sites ---
    elif domain == "Imgur":
        details = "Browsing Imgur"
        state = active_title
        image_key = "imgur_icon"

    elif domain == "KnowYourMeme":
        details = "Exploring KnowYourMeme"
        state = active_title
        image_key = "knowyourmeme_icon"

    elif domain == "Memedroid":
        details = "Browsing Memedroid"
        state = active_title
        image_key = "memedroid_icon"

    elif domain == "XKCD":
        details = "Reading XKCD Comics"
        state = active_title
        image_key = "xkcd_icon"

    elif domain == "Explosm":
        details = "Reading Cyanide & Happiness"
        state = active_title
        image_key = "explosm_icon"

        # --- Anime / Gaming / Otaku Stuff ---
    elif domain == "Crunchyroll":
        details = "Watching Anime on Crunchyroll"
        state = active_title
        image_key = "crunchyroll_icon"

    elif domain == "Funimation":
        details = "Watching Anime on Funimation"
        state = active_title
        image_key = "funimation_icon"

    elif domain == "MyAnimeList":
        details = "Browsing MyAnimeList"
        state = active_title
        image_key = "myanimelist_icon"

    elif domain == "AniList":
        details = "Browsing AniList"
        state = active_title
        image_key = "anilist_icon"

    elif domain == "Twitch":
        details = "Watching Twitch Streams"
        state = active_title
        image_key = "twitch_icon"

    elif domain == "Steam":
        details = "Browsing Steam"
        state = active_title
        image_key = "steam_icon"

    elif domain == "Epic Games":
        details = "Browsing Epic Games Store"
        state = active_title
        image_key = "epicgames_icon"

    elif domain == "Roblox":
        details = "Playing Roblox"
        state = active_title
        image_key = "roblox_icon"

    elif domain == "Minecraft":
        details = "Exploring Minecraft"
        state = active_title
        image_key = "minecraft_icon"

    elif domain == "League of Legends":
        details = "Playing League of Legends"
        state = active_title
        image_key = "lol_icon"

    elif domain == "Valorant":
        details = "Playing Valorant"
        state = active_title
        image_key = "valorant_icon"

    elif domain == "Fortnite":
        details = "Playing Fortnite"
        state = active_title
        image_key = "fortnite_icon"

    elif domain == "PUBG":
        details = "Playing PUBG"
        state = active_title
        image_key = "pubg_icon"

        # --- Torrent Trackers ---
    elif domain == "1337x":
        details = "Browsing 1337x Torrents"
        state = active_title
        image_key = "1337x_icon"

    elif domain == "The Pirate Bay":
        details = "Sailing The Pirate Bay"
        state = active_title
        image_key = "piratebay_icon"

    elif domain == "RARBG":
        details = "Browsing RARBG Torrents"
        state = active_title
        image_key = "rarbg_icon"

    elif domain == "YTS":
        details = "Browsing YTS Torrents"
        state = active_title
        image_key = "yts_icon"

    elif domain == "LimeTorrents":
        details = "Browsing LimeTorrents"
        state = active_title
        image_key = "limetorrents_icon"

    elif domain == "TorrentGalaxy":
        details = "Browsing TorrentGalaxy"
        state = active_title
        image_key = "torrentgalaxy_icon"

    elif domain == "Kickass Torrents":
        details = "Browsing Kickass Torrents"
        state = active_title
        image_key = "kat_icon"

    # --- Dark Web / Onion (Optional) ---
    elif domain == "Tor Project":
        details = "Exploring The Tor Project"
        state = active_title
        image_key = "tor_icon"

    elif domain == "ProtonMail":
        details = "Using ProtonMail"
        state = active_title
        image_key = "protonmail_icon"

    elif domain == "DuckDuckGo":
        details = "Searching with DuckDuckGo"
        state = active_title
        image_key = "duckduckgo_icon"

    elif domain == "Brave Browser":
        details = "Using Brave Browser"
        state = active_title
        image_key = "brave_icon"

    elif domain == "Tails OS":
        details = "Exploring Tails OS"
        state = active_title
        image_key = "tails_icon"

    elif domain == "DuckDuckGo Onion":
        details = "Searching DuckDuckGo (Onion)"
        state = active_title
        image_key = "duckduckgo_icon"

        # --- Crypto / Web3 / Blockchain / NFT / DeFi Platforms ---
    elif domain == "Binance":
        details = "Trading on Binance"
        state = active_title
        image_key = "binance_icon"

    elif domain == "Coinbase":
        details = "Trading on Coinbase"
        state = active_title
        image_key = "coinbase_icon"

    elif domain == "CoinMarketCap":
        details = "Browsing CoinMarketCap"
        state = active_title
        image_key = "coinmarketcap_icon"

    elif domain == "CoinGecko":
        details = "Browsing CoinGecko"
        state = active_title
        image_key = "coingecko_icon"

    elif domain == "Trust Wallet":
        details = "Using Trust Wallet"
        state = active_title
        image_key = "trustwallet_icon"

    elif domain == "MetaMask":
        details = "Using MetaMask Wallet"
        state = active_title
        image_key = "metamask_icon"

    elif domain == "Blockchain.com":
        details = "Exploring Blockchain.com"
        state = active_title
        image_key = "blockchain_icon"

    elif domain == "Kraken":
        details = "Trading on Kraken"
        state = active_title
        image_key = "kraken_icon"

    elif domain == "KuCoin":
        details = "Trading on KuCoin"
        state = active_title
        image_key = "kucoin_icon"

    elif domain == "OKX":
        details = "Trading on OKX"
        state = active_title
        image_key = "okx_icon"

    elif domain == "Gate.io":
        details = "Trading on Gate.io"
        state = active_title
        image_key = "gateio_icon"

    elif domain == "Bybit":
        details = "Trading on Bybit"
        state = active_title
        image_key = "bybit_icon"

    elif domain == "Bitfinex":
        details = "Trading on Bitfinex"
        state = active_title
        image_key = "bitfinex_icon"

    elif domain == "Crypto.com":
        details = "Trading on Crypto.com"
        state = active_title
        image_key = "cryptocom_icon"

    elif domain == "Uniswap":
        details = "Swapping on Uniswap"
        state = active_title
        image_key = "uniswap_icon"

    elif domain == "PancakeSwap":
        details = "Swapping on PancakeSwap"
        state = active_title
        image_key = "pancakeswap_icon"

    elif domain == "Opensea":
        details = "Browsing NFTs on Opensea"
        state = active_title
        image_key = "opensea_icon"

    elif domain == "Rarible":
        details = "Browsing NFTs on Rarible"
        state = active_title
        image_key = "rarible_icon"

    elif domain == "Etherscan":
        details = "Exploring Etherscan"
        state = active_title
        image_key = "etherscan_icon"

    elif domain == "Dune Analytics":
        details = "Viewing Dune Analytics"
        state = active_title
        image_key = "dune_icon"

    elif domain == "Phantom Wallet":
        details = "Using Phantom Wallet"
        state = active_title
        image_key = "phantom_icon"

    elif domain == "Solscan":
        details = "Exploring Solscan"
        state = active_title
        image_key = "solscan_icon"

    elif domain == "LooksRare":
        details = "Browsing NFTs on LooksRare"
        state = active_title
        image_key = "looksrare_icon"

    elif domain == "Magic Eden":
        details = "Browsing NFTs on Magic Eden"
        state = active_title
        image_key = "magiceden_icon"

    elif domain == "DefiLlama":
        details = "Exploring DefiLlama"
        state = active_title
        image_key = "defillama_icon"

    elif domain == "Ledger":
        details = "Using Ledger Wallet"
        state = active_title
        image_key = "ledger_icon"

    elif domain == "Trezor":
        details = "Using Trezor Wallet"
        state = active_title
        image_key = "trezor_icon"

    elif domain == "Zapper":
        details = "Exploring Zapper"
        state = active_title
        image_key = "zapper_icon"

    elif domain == "Blur NFT":
        details = "Browsing NFTs on Blur"
        state = active_title
        image_key = "blur_icon"

    # Adult Content
    elif domain == "Pornhub":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "XVideos":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "XNXX":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "OnlyFans":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "RedTube":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "Brazzers":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "YouPorn":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "SpankBang":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "Chaturbate":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "BangBros":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "RealityKings":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "NaughtyAmerica":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "XHamster":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "CamSoda":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "Stripchat":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    elif domain == "Fansly":
        details = random.choice(adult_states)
        state = active_title
        image_key = "adult_icon"

    else:
        details = f"Active on {proc_name.capitalize()}"
        state = active_title
        image_key = image_map.get(proc_name, "default_icon")

    if len(state) > 128:
        state = state[:125] + "..."

    return state, details, image_key
