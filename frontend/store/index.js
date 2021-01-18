import { generic_get, generic_post, generic_delete } from "~/api";
import { uploadAssignmentFile, uploadAssignmentArtifact } from "~/api/assignments"

export const state = () => ({
  assignments: [],
  assignment: undefined
})


export const mutations = {
  setAssignments: (state, assignments) => state.assignments = assignments,
  setAssignment: (state, assignment) => state.assignment = assignment,
  addAssignment: (state, assignment) => state.assignments.push(assignment),
  removeAssignment: (state, id) => state.assignments = state.assignments.filter(a => a.id !== id),
}

export const actions = {
  async fetchAssignments({ commit }) {
    commit('setAssignments', await generic_get(this, '/assignments/'))
  },
  async addAssignment({ commit }, {assignment, submissions, solution, makefile}) {
    const db_assignment =  await generic_post(this, '/assignments/', assignment)

    if (submissions) await uploadAssignmentFile(this, submissions, db_assignment)
    if (solution) await uploadAssignmentArtifact(this, solution, db_assignment.id)
    if (makefile) await uploadAssignmentArtifact(this, makefile, db_assignment.id)

    commit('addAssignment', db_assignment)
  },
  async fetchAssignment({ commit }, id) {
    commit('setAssignment', await generic_get(this, `/assignments/${id}/`))
  },
  async deleteAssignment({ commit }, id) {
    await generic_delete(this, `/assignments/${id}/`)
    commit('setAssignment', undefined)
    commit('removeAssignment', id)
  },
}
