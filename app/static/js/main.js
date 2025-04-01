/**
 * Main JavaScript for the Moon Phase Visualization app
 * Provides minimal client-side functionality
 */

document.addEventListener('DOMContentLoaded', function() {
  // Get the current date and set up auto-refresh for the next day
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);
  tomorrow.setHours(0, 0, 30, 0); // Set to 12:00:30 AM
  
  // Calculate milliseconds until next refresh
  const millisUntilRefresh = tomorrow - now;
  
  // Set up a refresh timer for the next day
  if (millisUntilRefresh > 0) {
    setTimeout(function() {
      // Reload the page to get the new moon phase for today
      window.location.reload();
    }, millisUntilRefresh);
  }
  
  // Add animation class to the moon image after a short delay
  setTimeout(function() {
    const moonImage = document.querySelector('.moon-image');
    if (moonImage) {
      moonImage.classList.add('loaded');
    }
  }, 300);
  
  // Format dates to be more readable
  const dateElements = document.querySelectorAll('.format-date');
  dateElements.forEach(function(element) {
    const dateStr = element.textContent;
    if (dateStr) {
      try {
        const date = new Date(dateStr);
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        element.textContent = date.toLocaleDateString(undefined, options);
      } catch (e) {
        console.error('Error formatting date:', e);
      }
    }
  });
});