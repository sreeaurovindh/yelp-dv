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

var showOnMap = function (response) {
  var data = response['data'];

  infowindow = new google.maps.InfoWindow();

  var markers = data.map(function (business, i) {
    var marker = new google.maps.Marker({
      position: business['location'],
      label: business['name'].charAt(0)
    });

    marker.addListener('click', function () {
      infowindow.setContent('<div><b>' + business['name'] + '</b></div><div>' + business['address'] + '</div><div>Rating: <b>' + business['stars'] + '</b> stars</div>');
      infowindow.open(map, marker);
      getUserListForBusiness(business['business_id']);
    });

    return marker;
  });

  var markerCluster = new MarkerClusterer(map, markers,
    { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
}

var getUserListForBusiness = function (businessid) {
  $.ajax({
    type: "GET",
    url: baseurl + "/getdata/userlistbybusinessid/" + businessid,
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(response) {
      populateUserList(response, businessid);
    },
    error: function (xhr, textStatus, errorMessage) {
      console.log(errorMessage);
    }
  });
}

var populateUserList = function (response, businessid) {
  var data = response['data'];
  var content = "";
  for (user in data) {
    content += '<a href="#"><div style="padding-left: 40px; font-size: larger; font-weight: bold;" '
    +'onclick="populateRestaurantRecommendation(\''+businessid+'\',\''+ data[user]['user_id'] + '\')">' + data[user]['name'] + '</div></a><hr>'
  }

  $('.review-user-list').html(content);
}

