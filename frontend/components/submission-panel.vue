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
        <v-row>
          <v-col cols="12"><v-chip dark v-for="f in submission.files" v-text="f.filename" class="mx-1"/></v-col>
          <v-col v-if="!buildResult" cols="12" class="text-h4 text-center">
            Submission has yet to be built.
          </v-col>

           <!-- Build Results -->
          <v-col v-else cols="12">
            <v-list>
              <v-list-item class="title">Build Results</v-list-item>
              <v-divider />
              <v-list-item v-if="buildResult.error_message">
                <pre class="error--text">Error Message: {{ buildResult.error_message }}</pre>
              </v-list-item>
              <v-list-item>Exit Code:&nbsp;<span :class="buildResult.exit_code !== 0 ? 'error--text' : 'success--text'" v-text="buildResult.exit_code" />
              </v-list-item>
            </v-list>
          </v-col>

          <!-- Test Results -->
          <v-col v-if="buildResult && testResult" cols="12">
            <v-list>
              <v-list-item class="title">Test Results</v-list-item>
              <v-divider />
              <v-list-item v-if="testResult.error_message">
                <pre class="error--text">Error Message: {{ testResult.error_message }}</pre>
              </v-list-item>
              <v-list-item v-if="testResult.total_tests">Total Tests: {{ testResult.total_tests }}</v-list-item>
              <v-list-item v-if="testResult.totaL_errors">Total Errors: {{ testResult.totaL_errors }}</v-list-item>
              <v-list-item v-if="testResult.total_failures">Total Failures: {{ testResult.total_failures }}</v-list-item>
              <v-list-item>Exit Code:&nbsp;<span :class="testResult.exit_code !== 0 ? 'error--text' : 'success--text'" v-text="testResult.exit_code" />
              </v-list-item>
            </v-list>
          </v-col>


          <v-col cols="12">
            <v-btn text @click="buildSubmission(submission)">Build</v-btn>
          </v-col>
        </v-row>
      </v-expansion-panel-content>
    </v-expansion-panel>
</template>

<script>
import { generic_post } from '~/api'

export default {
  name: "submission-panel",
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
    },
    async buildSubmission(submission) {
      let r = await generic_post(this, `/submissions/${submission.id}`)
      console.log(r)
    },
  }
}
</script>
