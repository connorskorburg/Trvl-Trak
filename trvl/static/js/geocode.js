function initMap() {
  const map = new google.maps.Map(document.getElementById("search-map"), {
    zoom: 5,
    center: { lat: -34.397, lng: 150.644 },
  });
  const geocoder = new google.maps.Geocoder();
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
      const content = document.getElementById('results-content');
      const ul = document.createElement('ul');
      const address = document.createElement('li');
      const lat = document.createElement('li');
      const lng = document.createElement('li');
      address.textContent = `Address: ${results[0].formatted_address}`;
      lng.textContent = `Longitude ${results[0].geometry.bounds.Sa.i}`;
      lat.textContent = `Latitude ${results[0].geometry.bounds.Ya.i}`;
      ul.appendChild(address);
      ul.appendChild(lng);
      ul.appendChild(lat);
      content.appendChild(ul);
      resultsMap.setCenter(results[0].geometry.location);
      new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location,
      });
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}