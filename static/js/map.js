// Wait for the DOM content to load
document.addEventListener("DOMContentLoaded", function() {
  // Set your Mapbox access token here
  mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzdWFsbWFwcGVyIiwiYSI6ImNsaXF3aHl4dDBpNTkzZHF2ODE5OTRuMXkifQ.WbZiBSY4DWHNi9GtOxFJ9g';
  // Initialize the map
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', // You can choose a different map style here
    center: [-71.305000, 44.271000], // Replace with your desired coordinates
    zoom: 1 // Replace with your desired zoom level
  });

  // Add markers for hiked locations
  hikedLocations.forEach(function(location) {
    var el = document.createElement('div');
    el.className = 'marker';
    new mapboxgl.Marker(el)
      .setLngLat(location.coordinates)
      .setPopup(new mapboxgl.Popup().setHTML('<b>' + location.name + '</b><br>Hiked location'))
      .addTo(map);
  });
  // Add markers for desired hike locations
  desiredHikeLocations.forEach(function(location) {
    var el = document.createElement('div');
    el.className = 'marker desired-hike';
    new mapboxgl.Marker(el)
      .setLngLat(location.coordinates)
      .setPopup(new mapboxgl.Popup().setHTML('<b>' + location.name + '</b><br>Desired hike'))
      .addTo(map);
  });
});
