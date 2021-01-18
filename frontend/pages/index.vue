<template>
  <v-row align="center" justify="center">
    <v-col cols="12" class="text-center">
      <h1>FastMark</h1>
      <v-btn outlined color="white" :to="'/dashboard'">Start</v-btn>
    </v-col>
  </v-row>
</template>
<script>
import TActiveJobs from "../components/t-active-jobs";
export default {
  components: {TActiveJobs},
  layout: 'home'
}
</script>

<style>
h1 {
  font-family: 'Faster One', cursive !important;
  font-size: 72px;
  color: black;
}
</style>
