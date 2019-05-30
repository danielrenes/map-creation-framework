<template>
  <div id="setup-rsu">
    <form v-on:submit.prevent="onSubmit">
      <div class="field has-addons">
        <div class="control">
          <input v-model="connection" class="input is-link" type="text" placeholder="RSU (IP:Port)">
        </div>
        <div class="control">
          <button class="button is-link">Add</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SetupRsu',
  data() {
    return {
      connection: ''
    }
  },
  methods: {
    onSubmit: function() {
      const defaultHost = 'localhost';
      const defaultPort = 31289;

      let [host, port] = this.connection.split(':');

      if (host === undefined || host === '') {
        host = defaultHost;
      }

      if (port === undefined || port === '') {
        port = defaultPort;
      }

      const rsu = {
        id: host + ':' + port,
        host: host,
        port: port,
        status: ''
      }

      this.$emit('new-rsu', rsu);

      this.connection = '';
    }
  }
}
</script>

<style scoped>
  #setup-rsu {
    margin: 1rem 0;
  }
</style>
