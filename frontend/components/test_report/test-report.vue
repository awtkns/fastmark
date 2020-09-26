<template>
  <v-expansion-panels flat>
    <v-expansion-panel v-if="report" v-model="panel" class="pa-0">
      <v-expansion-panel-header :color="color" class="subtitle-1l">
        <span class="title">{{ report.name }}</span>{{ report.tests - errorCount }}/{{ report.tests }}
      </v-expansion-panel-header>
      <v-expansion-panel-content class="test-result-panel">
        <test-report v-for="r in report.testsuites" :report="r" class="mt-2 px-2" />
        <v-sheet v-for="test in report.testsuite" :color="test.failures ? 'error lighten-1': 'success lighten-1'">
          <v-row no-gutters class="mx-1 text-caption" >[{{ test.status}}] {{ test.name }}<v-spacer />{{test.result}}</v-row>
          <pre v-for="f in test.failures">{{f.failure}}</pre>
        </v-sheet>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
  export default {
    name: "test-report",
    data: () => ({
      panel: false
    }),
    props: {
      report: undefined
    },
    computed: {
      errorCount: ctx => ctx.report.errors + ctx.report.failures,
      success: ctx => ctx.errorCount !== 0,
      color: ctx => ctx.errorCount ? 'error' : 'success',
    }
  }
</script>
<style>
.test-result-panel > div {
  padding: 0 !important;
}
</style>
