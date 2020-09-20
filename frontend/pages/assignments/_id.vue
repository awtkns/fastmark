<template>
  <div v-if="assignment">
    <v-expansion-panels v-model="panel">
      <v-expansion-panel v-for="s in assignment.submissions">
        <v-expansion-panel-header>
          <v-row no-gutters align="center">
            <span>{{ s.student.name }}</span>
            <v-spacer/>
            <v-chip class="mr-2" v-if="s.late" color="error" outlined v-text="'Late'" />
            <v-chip class="mr-2" v-if="s.overdue" color="error" v-text="'overdue'" />
          </v-row>

        </v-expansion-panel-header>
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
