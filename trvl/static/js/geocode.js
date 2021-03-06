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
      const content = document.getElementById('results-content');
      // ul elements
      const ul = document.createElement('ul');
      const address = document.createElement('h3');
      const lat = document.createElement('li');
      const lng = document.createElement('li');
      //form elements
      const form = document.createElement('form');
      const addressInput = document.createElement('input');
      const latInput = document.createElement('input');
      const lngInput = document.createElement('input');
      const button = document.createElement('button');
      //set form attributes
      form.setAttribute('action', '/addFav');      
      form.setAttribute('method', 'GET');
      //set input to hidden
      // csrf.setAttribute('type', 'hidden')
      addressInput.setAttribute('type', 'hidden');
      latInput.setAttribute('type', 'hidden');
      lngInput.setAttribute('type', 'hidden');
      //set name attribute
      addressInput.setAttribute('name', 'address')
      latInput.setAttribute('name', 'lat');
      lngInput.setAttribute('name', 'lng');
      //set value attribute
      addressInput.setAttribute('value', results[0].formatted_address);
      latInput.setAttribute('value', results[0].geometry.location.lat());
      lngInput.setAttribute('value', results[0].geometry.location.lng());
      //set button attributes and values
      button.classList.add('fav-btn')
      button.textContent = 'Add to Favorites'
      //append children to form
      form.appendChild(addressInput);
      form.appendChild(latInput);
      form.appendChild(lngInput);
      form.appendChild(button);



      ul.classList.add('ul-result');

      address.textContent = `${results[0].formatted_address}`;

      address.classList.add('title');
      lat.textContent = `Latitude: ${results[0].geometry.location.lat()}`;
      lng.textContent = `Longitude: ${results[0].geometry.location.lng()}`;

      ul.appendChild(address);
      ul.appendChild(lng);
      ul.appendChild(lat);
      ul.appendChild(form);
      
      content.appendChild(ul);
      console.log(ul);

      resultsMap.setCenter(results[0].geometry.location);

      const marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location,
      });

    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
