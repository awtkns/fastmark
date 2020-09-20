<template>
  <v-app>

    <v-navigation-drawer app permanent>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            FastMark
          </v-list-item-title>
          <v-list-item-subtitle>
            Assignments
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item v-for="a in assignments" :key="a.id" link>
          <v-list-item-content>
            <v-list-item-title>{{ a.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <f-assignment />
        </div>
      </template>
    </v-navigation-drawer>

    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>

  </v-app>
</template>

<script>
import { mapState } from 'vuex'
import FAssignment from "../components/f-assignment";

export default {
  components: {FAssignment},
  computed: {
    ...mapState(['assignments'])
  },
  created() {
    this.$store.dispatch('fetchAssignments')
  },
}
</script>
