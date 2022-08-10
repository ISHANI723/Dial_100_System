// Initialize and add the map
function initMap() {
    // The location of AISSMS, COE, Pune (18.531292158030173, 73.86560585260511)
    const center = { lat: 18.531292158030173, lng: 73.86560585260511 };
    // The map, centered at center
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: center,
    });
    // The marker, positioned at center
    const marker = new google.maps.Marker({
        position: center,
        map: map,
    });
}

window.initMap = initMap;
