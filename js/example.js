var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoia2Jyb3NlIiwiYSI6ImNpZ2tkMWZsZjAwcHR0aGx1czF3b2tlcW4ifQ.pRcu7EvRQ7fihsmQcXK9jA'
}).addTo(map);

var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);

var polygon = L.polygon([
    [51.509, -0.08],
    [51.503, -0.10]
]).addTo(map);

var latlngs = [
    [51.509, -0.08],
    [51.503, -0.12]
]

var polyline = L.polyline(latlngs, {
    color: 'red', weight: 1, fillOpacity: 1, opacity: 1
}).addTo(map);
