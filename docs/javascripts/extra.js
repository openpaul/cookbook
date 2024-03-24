document.addEventListener('DOMContentLoaded', () => {
  

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

  requestWakeLock();
 
});
