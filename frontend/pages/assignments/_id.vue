<template>
  <div v-if="assignment">
    <span class="text-h1" v-text="assignment.name" style="text-transform: capitalize" />

    <v-expansion-panels v-model="panel">
      <v-expansion-panel v-for="s in assignment.submissions">
        <v-expansion-panel-header class="py-0">
          <v-row no-gutters align="center">
            <span>{{ s.student.name }}</span>
            <v-spacer/>
            <v-chip class="mr-2" v-if="s.late" color="error" outlined v-text="'Late'" />
            <v-chip class="mr-2" v-if="s.overdue" color="error" v-text="'overdue'" />
            <v-chip
              v-if="assignment.expected_files && getMissing(assignment.expected_files, s.files).length"
              class="mr-2" color="warning"
              v-text="'Missing files'"
              outlined
            />
          </v-row>

        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row>
            <v-col cols="12"><v-chip dark v-for="f in s.files" v-text="f.filename" class="mx-1"/></v-col>
            <v-col cols="12">
              <v-btn text @click="buildSubmission(s)">Build</v-btn>
            </v-col>
            <v-col cols="12">
              {{ s }}
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { generic_post } from "~/api";

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
    },
    async buildSubmission(submission) {
      let r = await generic_post(this, `/submissions/${submission.id}`)
      console.log(r)
    }
  }
}
</script>
