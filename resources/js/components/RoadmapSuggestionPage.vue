<template>
  <GenericCrud
    endpoint="/roadmap-suggestions"
    title="Roadmap Suggestions"
    :fields="['id','roadmap_id','type','content']"
    :formFields="[
      { name: 'roadmap_id', label: 'Roadmap ID' },
      { name: 'type', label: 'Type' },
      { name: 'content', label: 'Content', type: 'textarea' }
    ]"
  />
</template>

<script>
import GenericCrud from './GenericCrud.vue'
export default { components: { GenericCrud } }
</script>