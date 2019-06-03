<template>
  <div id="app">
    <div class="tile is-ancestor">
      <div class="tile is-3 is-vertical is-parent">
        <div class="tile is-child">
          <SourceSelector v-on:source-selected="selectSource"/>
          <SetupRsu v-if="source === 'Map-Creator'" v-on:new-rsu="addRsu"/>
          <JsonLoader v-if="source === 'Map-Validator'" v-on:update-map="updateMap"/>
          <Connections v-bind:rsus="rsus" v-on:update-map="updateMap"/>
        </div>
      </div>
      <div class="tile is-parent">
        <div class="tile is-child">
          <Map v-bind:intersections="intersections"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Connections from './components/Connections.vue'
import JsonLoader from './components/JsonLoader.vue'
import Map from './components/Map.vue'
import SetupRsu from './components/SetupRsu.vue'
import SourceSelector from './components/SourceSelector.vue'

export default {
  name: 'app',
  components: {
    Connections,
    JsonLoader,
    Map,
    SetupRsu,
    SourceSelector
  },
  data: function() {
    return {
      source: 'Map-Creator',
      intersections: {},
      rsus: []
    }
  },
  methods: {
    addRsu: function(rsu) {
      this.rsus.push(rsu);
    },

    selectSource: function(source) {
      this.source = source;
    },

    updateMap: function(connections, info) {
      this.$set(this.intersections, info, connections);
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 60px 120px;
}
</style>
