<template>
  <div>
    <h2>{{ title }}</h2>
    <div style="margin-bottom:12px">
      <input v-model="filter" placeholder="search" />
      <button @click="fetchList">Refresh</button>
    </div>
    <table border="1" cellpadding="6" cellspacing="0">
      <thead>
        <tr>
          <th v-for="col in cols" :key="col">{{ col }}</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in list" :key="item.id">
          <td v-for="field in fields" :key="field">{{ display(item, field) }}</td>
          <td>
            <button @click="startEdit(item)">Edit</button>
            <button @click="remove(item)">Delete</button>
            <button v-if="attachable" @click="$emit('attach', item)">Attach</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div style="margin-top:12px">
      <h3>{{ editing.id ? 'Edit' : 'Create' }}</h3>
      <div v-for="f in formFields" :key="f.name" style="margin-bottom:8px">
        <label :for="f.name">{{ f.label }}</label>
        <div v-if="f.type === 'textarea'">
          <textarea v-model="editing[f.name]" :id="f.name" rows="3"></textarea>
        </div>
        <div v-else>
          <input v-model="editing[f.name]" :id="f.name" />
        </div>
      </div>
      <button @click="save">{{ editing.id ? 'Update' : 'Create' }}</button>
      <button @click="reset">Cancel</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    endpoint: { type: String, required: true },
    title: { type: String, required: true },
    fields: { type: Array, required: true },
    formFields: { type: Array, required: true },
    attachable: { type: Boolean, default: false }
  },
  data() {
    const cols = this.fields.map(f => f)
    return {
      list: [],
      editing: {},
      filter: '',
      cols
    }
  },
  methods: {
    display(item, field) {
      const v = item[field]
      return typeof v === 'object' ? JSON.stringify(v) : v
    },
    async fetchList() {
      const res = await this.$axios.get(this.endpoint)
      this.list = res.data
    },
    startEdit(item) {
      this.editing = Object.assign({}, item)
    },
    reset() {
      this.editing = {}
    },
    async save() {
      if (this.editing.id) {
        const id = this.editing.id
        const payload = this.pickFields(this.editing)
        const res = await this.$axios.put(`${this.endpoint}/${id}`, payload)
        await this.fetchList()
        this.reset()
      } else {
        const payload = this.pickFields(this.editing)
        const res = await this.$axios.post(this.endpoint, payload)
        await this.fetchList()
        this.reset()
      }
    },
    pickFields(obj) {
      const payload = {}
      this.formFields.forEach(f => {
        payload[f.name] = obj[f.name] ?? null
      })
      return payload
    },
    async remove(item) {
      if (!confirm('Delete?')) return
      await this.$axios.delete(`${this.endpoint}/${item.id}`)
      await this.fetchList()
    }
  },
  mounted() {
    this.fetchList()
  }
}
</script>