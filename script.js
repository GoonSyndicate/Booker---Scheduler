// script.js
const events = {};  
const today = new Date();  
const currentYear = today.getFullYear();  
const currentMonth = today.getMonth();  

const fetchEvents = () => {
  $.ajax({
    url: "http://localhost:5000/get_events",
    type: "GET",
    success: function(response) {
      // Clear the events object to prevent duplication
      Object.keys(events).forEach((key) => {
        delete events[key];
      });

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
          const cellWrapper = document.createElement("div");
          cellWrapper.className = "cell-wrapper";
          
          const currentDay = new Date(year, month, i * 7 + j - firstDay + 1).getDate();
          
          // Check if the day is within the current month
          if ((i === 0 && j < firstDay) || currentDay > daysInMonth) {
              cellWrapper.innerHTML = "";
          } else {
              const dayDiv = document.createElement("div");
              dayDiv.className = "day";
              dayDiv.innerHTML = currentDay;
              
              // Append the dayDiv directly to the cell, not the cellWrapper
              cell.appendChild(dayDiv);
              
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
                      cellWrapper.appendChild(eventDiv);
                  });
              }
          }
          
          if (j === 0 || j === 6) {
              cell.classList.add("weekend");
          }
          
          cell.appendChild(cellWrapper);
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
      fetchEvents();
      discardEvent();
    },
  });
};

const discardEvent = () => {  
  document.getElementById('event-form').style.display = 'none';  
  document.getElementById('event-name').value = '';  
  document.getElementById('event-start-time').value = '';  
  document.getElementById('event-end-time').value = '';  
  document.getElementById('event-color').value = '#4285f4';  
  document.getElementById('event-description').value = '';  
};  

$(document).ready(function() {
  fetchEvents();
  generateCalendar();
});
