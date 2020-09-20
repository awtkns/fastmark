import { generic_get, generic_post } from "~/api";
import { uploadAssignmentFile } from "~/api/assignments"

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
  async addAssignment({ commit }, {assignment, file}) {
    const db_assignment =  await generic_post(this, '/assignments/', assignment)
    uploadAssignmentFile(this, file, db_assignment)
    commit('addAssignment', db_assignment)
  }
}
