<template>
  <div id="map" class="map">
  </div>
</template>

<script>
import axios from 'axios';

const INGRESS_COLOR = "rgb(255, 0, 0)";
const EGRESS_COLOR = "rgb(0, 0, 255)";

export default {
  name: 'Map',
  props: ['rsus'],
  data() {
      return {
        map: null,
        tileLayer: null,
        layers: {},
        interval: null
    }
  },
  methods: {
    initMap: function() {
      this.map = new L.map('map').setView([47.4753, 19.0561], 16);
      this.tileLayer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          minZoom: 8,
          maxZoom: 18,
          attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
        }
      );

      this.tileLayer.addTo(this.map);
    },

    pullRsus: function() {
      // find rsus that are in the layers but were removed
      let removed_rsu_ids = Object.keys(this.layers);

      this.rsus.forEach(rsu => {
        const rsu_id = rsu.id;
        const index = removed_rsu_ids.indexOf(rsu_id);

        if (index > -1) {
          removed_rsu_ids.splice(index, 1);
          this.layers[rsu_id].length = 0;
        } else {
          this.layers[rsu_id] = [];
        }

        this.getRsuInfo(rsu, this.layers[rsu_id]);
        this.getMapData(rsu, this.layers[rsu_id]);
      });

      // those rsus were removed, so they are removed from the map
      removed_rsu_ids.forEach(rsu_id => {
        this.layers[rsu_id].forEach(layer => {
          map.removeLayer(layer);
        });

        delete this.layers[rsu_id];
      });
    },

    getRsuInfo: function(rsu, layerList) {
      axios
        .get('http://' + rsu.host + ':' + rsu.port + '/')
        .then(resp => {
          const refPoint = resp.data['ref_point'];
          const range = resp.data['range'];

          this.addMarker(refPoint['latitude'], refPoint['longitude'], layerList,
            'latitude: ' + refPoint['latitude'] + '<br>' +
            'longitude: ' + refPoint['longitude'] + '<br>' +
            'range: ' + range * 1000 + 'm'
          );
        })
        .catch(err => {
          console.log(err);
        });
    },

    getMapData: function(rsu, layerList) {
      axios
        .get('http://' + rsu.host + ':' + rsu.port + '/map')
        .then(resp => {
          const refPoint = resp.data['ref_point'];
          const ingresses = resp.data['ingresses'];

          this.addMarker(refPoint['latitude'], refPoint['longitude'], layerList);

          ingresses.forEach(ingress => this.addIngress(ingress, layerList));
        })
        .catch(err => {
          console.log(err);
        });
    },

    addMarker: function(latitude, longitude, layerList, message) {
      const latlng = new L.LatLng(latitude, longitude);
      const marker = new L.marker(latlng);

      if (message !== undefined) {
        marker.bindPopup(message);
        this.map.panTo(latlng);
      }

      marker.addTo(this.map);
      layerList.push(marker);
    },

    addIngress: function(ingress, layerList) {
      const points = ingress['points'];
      const egresses = ingress['egresses'];

      this.drawPolyline(points, INGRESS_COLOR, layerList);

      egresses.forEach(egress => this.addEgress(egress, layerList));
    },

    addEgress: function(egress, layerList) {
      this.drawPolyline(egress, EGRESS_COLOR, layerList);
    },

    drawPolyline: function(points, color, layerList) {
      if (!points) {
        return;
      }

      const coordinates = [];

      points.forEach(point => {
        const latlng = new L.LatLng(point['latitude'], point['longitude']);
        coordinates.push(latlng);
      });

      const polyline = new L.polyline(coordinates, {
        color: color,
        weight: 8,
        opacity: 0.5,
        smoothFactor: 1
      });

      polyline.addTo(this.map);
      layerList.push(polyline);
    }
  },
  mounted() {
    this.initMap();

    // TODO: stop interval when all rsus are removed
    this.interval = setInterval(this.pullRsus, 10000);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#map {
  float: right;
  width: 800px;
  height: 600px;
}
</style>
