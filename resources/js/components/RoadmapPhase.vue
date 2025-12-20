<template>
  <GenericCrud
    endpoint="/roadmap-phases"
    title="Roadmap Phases"
    :fields="['id','roadmap_id','title','order']"
    :formFields="[
      { name: 'roadmap_id', label: 'Roadmap ID' },
      { name: 'title', label: 'Title' },
      { name: 'order', label: 'Order' }
    ]"
  />
</template>

<script>
import GenericCrud from './GenericCrud.vue'
export default { components: { GenericCrud } }
</script>