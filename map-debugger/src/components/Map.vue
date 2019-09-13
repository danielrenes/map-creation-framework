<template>
  <div id="map">
    <div id="map-target"></div>
    <div id="map-controllers">
      <a v-on:click="clearMap" id="clear-map" class="button is-danger is-outlined">Clear</a>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const INGRESS_COLOR = "rgb(255, 0, 0)";
const EGRESS_COLOR = "rgb(0, 0, 255)";

export default {
  name: "Map",
  props: ["intersections"],
  data() {
    return {
      map: null,
      tileLayer: null,
      layers: {}
    };
  },
  methods: {
    initMap: function() {
      this.map = new L.map("map-target").setView([47.476123, 19.053197], 16);
      this.tileLayer = new L.TileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
          minZoom: 8,
          maxZoom: 18,
          attribution:
            'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
        }
      );

      this.tileLayer.addTo(this.map);
    },

    createMarker: function(info, layerGroup) {
      if (typeof info === "object" && "refPoint" in info) {
        const latlng = new L.LatLng(
          info.refPoint.latitude,
          info.refPoint.longitude
        );
        const marker = new L.marker(latlng);
        layerGroup.addLayer(marker);
      }
    },

    drawPolylines: function(connections, layerGroup) {
      for (const i in connections) {
        const connection = connections[i];
        this.drawConnection(connection, layerGroup);
      }
    },

    drawConnection: function(connection, layerGroup) {
      const ingress = connection.ingress;
      const egress = connection.egress;

      const ingressPolyline = this.drawPolyline(
        ingress,
        INGRESS_COLOR,
        layerGroup
      );
      const egressPolyline = this.drawPolyline(
        egress,
        EGRESS_COLOR,
        layerGroup
      );

      this.addPolylineHoverEventHandler(ingressPolyline, egressPolyline);
      this.addPolylineHoverEventHandler(egressPolyline, ingressPolyline);
    },

    addPolylineHoverEventHandler: function(polyline1, polyline2) {
      polyline1.on("mouseover", function(e) {
        polyline2.setStyle({ weight: 12 });
      });

      polyline1.on("mouseout", function(e) {
        polyline2.setStyle({ weight: 8 });
      });
    },

    drawPolyline: function(points, color, layerGroup) {
      if (!points) {
        return;
      }

      const coordinates = [];

      points.forEach(point => {
        const latlng = new L.LatLng(point[0], point[1]);
        coordinates.push(latlng);
      });

      const polyline = new L.polyline(coordinates, {
        color: color,
        weight: 8,
        opacity: 0.5,
        smoothFactor: 1
      });

      layerGroup.addLayer(polyline);

      return polyline;
    },

    clearMap: function() {
      for (const key in this.layers) {
        this.layers[key].clearLayers();
        delete this.layers[key];
      }
    }
  },
  mounted() {
    this.initMap();
  },
  watch: {
    intersections: {
      deep: true,
      immediate: true,
      handler: function(newValue, oldValue) {
        const oldKeys = Object.keys(this.layers);
        const newKeys = Object.keys(newValue);

        const removedKeys = oldKeys.filter(
          oldKey => newKeys.indexOf(oldKey) < 0
        );

        for (const i in removedKeys) {
          const key = removedKeys[i];

          if (key in this.layers) {
            this.layers[key].clearLayers();
            delete this.layers[key];
          }
        }

        for (const i in newKeys) {
          const key = newKeys[i];
          const data = newValue[key];
          const info = data.info;
          const connections = data.connections;

          if (connections.length === 0) {
            continue;
          }

          if (key in this.layers) {
            this.layers[key].clearLayers();
          } else {
            this.layers[key] = new L.layerGroup();
            this.layers[key].addTo(this.map);
          }

          this.createMarker(info, this.layers[key]);
          this.drawPolylines(connections, this.layers[key]);
        }
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#map {
  float: right;
  width: 800px;
  height: 700px;
}

#map-target {
  width: 800px;
  height: 600px;
}

#map-controllers {
  height: 75px;
  margin-top: 25px;
  margin-bottom: 0px;
  float: right;
}
</style>
