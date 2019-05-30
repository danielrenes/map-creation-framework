<template>
  <div id="connection">
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
      axios
        .get('http://' + this.rsu.host + ':' + this.rsu.port + '/ping')
        .then(resp => {
          this.rsu.status = 'available';
        })
        .catch(err => {
          this.rsu.status = 'unavailable';
        });
    }
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
