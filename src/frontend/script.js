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

  const latField = document.getElementById('lat');
  const lonField = document.getElementById('lon');
  const year = parseInt(document.getElementById('year').value);
  const month = parseInt(document.getElementById('month').value);

//   const lat = latField.value.trim();
//   const lon = lonField.value.trim();

  const lat = parseFloat(parseFloat(document.getElementById('lat').value).toFixed(2));
  const lon = parseFloat(parseFloat(document.getElementById('lon').value).toFixed(2));

  // === Case A: Show flood map for all points
  if (!lat || !lon) {
    floodMarkers.forEach(marker => map.removeLayer(marker));
    floodMarkers = [];

    const response = await fetch(`https://api-weathered-dew-6668.fly.dev/flood-map?year=${year}&month=${month}`);
    const points = await response.json();

    if (!Array.isArray(points) || points.length === 0) {
      document.getElementById('result').innerText = "✅ Nenhum ponto com alagamento previsto.";
      return;
    }

    points.forEach(({ lat, lon }) => {
      const marker = L.circleMarker([lat, lon], {
        radius: 5,
        color: 'red',
        fillOpacity: 0.8
      }).addTo(map);
      floodMarkers.push(marker);
    });

    document.getElementById('result').innerText = `⚠️ ${points.length} pontos com risco de alagamento.`;
    return;
  }

  // === Case B: Predict flood at specific point
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
