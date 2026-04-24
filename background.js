chrome.runtime.onInstalled.addListener(() => {
  console.log('BirdTalk extension installed');
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'GET_API_KEY') {
    chrome.storage.local.get(['twitterApiKey'], (result) => {
      sendResponse({ apiKey: result.twitterApiKey || null });
    });
    return true;
  }
});
