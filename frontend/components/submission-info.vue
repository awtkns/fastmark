<template>
  <v-row justify="start">
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
        <v-list-item>Exit Code:&nbsp;
          <span :class="buildResult.exit_code !== 0 ? 'error--text' : 'success--text'" v-text="buildResult.exit_code"/>
        </v-list-item>
      </v-list>
    </v-col>

    <!-- Test Results -->
    <v-col v-if="testResults" v-for="tr in testResults" :cols="testResults.length === 1 ? 12 : 6">
      <v-list>
        <v-list-item class="title">{{ tr.name }} Results</v-list-item>
        <v-divider/>
        <v-list-item v-if="tr.stderr">
          <pre class="error--text">Error Message: {{ tr.error_message }}</pre>
        </v-list-item>
        <v-list-item v-if="tr.total_tests">Total Tests: {{ tr.total_tests }}</v-list-item>
        <v-list-item v-if="tr.totaL_errors">Total Errors: {{ tr.totaL_errors }}</v-list-item>
        <v-list-item v-if="tr.total_failures">Total Failures: {{ tr.total_failures }}</v-list-item>
        <v-list-item>Exit Code:&nbsp;<span :class="tr.exit_code !== 0 ? 'error--text' : 'success--text'" v-text="tr.exit_code"/>
        </v-list-item>
        <test-report :report="tr.json_report" />
      </v-list>
    </v-col>
    <v-col cols="12">
      <v-row no-gutters justify="end">
        <btn-open-submission :submission="submission"/>
        <btn-build-submission :submission="submission"/>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import TestReport from "./test_report/test-report";
import BtnOpenSubmission from "./btn-open-submission";
import BtnBuildSubmission from "./btn-build-submission";
export default {
  name: "submission-info",
  components: {BtnBuildSubmission, BtnOpenSubmission, TestReport},
  props: {
    submission: undefined
  },
  computed: {
      buildResult: (ctx) => ctx.submission.build_result,
      testResults: (ctx) => ctx.buildResult ? ctx.buildResult.test_results : undefined
  },
}
</script>
