<template>
  <div id="json-loader">
    <div class="file has-name">
			<label class="file-label">
				<input v-on:change="openFile" class="file-input" type="file" accept=".json">
				<span class="file-cta">
					<span class="file-icon">
						<i class="fas fa-upload"></i>
					</span>
					<span class="file-label">Select JSON</span>
				</span>
				<span class="file-name">{{ filename }}</span>
			</label>
		</div>
  </div>
</template>

<script>
export default {
  name: 'JsonLoader',
  data() {
    return {
			filename: ''
    }
  },
  methods: {
		openFile: function(event) {
			const file = event.target.files[0];
			const reader = new FileReader();
			reader.onload = event => {
				const content = event.target.result;
				const json = JSON.parse(content);
				this.filename = file.name;
			};
			reader.readAsText(file);
		}
  }
}
</script>

<style scoped>
	#json-loader {
    margin: 1rem 0;
  }

	.file-name {
		width: 12rem;
	}
</style>
