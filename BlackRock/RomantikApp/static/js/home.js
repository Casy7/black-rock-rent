mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzeTciLCJhIjoiY2s1aWl5MXV4MGI5dDNvbW41bm82OGpmdyJ9.t3Er5THaXs9H0hH2JSp-Ww';
const map = new mapboxgl.Map({
container: 'map', // container ID
// Choose from Mapbox's core styles, or make your own style with Mapbox Studio
style: 'mapbox://styles/mapbox/streets-v12', // style URL
center: [30.7669, 46.43093], // starting position [lng, lat]
zoom: 13 // starting zoom
});

const marker1 = new mapboxgl.Marker().setLngLat([30.7469, 46.43093]).addTo(map);
 