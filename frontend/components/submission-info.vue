<template>
  <v-row>
    <v-col cols="12">
      <v-chip dark v-for="f in submission.files" v-text="f.filename" class="mx-1"/>
    </v-col>
    <v-col v-if="!buildResult" cols="12" class="text-h4 text-center">
      Submission has yet to be built.
    </v-col>

    <!-- Build Results -->
    <v-col v-else cols="12">
      <v-list>
        <v-list-item class="title">Build Results</v-list-item>
        <v-divider/>
        <v-list-item v-if="buildResult.error_message">
          <pre class="error--text">Error Message: {{ buildResult.error_message }}</pre>
        </v-list-item>
        <v-list-item>Exit Code:&nbsp;<span :class="buildResult.exit_code !== 0 ? 'error--text' : 'success--text'"
                                           v-text="buildResult.exit_code"/>
        </v-list-item>
      </v-list>
    </v-col>

    <!-- Test Results -->
    <v-col v-if="buildResult && testResult" cols="6">
      <v-list>
        <v-list-item class="title">Test Results</v-list-item>
        <v-divider/>
        <v-list-item v-if="testResult.error_message">
          <pre class="error--text">Error Message: {{ testResult.error_message }}</pre>
        </v-list-item>
        <v-list-item v-if="testResult.total_tests">Total Tests: {{ testResult.total_tests }}</v-list-item>
        <v-list-item v-if="testResult.totaL_errors">Total Errors: {{ testResult.totaL_errors }}</v-list-item>
        <v-list-item v-if="testResult.total_failures">Total Failures: {{ testResult.total_failures }}</v-list-item>
        <v-list-item>Exit Code:&nbsp;<span :class="testResult.exit_code !== 0 ? 'error--text' : 'success--text'" v-text="testResult.exit_code"/>
        </v-list-item>
      </v-list>
    </v-col>
    <v-col v-if="buildResult && testResult" cols="6" >
      <test-report :report="testResult.json_report" />
    </v-col>


    <v-col cols="12">
      <btn-build-submission :submission="submission"/>
    </v-col>
  </v-row>
</template>

<script>
import TestReport from "./test_report/test-report";
export default {
  name: "submission-info",
  components: {TestReport},
  props: {
    submission: undefined
  },
  computed: {
      buildResult: (ctx) => ctx.submission.build_result,
      testResult: (ctx) => ctx.submission.build_result.test_result
  },
}
</script>
