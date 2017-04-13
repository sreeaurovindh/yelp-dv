var map;
var infowindow;

var mapStyles = {
  default: null,
  retro: [
    {elementType: 'geometry', stylers: [{color: '#ebe3cd'}]},
    {elementType: 'labels.text.fill', stylers: [{color: '#523735'}]},
    {elementType: 'labels.text.stroke', stylers: [{color: '#f5f1e6'}]},
    {
      featureType: 'administrative',
      elementType: 'geometry.stroke',
      stylers: [{color: '#c9b2a6'}]
    },
    {
      featureType: 'administrative.land_parcel',
      elementType: 'geometry.stroke',
      stylers: [{color: '#dcd2be'}]
    },
    {
      featureType: 'administrative.land_parcel',
      elementType: 'labels.text.fill',
      stylers: [{color: '#ae9e90'}]
    },
    {
      featureType: 'landscape.natural',
      elementType: 'geometry',
      stylers: [{color: '#dfd2ae'}]
    },
    {
      featureType: 'poi',
      elementType: 'geometry',
      stylers: [{color: '#dfd2ae'}]
    },
    {
      featureType: 'poi',
      elementType: 'labels.text.fill',
      stylers: [{color: '#93817c'}]
    },
    {
      featureType: 'poi.park',
      elementType: 'geometry.fill',
      stylers: [{color: '#a5b076'}]
    },
    {
      featureType: 'poi.park',
      elementType: 'labels.text.fill',
      stylers: [{color: '#447530'}]
    },
    {
      featureType: 'road',
      elementType: 'geometry',
      stylers: [{color: '#f5f1e6'}]
    },
    {
      featureType: 'road.arterial',
      elementType: 'geometry',
      stylers: [{color: '#fdfcf8'}]
    },
    {
      featureType: 'road.highway',
      elementType: 'geometry',
      stylers: [{color: '#f8c967'}]
    },
    {
      featureType: 'road.highway',
      elementType: 'geometry.stroke',
      stylers: [{color: '#e9bc62'}]
    },
    {
      featureType: 'road.highway.controlled_access',
      elementType: 'geometry',
      stylers: [{color: '#e98d58'}]
    },
    {
      featureType: 'road.highway.controlled_access',
      elementType: 'geometry.stroke',
      stylers: [{color: '#db8555'}]
    },
    {
      featureType: 'road.local',
      elementType: 'labels.text.fill',
      stylers: [{color: '#806b63'}]
    },
    {
      featureType: 'transit.line',
      elementType: 'geometry',
      stylers: [{color: '#dfd2ae'}]
    },
    {
      featureType: 'transit.line',
      elementType: 'labels.text.fill',
      stylers: [{color: '#8f7d77'}]
    },
    {
      featureType: 'transit.line',
      elementType: 'labels.text.stroke',
      stylers: [{color: '#ebe3cd'}]
    },
    {
      featureType: 'transit.station',
      elementType: 'geometry',
      stylers: [{color: '#dfd2ae'}]
    },
    {
      featureType: 'poi.business',
      stylers: [{visibility: 'off'}]
    },
    {
      featureType: 'transit',
      elementType: 'labels.icon',
      stylers: [{visibility: 'off'}]
    },
    {
      featureType: 'water',
      elementType: 'geometry.fill',
      stylers: [{color: '#b9d3c2'}]
    },
    {
      featureType: 'water',
      elementType: 'labels.text.fill',
      stylers: [{color: '#92998d'}]
    }
  ]
};

function initMap() {
  var us_location = { lat: 38.967714, lng: -103.104248 };
  map = new google.maps.Map(document.getElementById('world-map'), {
    zoom: 3,
    center: us_location,
    mapTypeControl: false,
    disableDefaultUI: true
  });
  map.setOptions({styles: mapStyles["retro"]});
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
      paracoordOnTrigger(business['business_id']);
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

