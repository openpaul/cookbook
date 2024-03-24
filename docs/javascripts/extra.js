// Function to request a screen wake lock

const requestWakeLock = async () => {
  try {
    wakeLock = await navigator.wakeLock.request('screen');

    wakeLock.addEventListener('release', () => {
      console.log('Wake Lock was released');
    });
    console.log('Wake Lock is active');
  }
  catch(err) {
    console.error('Failed with error:', err);
  }
};

// Call the function to request the screen wake lock
requestWakeLock();
