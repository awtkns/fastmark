<template>
  <v-btn text @click="openSubmission(submission)">Open</v-btn>
</template>

<script>
import { generic_get } from '~/api'

export default {
  name: "btn-open-submission",
  props: {
    submission: undefined
  },
  methods: {
    async openSubmission(submission) {
      const params = { open : 'subl'}
      if (submission && submission.id) generic_get(this, `/submissions/${submission.id}?`, params)
    }
  }
}
</script>
