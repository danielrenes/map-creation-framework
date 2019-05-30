<template>
  <div id="source-selector">
		<div class="tabs">
			<ul>
				<li v-on:click="openTab" class="tab is-active"><a>Map-Creator</a></li>
				<li v-on:click="openTab" class="tab"><a>Map-Validator</a></li>
			</ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SourceSelector',
  data() {
    return {
    }
  },
  methods: {
		openTab(event) {
			const elements = document.getElementsByClassName('tab');
			Array.prototype.forEach.call(elements, element =>
					element.className = element.className.replace(' is-active', '')
			);
			event.currentTarget.className += ' is-active';
			const source = event.currentTarget.querySelector('a').innerHTML;
			this.$emit('source-selected', source);
		}
  }
}
</script>

<style scoped>
</style>
