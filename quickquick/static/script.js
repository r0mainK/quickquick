/*jshint esversion: 6 */

const shortenUrl = () => {
    const originalUrl = document.getElementById('original-url').value;
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'original_url': originalUrl})
    };
    const response = fetch('/url/', settings);
    const shortUrlContainer = document.getElementById('short-url-container');
    const errorContainer = document.getElementById('error-container');
    if (!response.ok){
      errorContainer.style.display = 'block';
      shortUrlContainer.style.display = 'none';
      document.body.style.backgroundColor = '#ff4545';
      return;
    }
    errorContainer.style.display = 'none';
    document.body.style.backgroundColor = '#91f086';
    const data = response.json();
    const shortUrlLink = document.getElementById('short-url').querySelector('a');
    shortUrlLink.href = `/${data.id}`;
    shortUrlLink.textContent = `${window.location.origin}/${data.id}`;
    shortUrlContainer.style.display = 'block';
    const copyBtn = document.getElementById('copy-btn');
    copyBtn.textContent = '  Copy ';
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(shortUrlLink.textContent).then(() => {
        copyBtn.textContent = 'Copied !';
      });
    });
  };
  const shortenBtn = document.getElementById('shorten-btn');
  shortenBtn.addEventListener('click', shortenUrl);
  document.addEventListener('keyup', function(event){
    if (event.key === "Enter") {
      shortenUrl();
    }
  });
