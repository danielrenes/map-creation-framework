<template>
  <div id="connections">
    <div v-bind:key="rsu.id" v-for="rsu in rsus">
      <Connection v-bind:rsu="rsu" v-on:update-map="updateMap"/>
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
    }
  }
}
</script>

<style scoped>

</style>
