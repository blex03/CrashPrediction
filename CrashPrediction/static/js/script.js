let map;
let latitude = 0;
let longitude = 0;
let cityName;


navigator.geolocation.getCurrentPosition(function(position) {
    latitude = position.coords.latitude;
    const latitudeEvent = new CustomEvent('latitudeUpdated', { detail: latitude });
    document.dispatchEvent(latitudeEvent);
});

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const mapId = '20c0f793a946419e';
  map = new Map(document.getElementById("map"), {
    center: { lat:41.562794, lng:-72.681610 },
    zoom: 8.5,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: false,
    mapId: mapId
  });

  map.addListener('click', function(event) {
    latitude = event.latLng.lat();
    longitude = event.latLng.lng();
    console.log('Clicked latitude:', latitude);
    console.log('Clicked longitude:', longitude);
    getTownCityName(event.latLng);
    updateMarker(event.latLng); // Update marker position
  });

  let marker;
  
  function updateMarker(latLng) {
    // Remove existing marker if present
    if (marker) {
      marker.setMap(null);
    }
    
    // Create new marker at the clicked location
    marker = new AdvancedMarkerElement({
      map: map,
      position: latLng
    });
  }
}

async function getTownCityName(latLng) {
    const geocoder = new google.maps.Geocoder();
    
    try {
      const response = await new Promise((resolve, reject) => {
        geocoder.geocode({ location: latLng }, (results, status) => {
          if (status === 'OK' && results[0]) {
            resolve(results[0]);
          } else {
            reject(new Error('Geocoder failed'));
          }
        });
      });
  
      cityName = response.address_components.find(component =>
        component.types.includes('locality')
      ).long_name;
  
      console.log('Town/City Name:', cityName);
    } catch (error) {
      console.error('Error:', error.message);
    }
}

initMap();

document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Retrieve the selected date, time, and day from the form
    const time = document.getElementById('timeInput').value;
    const date = document.getElementById('dateInput').value;
    const day = document.getElementById('dayInput').value;
    const weather = document.getElementById('weatherInput').value;
    const light = document.getElementById('lightInput').value;
    const street = document.getElementById('streetInput').value;
  
    // Log the selected date, time, and day to the console
    console.log('Selected Time:', time);
    console.log('Selected Date:', date);
    console.log('Selected Day:', day);
    console.log('Selected Weather:', weather);
    console.log('Selected Light Condition:', light);
    console.log('Selected Street:', street);
    console.log('Latitude:', latitude);
    console.log('Longitude:', longitude);
    console.log('City:', cityName)

    const formData = {
      time: time,
      date: date,
      day: day,
      weather: weather,
      light: light,
      street: street,
      city: cityName,
      longitude: longitude,
      latitude: latitude
    };

    // Send the form data to Flask using AJAX
    $.ajax({
        url: '/submit-form',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            // Data sent successfully
            console.log('Form data sent successfully');
            var resultAssignment = response.assignment;
            
            printResult(resultAssignment);
      
        },
        error: function(error) {
            // Error handling
            console.error('Failed to send form data:', error);
        }
    });

function printResult(resultAssignment){
  console.log("printing");

    // Get the result paragraph element
    var resultParagraph = resultsComponent.querySelector("p");

    // If resultParagraph does not exist, create it
    if (!resultParagraph) {
        // Create resultHeader and resultParagraph elements
        var resultHeader = document.createElement("h1");
        resultHeader.textContent = "Results";

        resultParagraph = document.createElement("h2");

        // Append resultHeader and resultParagraph to resultsComponent
        resultsComponent.appendChild(resultHeader);
        resultsComponent.appendChild(resultParagraph);
    }

    // Update the content of the resultParagraph with new resultDate
    resultParagraph.textContent = "Assignment =  " + resultAssignment;

    // Toggle the visibility of the results component based on resultDate
    resultsComponent.style.display = "block";
    
  
}
    
  
    // Here you can store the date, time, and day in variables, or perform any further actions
});