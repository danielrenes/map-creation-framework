<template>
  <div class="connection">
    <div class="card">
      <div class="card-content">
        <div class="content">
          <ul>
            <li>Host: {{ rsu.host }}</li>
            <li>Port: {{ rsu.port }}</li>
            <li>Status: {{ rsu.status }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const AVAILABLE_COLOR = '#4BB543';
const UNAVAILABLE_COLOR = '#FFD2D2';

export default {
  name: 'Connection',
  props: ['rsu'],
  data() {
    return {
      interval: null
    }
  },
  methods: {
    ping: function() {
      return axios
        .get('http://' + this.rsu.host + ':' + this.rsu.port + '/ping')
        .then(resp => {
          this.rsu.status = 'available';

          this.$el.querySelector('.card').style.color = AVAILABLE_COLOR;

          const info = {};
          const connections = [];

          Promise.all([this.getRsuInfo(info), this.getMapData(connections)]).then(() => {
            this.$emit('update-map', connections, info);
          });
        })
        .catch(err => {
          this.rsu.status = 'unavailable';
          this.$el.querySelector('.card').style.color = UNAVAILABLE_COLOR;
        });
    },

    getRsuInfo: function(info) {
      return axios
        .get('http://' + this.rsu.host + ':' + this.rsu.port + '/')
        .then(resp => {
          const refPoint = resp.data.ref_point;
          const range = resp.data.range;

          info.refPoint = refPoint;
          info.range = range;
        })
        .catch(err => {
          console.log(err);
        });
    },

    getMapData: function(connections) {
      return axios
        .get('http://' + this.rsu.host + ':' + this.rsu.port + '/map')
        .then(resp => {
          const ingresses = resp.data.ingresses;

          ingresses.forEach(ingress => {
            const ingressCoordinates = [];

            ingress.points.forEach(point => {
              ingressCoordinates.push([point.latitude, point.longitude]);
            });

            ingress.egresses.forEach(egress => {
              const egressCoordinates = [];

              egress.forEach(point => {
                egressCoordinates.push([point.latitude, point.longitude]);
              });

              const connection = {
                ingress: ingressCoordinates,
                egress: egressCoordinates
              };

              connections.push(connection);
            });
          });
        })
        .catch(err => {
          console.log(err);
        });
    },
  },
  mounted() {
    // TODO: stop interval when rsu is removed

    this.interval = setInterval(this.ping, 5000);
  }
}
</script>

<style scoped>
  #connection {
    margin-bottom: 0.25rem;
  }

  ul {
    margin: 0;
  }

  li {
    list-style: none;
    text-align: start;
  }

  .card-content {
    padding: 0.5rem 1rem;
  }
</style>
