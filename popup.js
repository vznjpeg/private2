const TWEETS_PER_PAGE = 5;
let currentHandle = '';
let allTweets = [];
let displayedTweetsCount = 0;

const elements = {
  twitterHandle: document.getElementById('twitterHandle'),
  searchBtn: document.getElementById('searchBtn'),
  tweetsContainer: document.getElementById('tweetsContainer'),
  showMoreBtn: document.getElementById('showMoreBtn'),
  errorMessage: document.getElementById('errorMessage'),
  loadingSpinner: document.getElementById('loadingSpinner'),
  noResults: document.getElementById('noResults'),
  apiKey: document.getElementById('apiKey'),
  saveApiKeyBtn: document.getElementById('saveApiKeyBtn'),
  apiKeyStatus: document.getElementById('apiKeyStatus'),
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadApiKey();
  loadLastHandle();
  setupEventListeners();
});

function setupEventListeners() {
  elements.searchBtn.addEventListener('click', handleSearch);
  elements.twitterHandle.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSearch();
  });
  elements.showMoreBtn.addEventListener('click', displayMoreTweets);
  elements.saveApiKeyBtn.addEventListener('click', saveApiKey);
}

function loadApiKey() {
  chrome.storage.local.get(['twitterApiKey'], (result) => {
    if (result.twitterApiKey) {
      elements.apiKey.value = result.twitterApiKey;
      updateApiKeyStatus('✓ Token saved', 'success');
    }
  });
}

function saveApiKey() {
  const apiKey = elements.apiKey.value.trim();
  if (!apiKey) {
    updateApiKeyStatus('⚠ Please enter a token', 'error');
    return;
  }

  chrome.storage.local.set({ twitterApiKey: apiKey }, () => {
    updateApiKeyStatus('✓ Token saved successfully', 'success');
  });
}

function updateApiKeyStatus(message, status) {
  elements.apiKeyStatus.textContent = message;
  elements.apiKeyStatus.className = `api-key-status ${status}`;
  if (status === 'success') {
    setTimeout(() => {
      elements.apiKeyStatus.textContent = '';
    }, 3000);
  }
}

function loadLastHandle() {
  chrome.storage.local.get(['lastHandle'], (result) => {
    if (result.lastHandle) {
      elements.twitterHandle.value = result.lastHandle;
    }
  });
}

function saveLastHandle(handle) {
  chrome.storage.local.set({ lastHandle: handle });
}

async function handleSearch() {
  const handle = elements.twitterHandle.value.trim().replace('@', '');
  if (!handle) {
    showError('Please enter a Twitter handle');
    return;
  }

  currentHandle = handle;
  saveLastHandle(handle);
  allTweets = [];
  displayedTweetsCount = 0;

  showLoading(true);
  hideError();
  elements.tweetsContainer.innerHTML = '';
  elements.showMoreBtn.style.display = 'none';
  elements.noResults.style.display = 'none';

  try {
    const apiKey = await getApiKey();
    if (!apiKey) {
      showError('Please configure your Twitter API key first');
      showLoading(false);
      return;
    }

    const userId = await getUserId(handle, apiKey);
    if (!userId) {
      showError(`User "${handle}" not found`);
      showLoading(false);
      return;
    }

    allTweets = await getTweets(userId, apiKey);

    if (allTweets.length === 0) {
      elements.noResults.style.display = 'block';
    } else {
      displayMoreTweets();
    }
  } catch (error) {
    console.error('Error:', error);
    showError(error.message || 'Failed to fetch tweets. Please try again.');
  } finally {
    showLoading(false);
  }
}

async function getApiKey() {
  return new Promise((resolve) => {
    chrome.storage.local.get(['twitterApiKey'], (result) => {
      resolve(result.twitterApiKey || null);
    });
  });
}

