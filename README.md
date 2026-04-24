# BirdTalk - Chrome Extension

A beautiful Chrome extension that displays the most popular tweets from any Twitter account in your browser sidebar.

## Features

- 🐦 View popular tweets from any Twitter handle
- 📊 See engagement metrics (likes, retweets, replies)
- 🎨 Blue and white theme with a modern, clean interface
- 📱 Responsive sidebar popup design
- 🔄 Load more tweets with a single click
- 💾 Remembers your last searched account
- 🔐 Securely stores your Twitter API token locally

## Setup Instructions

### Step 1: Get Your Twitter API Key

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app or select an existing one
3. Navigate to the "Keys and tokens" section
4. Copy your **Bearer Token** (you need API v2 access)

### Step 2: Install the Extension

1. Clone or download this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top right)
4. Click "Load unpacked" and select the folder containing this extension
5. The BirdTalk extension should now appear in your extensions list

### Step 3: Configure Your API Key

1. Click the BirdTalk extension icon in your Chrome toolbar
2. Scroll down and click the "⚙️ API Configuration" section
3. Paste your Twitter API Bearer Token
4. Click "Save Token"

## How to Use

1. Click the BirdTalk extension icon in your toolbar
2. Enter a Twitter handle (with or without @) in the search field
3. Click "Search" or press Enter
4. The extension will fetch and display the most popular tweets from that account
5. Click "Show More Tweets" to load additional tweets
6. Each tweet shows:
   - Author name and handle
   - Tweet text
   - Like count, retweet count, and reply count
   - Time posted

## Troubleshooting

### "Please configure your Twitter API key first"
- Make sure you've saved your API key in the extension settings
- Your token should be a Bearer Token from Twitter API v2

### "User not found"
- Check that you spelled the Twitter handle correctly
- The account must be public to be accessible via the API

### "Failed to fetch tweets"
- Your API key might be invalid or expired
- Check that your app has the correct permissions in the Twitter Developer Portal
- Make sure your API key has read-only access (you don't need write permissions)

## Technical Details

- **Manifest Version:** 3 (latest Chrome extension standard)
- **API:** Twitter API v2
- **Storage:** Chrome local storage (secure and private)
- **No external dependencies** - pure vanilla JavaScript

## File Structure

```
.
├── manifest.json      # Extension configuration
├── popup.html         # User interface
├── popup.css          # Styling with blue/white theme
├── popup.js           # Main logic for fetching and displaying tweets
├── background.js      # Service worker for background tasks
└── README.md          # This file
```

## Privacy & Security

- Your API key is stored locally in Chrome and never sent anywhere except to Twitter's servers
- The extension only makes requests to Twitter's official API
- No data is collected or stored on external servers

## License

MIT License - Feel free to use and modify as you like!
