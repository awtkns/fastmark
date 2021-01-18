<template>
  <v-app>
    <v-app-bar color="deep-purple accent-4" dense dark app>
      <v-app-bar-nav-icon @click="nav = !nav"/>
      <div class="title">FastMark</div>
      <v-breadcrumbs :items="crumbs">
        <template v-slot:item="{ item }">
          <v-breadcrumbs-item :disabled="item.disabled" :to="item.to" style="color: white; text-decoration: none">
            {{ item.text.toUpperCase() }}
          </v-breadcrumbs-item>
        </template>
      </v-breadcrumbs>
    </v-app-bar>

    <v-navigation-drawer v-model="nav" app>
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
      <v-divider/>
      <v-list-item :to="`/dashboard`">
        <v-list-item-content>
          <v-list-item-title>Active Jobs</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider/>

      <v-list dense nav>
        <v-list-item v-for="a in assignments" :key="a.id" :to="`/assignments/${a.id}`">
          <v-list-item-content>
            <v-list-item-title>{{ a.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <f-assignment/>
        </div>
      </template>
    </v-navigation-drawer>


    <v-main>
      <v-container>
        <nuxt/>
      </v-container>
    </v-main>

  </v-app>
</template>

<script>
  import {mapState} from 'vuex'
  import FAssignment from "../components/f-assignment";

  export default {
    components: {FAssignment},
    data: () => ({
      nav: true
    }),
    computed: {
      ...mapState(['assignments']),
      crumbs: ctx => {
        if (ctx.$route.path === '/') return []

        const routes = ctx.$route.path.split('/');
        const items = []
        for (const i in routes) {
          items.push({
            to: items.length ? items[items.length - 1].to + `${routes[i]}/` : '/',
            text: routes[i] ? routes[i] : ''
          })
        }

        return items
      }
    },
    created() {
      this.$store.dispatch('fetchAssignments')
    },
  }
</script>
<style>
a, a:hover, a:focus, a:active {
    text-decoration: none;
    color: inherit !important;
}
</style>
