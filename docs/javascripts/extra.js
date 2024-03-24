document.addEventListener('DOMContentLoaded', () => {
  const wakeLockToggle = document.createElement('button');
  wakeLockToggle.setAttribute('id', 'wake-lock-toggle');
  wakeLockToggle.textContent = 'Toggle Wake Lock'; // Add text content to the button


  const mdContentDivs = document.querySelectorAll('.md-content');
  const firstMdContentDiv = mdContentDivs[0];
  const article = firstMdContentDiv.querySelector('article');
  firstMdContentDiv.insertBefore(wakeLockToggle, article);

  const wakeLockSwitch = document.querySelector('#wake-lock-toggle');

  let wakeLock = null;

  const requestWakeLock = async () => {
    try {
      wakeLock = await navigator.wakeLock.request('screen');      
      wakeLock.addEventListener('release', () => {
        console.log('Wake Lock was released');
      });
      console.log('Wake Lock is active');
    }
    catch(err) {
      console.error(`Caught ${err.name} acquiring screen lock: ${err.message}`);
    }
  };

  const releaseWakeLock = () => {
    console.log('Releasing wakeLock');

    wakeLock.release();
    wakeLock = null;
  };

  wakeLockSwitch.addEventListener('click', () => {
    const checked = wakeLockSwitch.checked;

    checked ? requestWakeLock() : releaseWakeLock();
  });
});
