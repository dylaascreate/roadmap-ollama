<template>
  <GenericCrud
    endpoint="/phase-tasks"
    title="Phase Tasks"
    :fields="['id','roadmap_phase_id','content','order']"
    :formFields="[
      { name: 'roadmap_phase_id', label: 'Phase ID' },
      { name: 'content', label: 'Content', type: 'textarea' },
      { name: 'order', label: 'Order' }
    ]"
  />
</template>

<script>
import GenericCrud from './GenericCrud.vue'
export default { components: { GenericCrud } }
</script>