async function getUserId(handle, apiKey) {
  try {
    const response = await fetch(
      `https://api.twitter.com/2/users/by/username/${handle}?user.fields=public_metrics,profile_image_url`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
        },
      }
    );

    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error('Failed to fetch user data');
    }

    const data = await response.json();
    return data.data.id;
  } catch (error) {
    console.error('Error fetching user ID:', error);
    throw error;
  }
}

async function getTweets(userId, apiKey) {
  try {
    const response = await fetch(
      `https://api.twitter.com/2/users/${userId}/tweets?max_results=100&tweet.fields=created_at,public_metrics,author_id&expansions=author_id&user.fields=username,name,profile_image_url`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch tweets');
    }

    const data = await response.json();
    const tweets = data.data || [];
    const users = data.includes?.users || [];

    const userMap = {};
    users.forEach((user) => {
      userMap[user.id] = user;
    });

    return tweets
      .filter((tweet) => !tweet.text.startsWith('RT @'))
      .sort((a, b) => (b.public_metrics?.like_count || 0) - (a.public_metrics?.like_count || 0))
      .slice(0, 50)
      .map((tweet) => ({
        id: tweet.id,
        text: tweet.text,
        likes: tweet.public_metrics?.like_count || 0,
        retweets: tweet.public_metrics?.retweet_count || 0,
        replies: tweet.public_metrics?.reply_count || 0,
        user: userMap[tweet.author_id] || { name: 'Unknown', username: 'unknown' },
        created_at: tweet.created_at,
      }));
  } catch (error) {
    console.error('Error fetching tweets:', error);
    throw error;
  }
}

function displayMoreTweets() {
  const startIndex = displayedTweetsCount;
  const endIndex = Math.min(startIndex + TWEETS_PER_PAGE, allTweets.length);

  for (let i = startIndex; i < endIndex; i++) {
    const tweet = allTweets[i];
    const tweetElement = createTweetElement(tweet);
    elements.tweetsContainer.appendChild(tweetElement);
  }

  displayedTweetsCount = endIndex;

  if (displayedTweetsCount >= allTweets.length) {
    elements.showMoreBtn.style.display = 'none';
  } else {
    elements.showMoreBtn.style.display = 'block';
  }
}

function createTweetElement(tweet) {
  const div = document.createElement('div');
  div.className = 'tweet';

  const date = new Date(tweet.created_at);
  const timeAgo = getTimeAgo(date);
  const initial = (tweet.user.name || 'U')[0].toUpperCase();

  div.innerHTML = `
    <div class="tweet-author">
      <div class="tweet-avatar">${initial}</div>
      <div class="tweet-name">
        <div class="tweet-handle">${escapeHtml(tweet.user.name)}</div>
        <div class="tweet-username">@${escapeHtml(tweet.user.username)}</div>
      </div>
    </div>
    <div class="tweet-text">${escapeHtml(tweet.text)}</div>
    <div class="tweet-stats">
      <div class="tweet-stat">
        <span>❤️</span>
        <span class="tweet-stat-number">${formatNumber(tweet.likes)}</span>
      </div>
      <div class="tweet-stat">
        <span>🔄</span>
        <span class="tweet-stat-number">${formatNumber(tweet.retweets)}</span>
      </div>
      <div class="tweet-stat">
        <span>💬</span>
        <span class="tweet-stat-number">${formatNumber(tweet.replies)}</span>
      </div>
      <div class="tweet-stat" style="margin-left: auto; color: #657786;">
        ${timeAgo}
      </div>
    </div>
  `;

  return div;
}

function getTimeAgo(date) {
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) return 'now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d`;
  const weeks = Math.floor(days / 7);
  return `${weeks}w`;
}

function formatNumber(num) {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
  return num.toString();
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function showLoading(show) {
  elements.loadingSpinner.style.display = show ? 'flex' : 'none';
}

function showError(message) {
  elements.errorMessage.textContent = message;
  elements.errorMessage.style.display = 'block';
}

function hideError() {
  elements.errorMessage.style.display = 'none';
}
