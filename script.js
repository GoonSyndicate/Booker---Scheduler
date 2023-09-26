const events = {};  
    const today = new Date();  
    const currentYear = today.getFullYear();  
    const currentMonth = today.getMonth();  

  const fetchEvents = () => {
      $.ajax({
        url: "http://localhost:5000/get_events", // Added in the proper link for events cause I'm stupid lol
        type: "GET",
        success: function(response) {
          console.log(response);
          response.forEach(event => {
            const day = event[0];
            if (!events[day]) {
              events[day] = [];
            }
            events[day].push({
              name: event[1],
              startTime: event[2],
              endTime: event[3],
              description: event[4],
              color: event[5]
            });
          });
          generateCalendar();
        }
      });
    };

    // Call fetchEvents function when the page loads
    $(document).ready(function() {
      fetchEvents();
    });

    const generateCalendar = (year = currentYear, month = currentMonth) => {  
      const tbody = document.getElementById("calendar-body");  
      tbody.innerHTML = "";  
      const firstDay = new Date(year, month, 1).getDay();  
      const daysInMonth = new Date(year, month + 1, 0).getDate();  
      for (let i = 0; i < 5; i++) {  
        const row = document.createElement("tr");  
        for (let j = 0; j < 7; j++) {  
          const cell = document.createElement("td");  
          const currentDay = new Date(year, month, i * 7 + j - firstDay + 1).getDate();  
          if ((i === 0 && j < firstDay) || currentDay > daysInMonth) {  
            cell.innerHTML = "";  
          } else {  
            cell.innerHTML = `<div class="day">${currentDay}</div>`;  
            cell.onclick = () => selectDate(currentDay);  
            if (events[currentDay]) {  
              events[currentDay].forEach((event, index) => {  
                const eventDiv = document.createElement("div");  
                eventDiv.className = "event";  
                eventDiv.style.backgroundColor = event.color;  
                eventDiv.innerHTML = `${event.name} <span>${event.startTime} - ${event.endTime}</span>`;  
                eventDiv.title = event.description;  
                eventDiv.onclick = (e) => {  
                  e.stopPropagation();  
                  editEvent(currentDay, index);  
                };  
                cell.appendChild(eventDiv);  
              });  
            }  
          }  
          if (j === 0 || j === 6) {  
            cell.classList.add("weekend");  
          }  
          row.appendChild(cell);  
        }  
        tbody.appendChild(row);  
      }  
      document.querySelector("h1").textContent = `Booking Calendar for ${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}`;  
    };  
  
    const generateWeekView = (day) => {  
      const weekView = document.getElementById("week-view");  
      weekView.innerHTML = "";  
      for (let i = 0; i < 7; i++) {  
        const dayDiv = document.createElement("div");  
        dayDiv.className = "day";  
        for (let j = 0; j < 24; j++) {  
          const hourDiv = document.createElement("div");  
          hourDiv.className = "hour";  
          hourDiv.dataset.hour = `${j}:00`;  
          dayDiv.appendChild(hourDiv);  
        }  
        weekView.appendChild(dayDiv);  
      }  
      weekView.style.display = "flex";  
    };  

    const selectDate = (day) => {  
      document.getElementById('form-date').innerText = `${new Date(currentYear, currentMonth, day).toLocaleString('default', { month: 'long' })} ${day}, ${currentYear}`;  
      document.getElementById('event-form').style.display = 'block';  
      document.getElementById('event-form').dataset.day = day;  
      document.getElementById('event-form').dataset.index = -1;  // For new events  
      document.getElementById('form-title').textContent = 'Add Event';
    generateWeekView(day);  
  }; 
  
    

    const editEvent = (day, index) => {  
      const event = events[day][index];  
      document.getElementById('form-date').innerText = `${new Date(currentYear, currentMonth, day).toLocaleString('default', { month: 'long' })} ${day}, ${currentYear}`;  
      document.getElementById('event-form').style.display = 'block';  
      document.getElementById('event-form').dataset.day = day;  
      document.getElementById('event-form').dataset.index = index;  
      document.getElementById('event-name').value = event.name;  
      document.getElementById('event-start-time').value = event.startTime;  
      document.getElementById('event-end-time').value = event.endTime;  
      document.getElementById('event-color').value = event.color;  
      document.getElementById('event-description').value = event.description;  
      document.getElementById('form-title').textContent = 'Edit Event';
  }; 
    
  
  const saveEvent = () => {
    console.log("Save button clicked");
    const day = document.getElementById('event-form').dataset.day;
    const name = document.getElementById('event-name').value;
    const startTime = document.getElementById('event-start-time').value;
    const endTime = document.getElementById('event-end-time').value;
    const description = document.getElementById('event-description').value;
    const color = document.getElementById('event-color').value;

    $.ajax({
      url: "http://localhost:5000/add_event",
      type: "POST",
      dataType: "json",
      data: JSON.stringify({
        day,
        name,
        startTime,
        endTime,
        description,
        color,
      }),
      contentType: "application/json; charset=utf-8",
      success: function (response) {
        generateCalendar();
        discardEvent();
      },
    });
  };
  
    const discardEvent = () => {  
      console.log("Discard button clicked");
      document.getElementById('event-form').style.display = 'none';  
      document.getElementById('event-name').value = 'Sample Event';  
      document.getElementById('event-start-time').value = '12:00';  
      document.getElementById('event-end-time').value = '13:00';  
      document.getElementById('event-color').value = '#4285f4';  
      document.getElementById('event-description').value = 'Sample Description';  
    };  
  

      
  // Call fetchEvents function when the page loads
  $(document).ready(function() {
    fetchEvents();
  });

  // Initialize the calendar
  $(document).ready(function () {
    generateCalendar();

    $.ajax({
      url: "http://localhost:5000/get_events",
      type: "GET",
      dataType: "json",
      success: function (response) {
        response.forEach(function (event) {
          if (!events[event[1]]) {
            events[event[1]] = [];
          }
          events[event[1]].push({
            name: event[2],
            startTime: event[3],
            endTime: event[4],
            description: event[5],
            color: event[6],
          });
        });
        generateCalendar();
      },
    });
  });
