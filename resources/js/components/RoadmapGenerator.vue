<template>
  <div>
    <h2>Generate Roadmap</h2>
    <div>
      <label>Career</label>
      <input v-model="career" />
    </div>
    <div>
      <label>Skills (comma separated)</label>
      <input v-model="skills" />
    </div>
    <div>
      <button @click="generate">Generate</button>
    </div>
    <div v-if="loading">Generating...</div>
    <pre v-if="result">{{ result }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return { career: '', skills: '', result: null, loading: false }
  },
  methods: {
    async generate() {
      this.loading = true
      try {
        const res = await this.$axios.post('/roadmaps/generate', {
          career: this.career,
          skills: this.skills
        })
        this.result = JSON.stringify(res.data, null, 2)
      } catch (e) {
        this.result = e.response ? e.response.data : String(e)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>