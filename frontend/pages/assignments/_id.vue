<template>
  <div>
    <v-expansion-panels v-model="panel">
      <v-expansion-panel v-for="s in assignment.submissions">
        <v-expansion-panel-header>{{ s.student.name }}</v-expansion-panel-header>
        <v-expansion-panel-content>
          Some content
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    {{ assignment }}
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "assignment",
  data: () => ({
    panel: undefined,
  }),
  computed: {
    ...mapState(['assignment'])
  },
  created() {
    this.$store.dispatch('fetchAssignment', this.$route.params.id)
  }
}
</script>
