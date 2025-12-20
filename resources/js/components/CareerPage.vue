<template>
  <GenericCrud
    endpoint="/careers"
    title="Careers"
    :fields="['id','name','description']"
    :formFields="[
      { name: 'name', label: 'Name' },
      { name: 'description', label: 'Description', type: 'textarea' }
    ]"
  />
</template>

<script>
import GenericCrud from './GenericCrud.vue'
export default { components: { GenericCrud } }
</script>