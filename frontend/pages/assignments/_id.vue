<template>
  <div v-if="assignment">
    <v-row align="end" no-gutters class="mb-8">
      <span class="text-h1" v-text="assignment.name" style="text-transform: capitalize"/>
      <v-spacer/>
      <v-btn text outlined @click="buildAll">Build All</v-btn>
    </v-row>

    <v-expansion-panels v-model="panel">
      <submission-panel v-for="submission in assignment.submissions" :submission="submission" :assignment="assignment"/>
    </v-expansion-panels>

    <v-speed-dial v-model="fab" fixed bottom right>
      <template v-slot:activator>
        <v-btn v-model="fab" dark fab color="info">
          <v-icon v-if="fab">mdi-close</v-icon>
          <v-icon v-else>mdi-menu</v-icon>
        </v-btn>
      </template>

        <v-btn fab dark v-on="on" @click="deleteAssignment" color="red">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
    </v-speed-dial>
  </div>
</template>

<script>
  import {mapState} from 'vuex'
  import {generic_post} from "~/api";
  import SubmissionPanel from "../../components/submission-panel";

  export default {
    name: "assignment",
    components: {SubmissionPanel},
    data: () => ({
      panel: undefined,
      fab: undefined,
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
      },
      deleteAssignment() {
        this.$store.dispatch('deleteAssignment', this.assignment.id)
      }
    }
  }
</script>
