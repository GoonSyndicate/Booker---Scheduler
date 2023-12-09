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
    response.forEach(([id, EventType, Start_Date, End_Date, Start_Time, End_Time, Event_Name, Description, Color, Availability, User_ID, Items]) => {  
      if (!events[Start_Date]) events[Start_Date] = [];  
      events[Start_Date].push({ id, EventType, Start_Date, End_Date, Start_Time, End_Time, Event_Name, Description, Color, Availability, User_ID, Items });  
    });    
    generateCalendar();  
  });  
};  
  



const saveEvent = () => {
  const form = document.getElementById("event-form");
  const data = {
    EventType: 'Event',
    Start_Date: document.getElementById("event-date").value,  // Set based on the new input field
    End_Date: document.getElementById("event-date").value,  // Assuming the end date is the same as the start date
    Start_Time: document.getElementById("event-start-time").value,
    End_Time: document.getElementById("event-end-time").value,
    Event_Name: document.getElementById("event-name").value.trim(),
    Description: document.getElementById("event-description").value.trim(),
    Color: document.querySelector('input[name="event-color"]:checked').value,
    Availability: 'Available',  // This can be updated based on your requirements
    User_ID: null,  // This can be updated based on the user who is logged in
    Items: null  // This can be updated if you have items to associate with the event
  };

  // Field Validation
  if (!data.Event_Name || !data.Start_Time || !data.End_Time || !data.Description || !data.Color) {
    alert("All fields are required");
    return;
  }

  // Time Bounds Check
  if (data.Start_Time > "23:59" || data.End_Time > "23:59" || data.Start_Time < "00:00" || data.End_Time < "00:00") {
    alert("Invalid time");
    return;
  }

  console.log("Data being sent to server: ", data);

  const url = "http://localhost:5000/add_event";
  const method = "POST";

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
  form.dataset.date = date;
  form.dataset.index = index;
  
  // Populate the new date field
  document.getElementById("event-date").value = date;
  
  document.getElementById("event-name").value = event.Event_Name;
  document.getElementById("event-start-time").value = event.Start_Time;
  document.getElementById("event-end-time").value = event.End_Time;
  document.querySelector(`input[name="event-color"][value="${event.Color}"]`).checked = true;
  document.getElementById("event-description").value = event.Description;
  
  document.getElementById("form-title").textContent = "Edit Event";
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


// script.js

const generateCalendar = (year = currentYear, month = currentMonth) => {  
  const tbody = document.getElementById("calendar-body");  
  tbody.innerHTML = "";  
  
  const firstDay = new Date(year, month, 1).getDay();  
  const daysInMonth = new Date(year, month + 1, 0).getDate();  
  
  for (let i = 0; i < 5; i++) {  
    const row = document.createElement("tr");  
  
    for (let j = 0; j < 7; j++) {  
      const cell = document.createElement("td");  
      
      // Add class to cell based on day of the week
      if (j === 0 || j === 6) {
        cell.classList.add("weekend");
      } else {
        cell.classList.add("weekday");
      }
      
      const cellWrapper = document.createElement("div");  
      cellWrapper.className = "cell-wrapper";  
  
      let currentDay = i * 7 + j - firstDay + 1;  
      let displayMonth = month;  
      let displayYear = year;  
  
      // If the day number is less than 1, get the last few days of the previous month  
      if (currentDay < 1) {  
        displayMonth--;  
        if (displayMonth < 0) {  
          displayMonth = 11;  
          displayYear--;  
        }  
        const prevMonthDays = new Date(displayYear, displayMonth + 1, 0).getDate();  
        currentDay += prevMonthDays;  
      }  
  
      // If the day number is greater than the number of days in the month, get the first few days of the next month  
      else if (currentDay > daysInMonth) {  
        currentDay -= daysInMonth;  
        displayMonth++;  
        if (displayMonth > 11) {  
          displayMonth = 0;  
          displayYear++;  
        }  
      }  
  
      const date = `${displayYear}-${displayMonth+1}-${currentDay}`;  
  
      if ((i === 0 && j < firstDay) || currentDay > daysInMonth) {  
        cellWrapper.innerHTML = "";  
      } else {  
        const dayDiv = document.createElement("div");  
        dayDiv.className = "day";  
        dayDiv.innerHTML = currentDay;  
  
        // Add a class to the dayDiv if the day is not in the current month  
        if (displayMonth !== month) {  
          dayDiv.classList.add("other-month");  
        }  
  
        // Add a class to the dayDiv if the day is a weekend day  
        if (j === 0 || j === 6) {  
          dayDiv.classList.add("weekend-day");  
        }  
  
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
            eventDiv.innerHTML = `${event.name}`;  
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
  fetchEvents();
}  
  
// Function to go to the previous month  
const prevMonth = () => {  
  let date = new Date(currentYear, currentMonth - 1); // This will give you the previous month  
  currentYear = date.getFullYear();  
  currentMonth = date.getMonth();  
  generateCalendar(currentYear, currentMonth);  
  fetchEvents();
}  
  
const changeMonth = (selectedMonth) => {  
  currentMonth = parseInt(selectedMonth);  
  generateCalendar(currentYear, currentMonth);  
  fetchEvents();
};  
  
const changeYear = (selectedYear) => {  
  currentYear = parseInt(selectedYear);  
  generateCalendar(currentYear, currentMonth);  
  fetchEvents();
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

// Toggle between event and booking forms
const toggleForms = (showBooking = false) => {
  document.getElementById('event-form').style.display = showBooking ? 'none' : 'block';
  document.getElementById('booking-form').style.display = showBooking ? 'block' : 'none';
};

// Function to book a craft
const bookCraft = () => {
  toggleForms(true);  // Show the booking form
  // TODO: populate the booking form fields if needed
};

// Function to confirm a booking
const confirmBooking = () => {
  // Validate and gather form data
  const craftType = document.getElementById('craft-type').value;
  const startDate = document.getElementById('start-date').value;
  const endDate = document.getElementById('end-date').value;
  const passengerCount = document.getElementById('passenger-count').value;
  const canText = document.getElementById('can-text').value;
  const lifeJacketSizes = document.getElementById('life-jacket-sizes').value;
  const additionalAccessories = Array.from(document.querySelectorAll('input[name="additional-accessories"]:checked')).map(el => el.value);

  // Perform validations
  if (!craftType || !startDate || !endDate || !passengerCount || !canText || !lifeJacketSizes) {
    alert('All fields are required');
    return;
  }

  // Send booking data to the server
  const data = {
    craftType,
    startDate,
    endDate,
    passengerCount,
    canText,
    lifeJacketSizes,
    additionalAccessories: JSON.stringify(additionalAccessories)
  };
  
  $.post('http://localhost:5000/book', data, function(response) {
    // Handle server response
    if (response.status === 'success') {
      fetchEvents();  // Refresh the events if needed
      toggleForms(false);  // Hide the booking form
    } else {
      alert('Booking failed: ' + response.reason);
    }
  });
};

// Function to discard a booking instead of saving it, prompting the user to confirm.
const discardBooking = () => {
  if (confirm('Are you sure you want to discard the booking?')) {
    // Reset form fields
    document.getElementById('craft-type').value = '';
    document.getElementById('start-date').value = '';
    document.getElementById('end-date').value = '';
    document.getElementById('passenger-count').value = '';
    document.getElementById('can-text').value = 'yes';
    document.getElementById('life-jacket-sizes').value = '';
    const additionalAccessories = Array.from(document.querySelectorAll('input[name="additional-accessories"]'));
    additionalAccessories.forEach((accessory) => {
      accessory.checked = false;
    });
    // Hide the booking form
    toggleForms(false);
  }
};