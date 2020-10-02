function initMap(){
  let options = {
      zoom: 4,
      center: {lat: 41.8781, lng: -87.6298}
  }
  let map = new google.maps.Map(document.getElementById('map'), options);

  const image = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";
  
  // function addMarker(coords) {
  //     let marker = new google.maps.Marker({
  //         position: {
  //             lat: coords['lat'],
  //             lng: coords['lng'],
  //         },
  //         map,
  //         icon: image
  //     })
  // }

  // let results = document.getElementById('restaurants').value;
  // let parsedResults = JSON.parse(results);

  // parsedResults.forEach(res => {
  //     let coords = {
  //         "lat": parseFloat(res['latitude']),
  //         "lng": parseFloat(res['longitude']),
  //     }
  //     addMarker(coords);
  // });
}