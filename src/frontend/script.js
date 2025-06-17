const map = L.map('map').setView([-12.25, -38.95], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let userMarker = null;
let floodMarkers = [];

map.on('click', function (e) {
  const { lat, lng } = e.latlng;
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

  const year = parseInt(document.getElementById('year').value);
  const month = parseInt(document.getElementById('month').value);


  const lat = parseFloat(parseFloat(document.getElementById('lat').value).toFixed(2));
  const lon = parseFloat(parseFloat(document.getElementById('lon').value).toFixed(2));

  const response = await fetch('https://api-weathered-dew-6668.fly.dev/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      lat: parseFloat(lat),
      lon: parseFloat(lon),
      year,
      month
    })
  });

  const data = await response.json();

  if (response.ok) {
    document.getElementById('result').innerText =
      data.predicted_flood
        ? "⚠️ Alagamento previsto neste ponto." 
        : "✅ Sem alagamento previsto neste ponto.";
  } else {
    document.getElementById('result').innerText = `❌ Erro: ${data.detail || "Desconhecido"}`;
  }
});
