


$(document).ready(function () {



function initialize() {
        var input = document.getElementById('user-location');
        var autocomplete = new google.maps.places.Autocomplete(input);
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            var place = autocomplete.getPlace();
        	console.log(place);
        	userLat = place.geometry.location.k;
        	userLon = place.geometry.location.B;
        	// userLon = userLon + ''
        	// userLat = userLat + ''

        	console.log(userLat)
        	console.log(userLon)

        	var userLocation = userLat + "," + userLon
        	console.log(userLocation)
        	return userLocation
        	debugger
        	// console.log(userLocation)
            // document.getElementById('cityLat').value = place.geometry.location.lat();
            // document.getElementById('cityLng').value = place.geometry.location.lng();
            // alert("This function is working!");
            // alert(place.name);
       

        });
    }
    google.maps.event.addDomListener(window, 'load', initialize); 
	// this allows google autocomplete to display

	$(".typeahead").typeahead({
		minLength: 2,
		highlight: true,
	},
	{
		source: initialize,
		displayKey: 'description',
	});

	// this creates event listener for location form

	// $("#user-preferences-form").submit(searchForSpot);
});

// function for autocomplete from google autocomplete

// function getSuggestions(query, cb) {

// 	var service = new google.maps.places.AutocompleteService();
// 	service.getQueryPredictions({ input: query }, function(predictions, status) {
// 		if (status != google.maps.places.PlacesServiceStatus.OK) {
// 			alert(status);
// 			return;
// 		}
// 		console.log(predictions);
// 		return cb(predictions);

// 	});

	
// }

$("#submit-button").submit(console.log("click!"));
