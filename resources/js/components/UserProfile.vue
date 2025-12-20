<template>
  <div>
    <h2>My Profile</h2>
    <div>
      <button @click="load">Refresh</button>
    </div>
    <div v-if="profile">
      <h3>Skills</h3>
      <ul>
        <li v-for="s in profile.skills" :key="s.id">
          {{ s.name }}
          <button @click="detachSkill(s.id)">Remove</button>
        </li>
      </ul>
      <div>
        <select v-model="selectedSkill">
          <option v-for="s in skills" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
        <button @click="attachSkill">Add Skill</button>
      </div>

      <h3>Careers</h3>
      <ul>
        <li v-for="c in profile.careers" :key="c.id">
          {{ c.name }}
          <button @click="detachCareer(c.id)">Remove</button>
        </li>
      </ul>
      <div>
        <select v-model="selectedCareer">
          <option v-for="c in careers" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
        <button @click="attachCareer">Add Career</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return { profile: null, skills: [], careers: [], selectedSkill: null, selectedCareer: null }
  },
  methods: {
    async load() {
      const me = await this.$axios.get('/me')
      this.profile = me.data
      const s = await this.$axios.get('/skills')
      this.skills = s.data
      const c = await this.$axios.get('/careers')
      this.careers = c.data
    },
    async attachSkill() {
      await this.$axios.post('/me/skills', { skill_id: this.selectedSkill })
      await this.load()
    },
    async detachSkill(id) {
      await this.$axios.delete(`/me/skills/${id}`)
      await this.load()
    },
    async attachCareer() {
      await this.$axios.post('/me/careers', { career_id: this.selectedCareer })
      await this.load()
    },
    async detachCareer(id) {
      await this.$axios.delete(`/me/careers/${id}`)
      await this.load()
    }
  },
  mounted() {
    this.load()
  }
}
</script>