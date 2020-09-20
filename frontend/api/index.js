export const generic_get = async ({ $axios }, url) => (await $axios.get(url)).data

export const generic_post = async ({ $axios }, url, payload) => (await $axios.post(url, payload)).data

