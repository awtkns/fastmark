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
            <v-chip class="mr-2" v-if="getMissing(assignment.expected_files, s.files).length" color="warning" v-text="'Missing files'" outlined />
          </v-row>

        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-chip dark v-for="f in s.files" v-text="f.filename" class="mx-1"/>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
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
    ...mapState(['assignment']),
  },
  created() {
    this.$store.dispatch('fetchAssignment', this.$route.params.id)
  },
  methods: {
    getMissing: (expected, files) => {
      const actual = files.map(f => f.filename)
      return expected.filter(e => !actual.includes(e))
    }
  }
}
</script>
