<template>
  <v-row>
    <v-col cols="12" class="headline">Active Jobs</v-col>
    <v-col cols="12" class="headline">
      <t-active-jobs />
    </v-col>
  </v-row>
</template>
<script>
import TActiveJobs from "../components/t-active-jobs";
export default {
  components: {TActiveJobs}
}
</script>
