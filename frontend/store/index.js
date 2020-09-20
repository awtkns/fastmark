import { generic_get, generic_post } from "~/api";

export const state = () => ({
  assignments: []
})


export const mutations = {
  setAssignments: (state, assignments) => (state.assignments = assignments)
}

export const actions = {
  async fetchAssignments({ commit }) {
    commit('setAssignments', await generic_get(this, 'assignments'))
  },
  async addAssignment({ commit }, assignment) {
    console.log(assignment)
    commit('setAssignments', await generic_post(this, '/assignments/', {'name': assignment.name}))
  }
}
