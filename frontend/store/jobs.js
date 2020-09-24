import { generic_get } from '~/api'

export const state = () => ({
    jobs: []
})

export const mutations = {
    setJobs: (state, jobs) => state.jobs = jobs,
}

export const actions = {
    async fetchJobs({commit}) {
        commit('setJobs', await generic_get(this, '/jobs/'))
    },
}
