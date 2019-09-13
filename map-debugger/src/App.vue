<template>
  <div id="app">
    <div class="tile is-ancestor">
      <div class="tile is-3 is-vertical is-parent">
        <div class="tile is-child">
          <SourceSelector v-on:source-selected="selectSource"/>
          <SetupRsu v-if="source === 'Map-Creator'" v-on:new-rsu="addRsu"/>
          <JsonLoader v-if="source === 'Map-Validator'" v-on:update-map="updateMap"/>
          <Connections v-if="source === 'Map-Creator'" v-bind:rsus="rsus" v-on:update-map="updateMap" v-on:remove-connection="removeConnection"/>
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

    uniqueId: function(a, b) {
      return (a + b) * (a + b + 1) / 2 + a;
    },

    updateMap: function(connections, info, rsu) {
      if (connections.length > 0) {
        let key = 0;
        if (info !== undefined) {
          if (rsu === undefined || rsu.key === undefined) {
            key = this.uniqueId(Math.floor(info.refPoint.latitude * 1e7), Math.floor(info.refPoint.longitude * 1e7));

            if (rsu !== undefined) {
              rsu.uniqueId = key;
            }
          } else {
            key = rsu.uniqueId;
          }
        }
        this.$set(this.intersections, key, {info: info, connections: connections});
      }
    },

    removeConnection: function(rsu) {
      this.rsus = this.rsus.filter(element => element != rsu);
      console.log('delete');
      this.$delete(this.intersections, rsu.uniqueId);
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
