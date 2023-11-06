var map;
var currentAction;
var markerForm = document.getElementById('markerForm');
var nameField = document.getElementById('name');

function showMapToolbar() {
  var toolbar = document.getElementById('map_toolbar');
  toolbar.style.display = 'block';
}

function hideMapToolbar() {
  var toolbar = document.getElementById('map_toolbar');
  toolbar.style.display = 'none';
  hideMarkerForm();
}

function hideMarkerForm() {
  markerForm.style.display = 'none';
  nameField.value = '';
  document.getElementById('latitude').value = '';
  document.getElementById('longitude').value = '';
}

function showMarkerForm() {
  markerForm.style.display = 'block';
  if (currentAction === 'addPlaceToHike' || currentAction === 'addHikedPlace') {
    nameField.style.display = 'block';
  } else {
    nameField.style.display = 'none';
  }
}

function addHikedPlace() {
  currentAction = 'addHikedPlace';
  showMarkerForm();
}

function removeHikedPlace() {
  currentAction = 'removeHikedPlace';
  showMarkerForm();
}

function addPlaceToHike() {
  currentAction = 'addPlaceToHike';
  showMarkerForm();
}

function removePlaceToHike() {
  currentAction = 'removePlaceToHike';
  showMarkerForm();
}

function confirmMarker() {
  var name = nameField.value;
  var latitude = parseFloat(document.getElementById('latitude').value);
  var longitude = parseFloat(document.getElementById('longitude').value);
  if (!isNaN(latitude) && !isNaN(longitude)) {
    var coordinates = {
      name: name,
      latitude: latitude,
      longitude: longitude,
      action: currentAction
    };
    $.ajax({
      url: '/handle_map_marker',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(coordinates),
      success: function(response) {
        console.log('Marker action successful');
      },
      error: function(error) {
        console.error('Failed to handle marker');
      }
    });
  }
  hideMarkerForm();
}

function cancelMarker() {
  hideMarkerForm();
}

// Wait for the DOM content to load
$(document).ready(function() {
  // Set your Mapbox access token here
  mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzdWFsbWFwcGVyIiwiYSI6ImNsaXF3aHl4dDBpNTkzZHF2ODE5OTRuMXkifQ.WbZiBSY4DWHNi9GtOxFJ9g';
  // Initialize the map
  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-71.305000, 44.271000],
    zoom: 1
  });
});
