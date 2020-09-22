<template>
  <div v-if="assignment">
    <v-row align="end" no-gutters class="mb-8">
      <span class="text-h1" v-text="assignment.name" style="text-transform: capitalize" />
      <v-spacer />
      <v-btn text outlined @click="buildAll">Build All</v-btn>
    </v-row>

    <v-expansion-panels v-model="panel">
      <submission-panel v-for="submission in assignment.submissions" :submission="submission" :assignment="assignment" />
    </v-expansion-panels>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { generic_post } from "~/api";
import SubmissionPanel from "../../components/submission-panel";

export default {
  name: "assignment",
  components: {SubmissionPanel},
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
    async buildAll() {
      let r = await generic_post(this, `/submissions/`)
      console.log(r)
    }
  }
}
</script>
