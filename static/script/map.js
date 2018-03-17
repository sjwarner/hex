function myMap() {
	var mapProp= {
	    center:new google.maps.LatLng(51.4381039,5.4424674),
	    zoom:7,
	};
	
	var icon = {
    url: "../img/bee.png" , // url
    scaledSize: new google.maps.Size(50, 50), // scaled size
    origin: new google.maps.Point(0,0), // origin
    anchor: new google.maps.Point(0, 0) // anchor
	};

	var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
	var myCenter = new google.maps.LatLng(51.4381039,5.4424674);
	var marker = new google.maps.Marker(
		{
			position: myCenter,
			animation:google.maps.Animation.BOUNCE,
			icon: icon
		});
	marker.setMap(map); 	
	google.maps.event.addListener(marker,'click',function() {
    map.setZoom(12);
    map.setCenter(marker.getPosition());
  	});
	}