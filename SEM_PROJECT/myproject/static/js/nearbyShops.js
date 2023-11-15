// function observeCards() {
//     // Create a new intersection observer 
//     var observer = new IntersectionObserver(function (entries) {
//         // Loop through the entries 
//         for (var entry of entries) {
//             // Check if the entry is intersecting 
//             if (entry.isIntersecting) {
//                 // Add the highlight class to the entry target 
//                 entry.target.classList.add("highlight");
//                 // Remove the highlight class after 3 seconds 
//                 setTimeout(function () { entry.target.classList.remove("highlight"); }, 3000);
//             }
//         }
//     });

//     // Get all the card elements 
//     var cards = document.querySelectorAll(".card");

//     // Loop through the card elements 
//     for (var card of cards) {
//         // Observe each card element 
//         observer.observe(card);
//     }
// }


function createPlaceRow(place) {
    console.log(place)
    var container = document.getElementById("container");
    var row = container.querySelector(".row");
    var col = document.createElement("div");
    col.className = "col";
    var card = document.createElement("div");
    console.log(`PlaceId: ${place.place_id}`)

    card.setAttribute("data_place_id", place.place_id); // Set the data-place-id attribute
    console.log(`Card's PlaceID: ${card.getAttribute("data_place_id")}`)
    card.className = "card h-100";
    var img = document.createElement("img");
    img.className = "card-img-top";
    if (place.photos) {
        let photoUrl = place.photos[0].getUrl();
        img.src = photoUrl;
    } else {
        let photoUrl = "https://via.placeholder.com/150";
        img.src = photoUrl;
    }
    var cardBody = document.createElement("div");
    cardBody.className = "card-body";
    var cardTitle = document.createElement("h5");
    cardTitle.className = "card-title";
    cardTitle.innerHTML = place.name;
    var cardText = document.createElement("p");
    cardText.className = "card-text";
    card.className = "card-hghlght card h-100";
    cardText.innerHTML = place.formatted_address;
    // Create a link element with the Google Maps URL
    var link = document.createElement("a");
    link.className = "card-link";
    // Use the place ID and name properties to construct the URL
    link.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place.name)}&query_place_id=${place.place_id}`;
    link.target = "_blank"; // Open the link in a new tab
    link.innerHTML = "See on Google Maps"; // Set the link text
    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(link); // Append the link element
    card.appendChild(img);
    card.appendChild(cardBody);
    col.appendChild(card);
    row.appendChild(col);

    // Call the function when you need it 
    // observeCards();
}


// Define a function that creates the map and the marker 
function createMapAndMarker(lat, lng) {
    // Create the map with the given center 
    map = new google.maps.Map(document.getElementById("map"), {
        mapId: "9a2c6f65f5f9e6e1",
        //9a2c6f65f5f9e6e1 fcbdee3387b3fdb8 
        center: { lat: lat, lng: lng },
        zoom: 15,
        mapTypeControl: false,
        fullscreenControl: false,
        streetViewControl: false
    });
    // Add a marker to the given location
    new google.maps.Marker({
        position: { lat: lat, lng: lng },
        map,
        title: "My Location",
        // icon: {
        //     url: "bike_icon.svg",
        //     scaledSize: new google.maps.Size(38, 31)
        // },
        animation: google.maps.Animation.DROP
    });

    // Create a request object for the text search
    var request = {
        location: { lat: lat, lng: lng },
        radius: 5000, // Search within 5 km radius
        query: "nearby cycle repair shop" // Search for bike repair shops
    };

    // Create a service object to perform the text search
    var service = new google.maps.places.PlacesService(map);

    // Call the textSearch method with the request and a callback function
    service.textSearch(request, function (results, status) {
        // Check if the status is OK
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            console.log(results)
            // Loop through the results array
            for (var i = 0; i < results.length; i++) {
                // Create a marker for each result
                var marker = new google.maps.Marker({
                    position: results[i].geometry.location,
                    map,
                    title: results[i].name,
                    //label: results[i].place_id,
                    label: "", // keeping marker text empty
                    icon: {
                        //url: "http://localhost:8080/bike_icon.svg",
                        url: "/static/images/bike_icon.svg",
                        scaledSize: new google.maps.Size(38, 31)
                    }
                });
                // Add a click event listener to each marker
                google.maps.event.addListener(marker, "click", function () {
                    // Get the place ID of the clicked marker
                    var placeId = this.label;
                    console.log(placeId);
                    console.log(this);
                    console.log(marker)
                    // Get the card element that matches the place ID
                    var card = document.querySelector(`.card[data_place_id="${placeId}"]`);
                    console.log(card);
                    // Scroll to the card element
                    card.scrollIntoView({ behavior: "smooth", block: "center" });
                });
            }

            for (var i = 0; i < results.length; i++) {
                console.log(results[i].name)
                createPlaceRow(results[i]);
            }
        }
    });
}
function initMap() {
    // Check if the user has given location permission 
    if (navigator.geolocation) {
        // Get the current position of the user 
        navigator.geolocation.getCurrentPosition(function (position) {
            // Call the function with the user’s location 
            createMapAndMarker(position.coords.latitude, position.coords.longitude);
        });
    }
    else {
        // Call the function with the default location 
        createMapAndMarker(28.36067763111428, 75.58666690903469);
    }

    // Call the function when you need it
    // observeCards();
}

window.initMap = initMap;
