const osm = "https://www.openstreetmap.org/copyright";
const copy = "&copy; <a href='${osm}'>OpenStreetMap</a>";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

const layer = L.tileLayer(url, { noWrap: true, attribution: copy });

const map = L.map("map", {
    maxBounds: [[-90, -180], [90, 180]],
    layers: [layer],
    minZoom: 2, // Minimum zoom to prevent over-zooming out
}).setView([25, 0], 2.5); // Center the map and initial zoom level

fetch('/events/api/')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(apiData => renderEvents(apiData))
    .catch(() => {
        L.marker([25, 0]).addTo(map)
            .bindPopup('Error loading event data')
            .openPopup();
    });


function renderEvents(geojsonData) {
    const geojsonLayer = L.geoJSON(geojsonData, {
        pointToLayer: function(feature, latlng) {
            return L.circleMarker(latlng, {
                radius: 8,
                fillColor: "#092E20",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            });
        },
        onEachFeature: function(feature, layer) {
            const props = feature.properties;
            const eventDate = new Date(props.datetime);
            const formattedDate = eventDate.toLocaleString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                timeZoneName: 'short'
            });

            layer.bindPopup(`
                <b>${props.name}</b><br>
                <small>${formattedDate}</small><br>
                ${props.address}<br>
                <a href="${props.website}" target="_blank">Website</a>
            `);
        }
    }).addTo(map);

    // Auto-fit only if there are features
    if (geojsonData.features.length > 0) {
        map.fitBounds(geojsonLayer.getBounds(), {
            padding: [50, 50],
            maxZoom: 16
        });
    }
}


// Reset view control
L.Control.ResetView = L.Control.extend({
    onAdd: function() {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        const button = L.DomUtil.create('a', 'leaflet-control-resetview', container);
        button.href = '#';
        button.title = 'Reset View';
        button.innerHTML = '↻';
        L.DomEvent.on(button, 'click', this._resetView, this);
        return container;
    },

    _resetView: function(e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);
        this._map.setView([30, 0], 2);
    }
});

L.control.resetView = function(opts) {
    return new L.Control.ResetView(opts);
};

L.control.resetView({position: 'topleft'}).addTo(map);
