document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      start: 'title',
      center: '',
      end: 'prev,next today', // Navigation buttons
    },
    events: async function (fetchInfo, successCallback, failureCallback) {
      const icalText = `
  BEGIN:VCALENDAR
  PRODID:-//Airbnb Inc//Hosting Calendar 1.0//EN
  CALSCALE:GREGORIAN
  VERSION:2.0
  BEGIN:VEVENT
  DTSTART;VALUE=DATE:20241203
  DTEND;VALUE=DATE:20241206
  SUMMARY:Reserved
  END:VEVENT
  BEGIN:VEVENT
  DTSTART;VALUE=DATE:20241210
  DTEND;VALUE=DATE:20241212
  SUMMARY:Reserved
  END:VEVENT
  BEGIN:VEVENT
  DTSTART;VALUE=DATE:20241224
  DTEND;VALUE=DATE:20241227
  SUMMARY:Reserved
  END:VEVENT
  `;
      try {
        // Parse iCal text
        const events = icalText
          .split('BEGIN:VEVENT')
          .slice(1)
          .map((event) => {
            const summary = event.match(/SUMMARY:(.*)/)?.[1] || 'No Title';
            const startDate = event.match(/DTSTART;VALUE=DATE:(.*)/)?.[1] || '';
            const endDate = event.match(/DTEND;VALUE=DATE:(.*)/)?.[1] || '';
            return {
              title: summary,
              start: startDate,
              end: endDate,
              allDay: true,
            };
          });

        successCallback(events);
      } catch (error) {
        console.error('Error parsing iCal:', error);
        failureCallback(error);
      }
    },
    height: 'auto',

    // Handle user clicks on dates
    dateClick: function (info) {
      const selectedDate = info.dateStr;

      // Redirect user to Airbnb booking page with pre-filled dates
      const airbnbBookingUrl = `https://www.airbnb.com/rooms/1176834180472791861?adults=1&children=0&infants=0&check_in=${selectedDate}&check_out=${getNextDate(
        selectedDate
      )}`;
      window.location.href = airbnbBookingUrl;
    },
  });

  calendar.render();

  // Helper function to calculate the next date (for check-out)
  function getNextDate(dateStr) {
    const date = new Date(dateStr);
    date.setDate(date.getDate() + 1); // Add 1 day for default check-out
    return date.toISOString().split('T')[0]; // Return in YYYY-MM-DD format
  }
});
