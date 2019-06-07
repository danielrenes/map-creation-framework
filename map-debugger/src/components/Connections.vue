<template>
  <div id="connections">
    <div v-bind:key="rsu.id" v-for="rsu in rsus">
      <Connection v-bind:rsu="rsu" v-on:update-map="updateMap" v-on:remove-connection="removeConnection"/>
    </div>
  </div>
</template>

<script>
import Connection from './Connection.vue'

export default {
  name: 'Connections',
  components: {
    Connection
  },
  props: ['rsus'],
  methods: {
    updateMap: function(connections, info) {
      this.$emit('update-map', connections, info);
    },

    removeConnection: function(rsu) {
      this.$emit('remove-connection', rsu);
    }
  }
}
</script>

<style scoped>

</style>
