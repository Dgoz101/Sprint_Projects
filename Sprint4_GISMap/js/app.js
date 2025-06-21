/**
 * Loads the ArcGIS map, geocodes apartment addresses, adds markers with
 * detailed popups, and provides interactive price/parking filters.  API key comes from js/config.js.
 */
require([
  "esri/config",
  "esri/Map",
  "esri/views/MapView",
  "esri/layers/GraphicsLayer",
  "esri/Graphic",
  "esri/rest/locator"
], function(esriConfig, EsriMap, EsriMapView, EsriGraphicsLayer, EsriGraphic, locator) {

  esriConfig.apiKey = window.AppConfig.apiKey;

  const map = new EsriMap({ basemap: "streets-navigation-vector" });
  const view = new EsriMapView({
    container: "viewDiv",
    map,
    center: [-111.789, 43.825],
    zoom: 13
  });

  const housingLayer = new EsriGraphicsLayer();
  map.add(housingLayer);

  fetch("apartments.json")
    .then(r => r.json())
    .then(items =>
      Promise.all(items.map(item =>
        locator.addressToLocations(
          "https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer",
          {
            address: { SingleLine: item.address },
            maxLocations: 1
          }
        ).then(results => {
          if (!results.length) return null;
          const { x: longitude, y: latitude } = results[0].location;
          return new EsriGraphic({
            geometry: { type: "point", longitude, latitude },
            symbol: {
              type: "simple-marker",
              style: "circle",
              size: 10,
              color: item.parking ? [0,128,0] : [128,0,0]
            },
            attributes: {
              Name:         item.name,
              Address:      item.address,
              Price:        `$${item.price}`,
              Parking:      item.parking ? "Yes" : "No",
              ParkingSpots: item.p_spots,
              Contact:      item.contact
            },
            popupTemplate: {
              title: "{Name}",
              content: `
                <ul>
                  <li><b>Address:</b> {Address}</li>
                  <li><b>Price:</b> {Price}</li>
                  <li><b>On-site Parking:</b> {Parking}</li>
                  <li><b>Parking Spots:</b> {ParkingSpots}</li>
                  <li><b>Contact:</b> {Contact}</li>
                </ul>`
            }
          });
        })
      ))
    )
    .then(graphics => {
      graphics.filter(g => g).forEach(g => housingLayer.add(g));
      setupFilters();
    })
    .catch(console.error);

  function setupFilters() {
    const priceSlider     = document.getElementById("priceSlider");
    const parkingCheckbox = document.getElementById("parkingCheckbox");
    const priceValue      = document.getElementById("priceValue");

    priceSlider.oninput = () => {
      priceValue.textContent = priceSlider.value;
      applyFilters();
    };
    parkingCheckbox.onchange = applyFilters;

    applyFilters();
  }

  function applyFilters() {
    const maxPrice    = +document.getElementById("priceSlider").value;
    const parkingOnly = document.getElementById("parkingCheckbox").checked;

    housingLayer.graphics.forEach(g => {
      const price   = parseInt(g.attributes.Price.slice(1), 10);
      const parking = g.attributes.Parking === "Yes";
      g.visible     = price <= maxPrice && (!parkingOnly || parking);
    });
  }

});
