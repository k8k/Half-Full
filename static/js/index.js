// window.onload = function() {
//   var startPos;
//   var geoSuccess = function(position) {
//     startPos = position;
//     document.getElementById('startLat').innerHTML = startPos.coords.latitude;
//     document.getElementById('startLon').innerHTML = startPos.coords.longitude;
//     console.log(position)
//   };
//  navigator.geolocation.getCurrentPosition(geoSuccess);
// };



$("#submit-button").submit(console.log("click!"));
   



$(document).ready(function () {

	// this allows google autocomplete to display

	$(".typeahead").typeahead({
		minLength: 2,
		highlight: true,
	},
	{
		source: getSuggestions,
		displayKey: 'description',
	});

	// this creates event listener for location form

	$("#user-preferences-form").submit(searchForSpot);
});

// function for autocomplete from google autocomplete

function getSuggestions(query, cb) {
	// var defaultBounds = new google.maps.LatLngBounds(
	// 	new google.mapsLatLng(37.420734, -122.628001)
	// 	new google.mapsLatLng(38.169499, -121.889170));
	
	// var options = {
	// 	bounds: defaultBounds
	// };

	var service = new google.maps.places.AutocompleteService();
	service.getQueryPredictions({ input: query }, function(predictions, status) {
		if (status != google.maps.places.PlacesServiceStatus.OK) {
			alert(status);
			return;
		}
		console.log(predictions);
		return cb(predictions, options);

	});

	
}

// function to submit and store variables for locations



// function searchForSpot(evt) {
// 	evt.preventDefault();
// 	console.log("Got here");
// 	var locationOne = $("#location_one");
// 	locationOne = locationOne.val();
// 	console.log(locationOne);
// 	var locationTwo = $("#location_two").val();
// 	console.log("searchForSpot: ", locationOne, locationTwo);
// }


// if (navigator.geolocation) {
//   alert('Geolocation is supported!');
// }
// else {
//   alert('Geolocation is not supported for this Browser/OS version yet.');
// }
