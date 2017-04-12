var map;
var infowindow;

function initMap() {
  var us_location = { lat: 38.967714, lng: -103.104248 };
  map = new google.maps.Map(document.getElementById('world-map'), {
    zoom: 3,
    center: us_location,
    mapTypeControl: false,
    disableDefaultUI: true,
  });
}

var getBusinessData = function (location_type, location) {
  $.ajax({
    type: "GET",
    url: baseurl + "/getdata/business/locationtype/" + location_type + "/location/" + location,
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: showOnMap,
    error: function (xhr, textStatus, errorMessage) {
      console.log(errorMessage);
    }
  });
}

var showOnMap = function (result) {
  var data = result['data'];

  infowindow = new google.maps.InfoWindow();

  var markers = data.map(function (business, i) {
    var marker = new google.maps.Marker({
      position: business['location'],
      label: business['name'].charAt(0)
    });

    marker.addListener('click', function () {
      infowindow.setContent('<div><b>' + business['name'] + '</b></div><div>' + business['address'] + '</div><div>Rating: ' + business['stars'] + ' stars</div>');
      infowindow.open(map, marker);
    });

    return marker;
  });

  var markerCluster = new MarkerClusterer(map, markers,
    { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
}


