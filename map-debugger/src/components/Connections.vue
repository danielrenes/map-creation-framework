<template>
  <div id="connections">
    <div v-bind:key="rsu.id" v-for="rsu in rsus">
      <Connection v-bind:rsu="rsu"/>
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
  props: ['rsus']
}
</script>

<style scoped>

</style>
