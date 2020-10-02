function initMap() {
  console.log(document.getElementById('address').value);
  document.getElementById("submit").click()
  const map = new google.maps.Map(document.getElementById("search-map"), {
    zoom: 8,
    center: {lat: 41.8781, lng: -87.6298},
  });

  const geocoder = new google.maps.Geocoder();
  geocodeAddress(geocoder, map);
  
  document.getElementById("submit").addEventListener("click", () => {
    geocodeAddress(geocoder, map);
  });
}

function geocodeAddress(geocoder, resultsMap) {
  const address = document.getElementById("address").value;
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === "OK") {
      console.log(results);
      //create results 
      document.getElementById('address').value = '';
      const content = document.getElementById('results-content');;
      const ul = document.createElement('ul');
      const address = document.createElement('li');
      const lat = document.createElement('li');
      const lng = document.createElement('li');
      const button = document.createElement('button');

      button.textContent = 'Add To Favorites';
      button.addEventListener('click', ()=> {
        console.log('hello');
      })

      address.textContent = `Address: ${results[0].formatted_address}`;

      lat.textContent = `Latitude ${results[0].geometry.location.lat()}`;
      lng.textContent = `Longitude ${results[0].geometry.location.lng()}`;
      ul.appendChild(address);
      ul.appendChild(lng);
      ul.appendChild(lat);
      ul.appendChild(button);
      
      content.appendChild(ul);
      console.log(ul);
      resultsMap.setCenter(results[0].geometry.location);
      const infoWindow = new google.maps.InfoWindow({
        content: ul,
      })
      const marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location,
      });
      infoWindow.open(resultsMap, marker);
      marker.addListener('click', ()=> {
        infoWindow.open(resultsMap, marker);
      })
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}

  //add marker
  // function addMarker(location) {
  //   const marker = new google.maps.Marker({
  //     position: location,
  //     map: map,
  //   });
  //   markers.push(marker);
  // }

  // function deleteMarkers() {
  //   setMapOnAll(null);
  //   markers = [];
  // }
  // function showMarkers() {
  //   setMapOnAll(map);
  // }