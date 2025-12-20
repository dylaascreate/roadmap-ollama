<template>
  <GenericCrud
    endpoint="/skills"
    title="Skills"
    :fields="['id','name']"
    :formFields="[
      { name: 'name', label: 'Name' }
    ]"
  />
</template>

<script>
import GenericCrud from './GenericCrud.vue'
export default { components: { GenericCrud } }
</script>