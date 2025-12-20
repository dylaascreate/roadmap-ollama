<template>
  <div style="padding:20px">
    <h1>DevNexus Admin</h1>
    <nav style="margin-bottom:12px">
      <button @click="tab='careers'">Careers</button>
      <button @click="tab='skills'">Skills</button>
      <button @click="tab='phases'">Phases</button>
      <button @click="tab='tasks'">Tasks</button>
      <button @click="tab='suggestions'">Suggestions</button>
      <button @click="tab='generator'">Generator</button>
      <button @click="tab='profile'">My Profile</button>
    </nav>

    <div v-if="tab==='careers'"><CareerPage /></div>
    <div v-if="tab==='skills'"><SkillPage /></div>
    <div v-if="tab==='phases'"><RoadmapPhasePage /></div>
    <div v-if="tab==='tasks'"><PhaseTaskPage /></div>
    <div v-if="tab==='suggestions'"><RoadmapSuggestionPage /></div>
    <div v-if="tab==='generator'"><RoadmapGenerator /></div>
    <div v-if="tab==='profile'"><UserProfile /></div>
  </div>
</template>

<script>
import CareerPage from './CareerPage.vue'
import SkillPage from './SkillPage.vue'
import RoadmapPhasePage from './RoadmapPhasePage.vue'
import PhaseTaskPage from './PhaseTaskPage.vue'
import RoadmapSuggestionPage from './RoadmapSuggestionPage.vue'
import RoadmapGenerator from './RoadmapGenerator.vue'
import UserProfile from './UserProfile.vue'
export default {
  components: {
    CareerPage,
    SkillPage,
    RoadmapPhasePage,
    PhaseTaskPage,
    RoadmapSuggestionPage,
    RoadmapGenerator,
    UserProfile
  },
  data() {
    return { tab: 'careers' }
  }
}
</script>