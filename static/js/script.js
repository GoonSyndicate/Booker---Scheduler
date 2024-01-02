$(document).ready(function() {
  // Function to generate the calendar grid
  function generateCalendar(year, month) {
    const calendarBody = document.getElementById('calendar-body');
    const currentMonthYear = document.getElementById('current-month-year');
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDay = firstDay.getDay();
    
    // Clear the calendar
    calendarBody.innerHTML = '';

    // Set the month and year in the header
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    currentMonthYear.textContent = `${monthNames[month]} ${year}`;

    // Create the calendar grid
    let date = 1;
    for (let i = 0; i < 6; i++) {
      const row = document.createElement('tr');
      for (let j = 0; j < 7; j++) {
        if (i === 0 && j < startingDay) {
          const cell = document.createElement('td');
          const prevMonthDay = new Date(year, month, 0 - (startingDay - j));
          cell.textContent = prevMonthDay.getDate();
          cell.classList.add('prev-month-day');
          row.appendChild(cell);
        } else if (date > daysInMonth) {
          const cell = document.createElement('td');
          const nextMonthDay = new Date(year, month + 1, date - daysInMonth);
          cell.textContent = nextMonthDay.getDate();
          cell.classList.add('next-month-day');
          row.appendChild(cell);
          date++;
        } else {
          const cell = document.createElement('td');
          const dayNumber = document.createElement('span');
          dayNumber.textContent = date;
          cell.appendChild(dayNumber);
          row.appendChild(cell);
          date++;
        }
      }
      calendarBody.appendChild(row);
    }
  }

  // Initial calendar generation for the current month
  const currentDate = new Date();
  generateCalendar(currentDate.getFullYear(), currentDate.getMonth());

  // Handle previous month button click
  $('#prev-month').on('click', function() {
    const currentMonth = currentDate.getMonth();
    currentDate.setMonth(currentMonth - 1);
    generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
  });

  // Handle next month button click
  $('#next-month').on('click', function() {
    const currentMonth = currentDate.getMonth();
    currentDate.setMonth(currentMonth + 1);
    generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
  });

  // Handle day cell hover effect
  $('#calendar-body td').hover(
    function() {
      $(this).css('background-color', '#45a049');
      $(this).css('color', 'white');
    },
    function() {
      $(this).css('background-color', '');
      $(this).css('color', '');
    }
  );

  // Handle day cell click event to open the event form
  $('#calendar-body td').click(function() {
    const clickedDate = parseInt($(this).text());

    if (!isNaN(clickedDate)) {
      const currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), clickedDate);
      const formattedDate = currentDate.toISOString().split('T')[0];
      $('#form-date').text(formattedDate);
      $('#event-form').show();
    }
  });

  // Handle save event button click to add and display events
  $('#save-event').click(function() {
    const eventName = $('#event-name').val();
    const startTime = $('#event-start-time').val();
    const endTime = $('#event-end-time').val();
    const eventColor = $('#event-color').val();
    const eventDescription = $('#event-description').val();
    const eventDate = $('#form-date').text();

    // Create an event object with the data
    const event = {
      name: eventName,
      startTime: startTime,
      endTime: endTime,
      color: eventColor,
      description: eventDescription
    };

    // Send the event data to the server to store in the database
    $.ajax({
      type: 'POST',
      url: '/add_event', // Define a Flask route for adding events
      data: JSON.stringify(event),
      contentType: 'application/json',
      success: function(response) {
        // Display the event in the calendar (example: change cell background color)
        $(`td:contains(${eventDate})`).css('background-color', event.color);
        
        // Hide the event form
        $('#event-form').hide();
      },
      error: function(error) {
        console.error('Error:', error);
      }
    });
  });

});
