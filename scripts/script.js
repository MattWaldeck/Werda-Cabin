document.addEventListener('DOMContentLoaded', function () {
  const calendarContainer = document.getElementById('calendar');
  if (calendarContainer) {
    // Create and append the Google Calendar iframe
    const iframe = document.createElement('iframe');
    iframe.src =
      'https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=Africa%2FJohannesburg&showPrint=0&title=Werda%20Cabin&showTz=0&src=ZW4uc2EjaG9saWRheUBncm91cC52LmNhbGVuZGFyLmdvb2dsZS5jb20&src=OXRrNHA3YnRtczI1bWJjdGQxaGpiNW9ibW92MWQya3ZAaW1wb3J0LmNhbGVuZGFyLmdvb2dsZS5jb20&color=%230B8043&color=%239E69AF';
    iframe.style.border = 'solid 1px #777';
    iframe.width = '800';
    iframe.height = '600';
    iframe.frameBorder = '0';
    iframe.scrolling = 'no';

    calendarContainer.appendChild(iframe);
  }
});
