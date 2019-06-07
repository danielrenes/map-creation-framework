<template>
  <div class="connection">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          <ul>
            <li>Host: {{ rsu.host }}</li>
            <li>Port: {{ rsu.port }}</li>
            <li>Status: {{ rsu.status }}</li>
          </ul>
        </p>
        <a v-on:click="remove" href="#" class="card-header-icon">
          <span class="icon">
            <i class="fas fa-times" aria-hidden="true"></i>
          </span>
        </a>
      </header>
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

          this.$el.querySelector('.card-header-title').style.color = AVAILABLE_COLOR;

          const info = {};
          const connections = [];

          Promise.all([this.getRsuInfo(info), this.getMapData(connections)]).then(() => {
            this.$emit('update-map', connections, info);
          });
        })
        .catch(err => {
          this.rsu.status = 'unavailable';
          this.$el.querySelector('.card-header-title').style.color = UNAVAILABLE_COLOR;
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
          if ('ingresses' in resp.data) {
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
          }
        })
        .catch(err => {
          console.log(err);
        });
    },

    remove: function() {
      this.$emit('remove-connection', this.rsu);
      clearInterval(this.interval);
    }
  },
  mounted() {
    this.interval = setInterval(this.ping, 5000);
  }
}
</script>

<style scoped>
  #connection {
    margin-bottom: 0.25rem;
  }

  .card-header-title {
    font-weight: normal;
  }

  .card-header-icon {
    align-items: flex-start;
    outline: none;
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
