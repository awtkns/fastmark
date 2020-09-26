<template>
  <v-expansion-panel>
      <v-expansion-panel-header class="py-0">
        <v-row no-gutters align="center">
          <span class="subtitle-1">{{ submission.student.name }}</span>
          <v-spacer/>
          <v-chip class="mr-2" v-if="submission.late" color="error" outlined v-text="'Late'" />
          <v-chip class="mr-2" v-if="submission.overdue" color="error" v-text="'overdue'" />
          <v-chip
            v-if="assignment.expected_files && getMissing(assignment.expected_files, submission.files).length"
            class="mr-2" color="warning"
            v-text="'Missing files'"
            outlined
          />
          <v-icon v-if="submission.build_result && submission.build_result.test_result" v-text="'mdi-check'" color="success" />
        </v-row>

      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <submission-info :submission="submission" />
      </v-expansion-panel-content>
    </v-expansion-panel>
</template>

<script>
import { generic_post } from '~/api'
import BtnBuildSubmission from "./btn-build-submission";
import SubmissionInfo from "./submission-info";

export default {
  name: "submission-panel",
  components: {SubmissionInfo, BtnBuildSubmission},
  props: {
    submission: undefined,
    assignment: undefined
  },
  data: () => ({

  }),
  computed: {
      buildResult: (ctx) => ctx.submission.build_result,
      testResult: (ctx) => ctx.submission.build_result.test_result
  },
  methods: {
    getMissing: (expected, files) => {
      const actual = files.map(f => f.filename)
      return expected.filter(e => !actual.includes(e))
    }
  }
}
</script>
