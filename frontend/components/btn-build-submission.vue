<template>
  <v-btn text @click="buildSubmission(submission)">Build</v-btn>
</template>

<script>
import { generic_post } from '~/api'

export default {
  name: "btn-build-submission",
  props: {
    submission: undefined
  },
  methods: {
    async buildSubmission(submission) {
      if (submission && submission.id) generic_post(this, `/submissions/${submission.id}`)
    }
  }
}
</script>
