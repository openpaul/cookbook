document.addEventListener('DOMContentLoaded', () => {
  const wakeLockToggle = document.createElement('input');
  wakeLockToggle.setAttribute('type', 'checkbox');
  wakeLockToggle.setAttribute('id', 'wake-lock-toggle');

  const mdContentDivs = document.querySelectorAll('.md-content');
  const firstMdContentDiv = mdContentDivs[0];
  const article = firstMdContentDiv.querySelector('article');
  firstMdContentDiv.insertBefore(wakeLockToggle, article);

  const wakeLockSwitch = document.querySelector('#wake-lock-toggle');

  let wakeLock = null;

  const requestWakeLock = async () => {
    if ('wakeLock' in navigator) {
      try {
        wakeLock = await navigator.wakeLock.request('screen');      
        wakeLock.addEventListener('release', () => {
          console.log('Wake Lock was released');
        });
        console.log('Wake Lock is active');
      } catch(err) {
        console.error(`Caught ${err.name} acquiring screen lock: ${err.message}`);
      }
    } else {
      console.error('Wake Lock API is not supported.');
    }
  };

  const releaseWakeLock = () => {
    console.log('Releasing wakeLock');

    if (wakeLock) {
      wakeLock.release();
      wakeLock = null;
    } 
  };

  wakeLockSwitch.addEventListener('change', () => {
    const checked = wakeLockSwitch.checked;

    checked ? requestWakeLock() : releaseWakeLock();
  });
});
