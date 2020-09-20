import { generic_get, generic_post } from "~/api";

export const state = () => ({
  assignments: []
})


export const mutations = {
  setAssignments: (state, assignments) => state.assignments = assignments,
  addAssignment: (state, assignment) => state.assignments.push(assignment)
}

export const actions = {
  async fetchAssignments({ commit }) {
    commit('setAssignments', await generic_get(this, 'assignments'))
  },
  async addAssignment({ commit }, assignment) {
    commit('addAssignment', await generic_post(this, '/assignments/', assignment))
  }
}
