// script.js
let events = {};
const today = new Date();
let currentYear = today.getFullYear();  
let currentMonth = today.getMonth();  


const fetchEvents = () => {  
  console.log("Fetching events from server...");  
  $.get(`http://localhost:5000/get_events?year=${currentYear}&month=${currentMonth}`, function (response) {  
    console.log("Events fetched from server: ", response);  
    events = {}; // Clear existing events  
    response.forEach(([id, date, name, startTime, endTime, description, color]) => {  
      if (!events[date]) events[date] = [];  
      events[date].push({ id, name, startTime, endTime, description, color });  
    });  
    generateCalendar();  
  });  
};  
  


const saveEvent = () => {  
  const form = document.getElementById("event-form");  
  const data = {  
    date: form.dataset.date,  
    name: document.getElementById("event-name").value.trim(),  
    startTime: document.getElementById("event-start-time").value,  
    endTime: document.getElementById("event-end-time").value,  
    description: document.getElementById("event-description").value.trim(),  
    color: document.getElementById("event-color").value  
  };  
  
  if (form.dataset.id && form.dataset.id !== "null") {  
    data.id = form.dataset.id;  
  } else {  
    data.id = null;  
  }  
  
  // Field Validation  
  if (!data.name || !data.startTime || !data.endTime || !data.description || !data.color) {  
      alert("All fields are required");  
      return;  
  }  
  
  // Time Bounds Check  
  if (data.startTime > "23:59" || data.endTime > "23:59" || data.startTime < "00:00" || data.endTime < "00:00") {  
      alert("Invalid time");  
      return;  
  }  
  
  console.log("Data being sent to server: ", data);  
  
  const url = data.id ? "http://localhost:5000/update_event" : "http://localhost:5000/add_event";  
  const method = data.id ? "PUT" : "POST";  
  
  $.ajax({  
    url,  
    type: method,  
    data: JSON.stringify(data),  
    contentType: "application/json; charset=utf-8",  
    success: function(response) {  
      console.log("Server response: ", response);  
      fetchEvents();  
    },  
    complete: discardEvent  
  });  
};  
  
const editEvent = (date, index) => {  
  const event = events[date][index];  
  const form = document.getElementById("event-form");  
  form.dataset.id = event.id;  
  console.log("Setting form.dataset.id to ", event.id);  
  form.dataset.date = date;  
  form.dataset.index = index;  
  document.getElementById("event-name").value = event.name;  
  document.getElementById("event-start-time").value = event.startTime;  
  document.getElementById("event-end-time").value = event.endTime;  
  document.getElementById("event-color").value = event.color;  
  document.getElementById("event-description").value = event.description;  
  document.getElementById("form-title").textContent = "Edit Event";  
  form.style.display = "block";  
  const tooltips = document.querySelectorAll('.tooltip');  
  tooltips[index].style.display = 'none';  
  
  form.style.display = "block";  
};  


const deleteEvent = () => {
  const id = document.getElementById("event-form").dataset.id;
  if (!id) return;
  $.ajax({
    url: "http://localhost:5000/delete_event",
    type: "DELETE",
    data: JSON.stringify({ id }),
    contentType: "application/json; charset=utf-8",
    success: fetchEvents,
    complete: discardEvent
  });
};



const selectDate = (day, event) => {  
  event.stopPropagation();  // Add this line  
  const form = document.getElementById("event-form");  
  form.dataset.id = null;  
  form.dataset.date = `${currentYear}-${currentMonth+1}-${day}`;  
  form.dataset.index = null;  
  document.getElementById("form-title").textContent = "Add Event";  
  form.style.left = `${event.pageX}px`;  
  form.style.top = `${event.pageY}px`;  
  form.style.display = "block";  
  console.log("Form should be displayed now");  
};  

  
const discardEvent = () => {  
  const form = document.getElementById("event-form");  
  form.dataset.id = null;  
  form.dataset.day = null;  
  form.dataset.index = null;  
  form.style.display = "none";  
  console.log("Form should be hidden now");  
};  





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
      const date = `${year}-${month+1}-${currentDay}`;  
  
      if ((i === 0 && j < firstDay) || currentDay > daysInMonth) {  
        cellWrapper.innerHTML = "";  
      } else {  
        const dayDiv = document.createElement("div");  
        dayDiv.className = "day";  
        dayDiv.innerHTML = currentDay;  
  
        cellWrapper.onclick = (event) => selectDate(currentDay, event);  
  
        if (events[date]) {  
          events[date].forEach((event, index) => {  
            const eventDiv = document.createElement("div");  
            const tooltipDiv = document.createElement("div");  
            tooltipDiv.className = 'tooltip';  
            tooltipDiv.innerHTML = `  
              <strong>${event.name}</strong><br>  
              ${event.startTime} - ${event.endTime}<br>  
              ${event.description}  
            `;  
  
            eventDiv.className = "event";  
            eventDiv.style.backgroundColor = event.color;  
            eventDiv.innerHTML = `${event.name} <span>${event.startTime} - ${event.endTime}</span>`;  
            eventDiv.title = event.description;  
  
            eventDiv.onclick = (e) => {  
              e.stopPropagation();  
              editEvent(date, index);  
            };  
  
            eventDiv.onmouseover = (e) => {  
              tooltipDiv.style.left = `${e.pageX + 10}px`;  
              tooltipDiv.style.top = `${e.pageY + 10}px`;  
              tooltipDiv.style.display = 'block';  
            };  
  
            eventDiv.onmouseout = () => {  
              tooltipDiv.style.display = 'none';  
            };  
  
            cellWrapper.appendChild(eventDiv);  
            document.body.appendChild(tooltipDiv);  // Append tooltip to the body  
          });  
        }  
  
        cell.appendChild(dayDiv);  
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


// Function to go to the next month  
const nextMonth = () => {  
  let date = new Date(currentYear, currentMonth + 1); // This will give you the next month  
  currentYear = date.getFullYear();  
  currentMonth = date.getMonth();  
  generateCalendar(currentYear, currentMonth);  
}  
  
// Function to go to the previous month  
const prevMonth = () => {  
  let date = new Date(currentYear, currentMonth - 1); // This will give you the previous month  
  currentYear = date.getFullYear();  
  currentMonth = date.getMonth();  
  generateCalendar(currentYear, currentMonth);  
}  
  
const changeMonth = (selectedMonth) => {  
  currentMonth = parseInt(selectedMonth);  
  generateCalendar(currentYear, currentMonth);  
};  
  
const changeYear = (selectedYear) => {  
  currentYear = parseInt(selectedYear);  
  generateCalendar(currentYear, currentMonth);  
};  



$(document).ready(() => {  
  setTimeout(() => {  
    fetchEvents();  
    generateCalendar();  
      
    const yearSelect = document.getElementById("year-select");  
    const currentYear = new Date().getFullYear();  
    for(let i = currentYear - 10; i <= currentYear + 10; i++) {  
      const option = document.createElement("option");  
      option.value = i;  
      option.innerHTML = i;  
      yearSelect.appendChild(option);  
    }  
  
    // Set the selected month and year to the current month and year  
    document.getElementById("month-select").value = currentMonth;  
    yearSelect.value = currentYear;  
  }, 1000); // Wait for 1 second before fetching events and populating years  
});  



document.addEventListener("click", function(event) {
  const form = document.getElementById("event-form");
  if (!form.contains(event.target) && form.style.display === "block") {
    discardEvent();
  }
})