function initMap() {
  var us_location = { lat: 38.967714, lng: -103.104248 };
  var map = new google.maps.Map(document.getElementById('world-map'), {
    zoom: 4,
    center: us_location,
    mapTypeControl: false,
    disableDefaultUI: true,
  });
  var marker = new google.maps.Marker({
    position: us_location,
    map: map
  });
}


