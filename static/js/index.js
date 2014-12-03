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

            console.log(userLat);
            console.log(userLon);

            var userLocation = userLat + "," + userLon;
            console.log(userLocation);
            userLocation = userLocation + '';
            // $("#lat_long_from_js").load(userLocation);
            $.ajax({
                type: "GET",
                url: location,
                data: JSON.stringify(userLocation),
                dataType: 'json',
                contentType: 'application/json; charset=utf-8'
            }).done(function(msg) {
                alert("Data Saved:" + msg);
                console.log(msg);
            });



            return userLocation;
            // debugger;
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

});







$(document).ready(function() {
  var menu = $('#navigation-menu');
  var menuToggle = $('#js-mobile-menu');
  var signUp = $('.sign-up');

  $(menuToggle).on('click', function(e) {
    e.preventDefault();
    menu.slideToggle(function(){
      if(menu.is(':hidden')) {
        menu.removeAttr('style');
      }
    });
  });


  // underline under the active nav item
  $(".nav .nav-link").click(function() {
    $(".nav .nav-link").each(function() {
      $(this).removeClass("active-nav-item");
    });
    $(this).addClass("active-nav-item");
    $(".nav .more").removeClass("active-nav-item");
  });
});


$("#submit-button").submit(console.log("click!"));



