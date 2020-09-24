<template>
  <v-data-table
    :headers="headers"
    :items="jobs"
    class="elevation-1"
  />
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "t-active-jobs",
  data: () => ({
    headers: [
      {text: 'Job ID', value: 'id'},
      {text: 'Name', value: 'name'},
      {text: 'Type', value: 'type'},
      {text: 'Status', value: 'status'}
    ]
  }),
  computed: {
    ...mapState('jobs', ['jobs'])
  },
  created() {
    this.$store.dispatch('jobs/fetchJobs')
  }
}
</script>
