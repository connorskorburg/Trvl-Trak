function initMap(){
    const trips = document.getElementById('trips').value;
    const parsedResults = JSON.parse(trips);
    let options = {
        zoom: 4,
        center: {lat: 41.8781, lng: -87.6298}
    }
    let map = new google.maps.Map(document.getElementById('map'), options);


    const addInfo = (coords, content) => {
        const marker = new google.maps.Marker({
            position: {
                lat: coords['lat'],
                lng: coords['lng'],
            },
            map,
        })

        const infoWindow = new google.maps.InfoWindow({
            content: content,
        })

        infoWindow.open(map, marker);

        marker.addListener('click', ()=> {
            infoWindow.open(map, marker);
        })
    }
    if(parsedResults.length === 0) {
        return false
    } else {
        parsedResults.forEach(res => {
            let coords = {
                "lat": parseFloat(res['latitude']),
                "lng": parseFloat(res['longitude']),
            }
            const ul = document.createElement('ul');
            const title = document.createElement('h3');
            const address = document.createElement('li');
            const date = document.createElement('li');
            title.textContent = res['title'];
            address.textContent = res['address'];
            date.textContent = `${res['trip_start']}-${res['trip_end']}`;
            ul.appendChild(title);
            ul.appendChild(address);
            ul.appendChild(date);
            addInfo(coords, ul)
        });
    }
}