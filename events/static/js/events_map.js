const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

const layer = L.tileLayer(url, { noWrap: true, attribution: copy });

const map = L.map("map", {
	maxBounds: [
		[-90, -180],
		[90, 180],
	],
	layers: [layer],
	minZoom: 2, // Minimum zoom to prevent over-zooming out
}).setView([25, 0], 2.5); // Center the map and initial zoom level

const categoryColors = {
	conference: "#092E20", // green
	local_community: "#44B78B", // accent green
};

function getColorByCategory(category) {
	return categoryColors[category];
}

fetch("/events/api/")
	.then((response) => {
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		return response.json();
	})
	.then((apiData) => renderEvents(apiData))
	.catch(() => {
		L.marker([25, 0]).addTo(map).bindPopup("Error loading event data").openPopup();
	});

function renderEvents(geojsonData) {
	const geojsonLayer = L.geoJSON(geojsonData, {
		pointToLayer: (feature, latlng) => {
			const category = feature.properties.event_category;
			const color = getColorByCategory(category);
			console.log("Category:", category);
			console.log("Color:", color);

			return L.circleMarker(latlng, {
				radius: 8,
				fillColor: color,
				color: "#000",
				weight: 1,
				opacity: 1,
				fillOpacity: 0.8,
			});
		},
		onEachFeature: (feature, layer) => {
			const props = feature.properties;
			const eventDate = new Date(props.date);
			const formattedDate = eventDate.toLocaleDateString("en-US", {
				weekday: "long",
				year: "numeric",
				month: "long",
				day: "numeric",
			});

			layer.bindPopup(`
                <a href="${props.website}" target="_blank"><b>${props.name}</b><br></a>
                <strong>${props.event_category_label}</strong><br>
                ${formattedDate}<br>
                <small>${props.address}</small><br>
            `);
		},
	}).addTo(map);

	// Auto-fit only if there are features
	if (geojsonData.features.length > 0) {
		map.fitBounds(geojsonLayer.getBounds(), {
			padding: [50, 50],
			maxZoom: 16,
		});
	}
}

// Reset view control
L.Control.ResetView = L.Control.extend({
	onAdd: function () {
		const container = L.DomUtil.create("div", "leaflet-bar leaflet-control");
		const button = L.DomUtil.create("a", "leaflet-control-resetview", container);
		button.href = "#";
		button.title = "Reset View";
		button.innerHTML = "↻";
		L.DomEvent.on(button, "click", this._resetView, this);
		return container;
	},

	_resetView: function (e) {
		L.DomEvent.stopPropagation(e);
		L.DomEvent.preventDefault(e);
		this._map.setView([30, 0], 2);
	},
});

L.control.resetView = (opts) => new L.Control.ResetView(opts);

L.control.resetView({ position: "topleft" }).addTo(map);
