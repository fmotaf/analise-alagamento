const map = L.map('map').setView([-12.25, -38.95], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// === On map click, populate coordinates ===
let userMarker = null;

const lat_min = -12.35, lat_max = -12.15, lon_min = -39.10, lon_max = -38.90;

map.on('click', function (e) {
  const { lat, lng } = e.latlng;
  // Only allow points within region of interest
  if (
    lat < lat_min || lat > lat_max ||
    lng < lon_min || lng > lon_max
  ) {
    alert("Selected point is outside the region of interest.");
    return;
  }
  // Use 2 decimal places for grid match
  document.getElementById('lat').value = lat.toFixed(2);
  document.getElementById('lon').value = lng.toFixed(2);

  if (userMarker) {
    userMarker.setLatLng([lat, lng]);
  } else {
    userMarker = L.marker([lat, lng], { color: 'red' }).addTo(map);
  }
});


document.getElementById('flood-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  // Parse as 2 decimal float for API
  const lat = parseFloat(parseFloat(document.getElementById('lat').value).toFixed(2));
  const lon = parseFloat(parseFloat(document.getElementById('lon').value).toFixed(2));
  const year = parseInt(document.getElementById('year').value);
  const month = parseInt(document.getElementById('month').value);

  const response = await fetch('http://localhost:8000/predict/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lat, lon, year, month })
  });

  const data = await response.json();

  console.log(data);

  document.getElementById('result').innerText =
    response.ok
      ? (data.predicted_flood ? "⚠️ Flood predicted" : "✅ No flood expected")
      : `❌ Error: ${data.detail || "Unknown error"}`;
});