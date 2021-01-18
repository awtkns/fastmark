export const uploadAssignmentFile = async ({ $axios }, file, assignment) => {
  const f = await readFile(file)
  console.log("HERE")
  // Uploading File to server
  const formData = new FormData()
  formData.append('filename', file.name)
  formData.append('assignment_id', assignment.id)
  formData.append('file', new Blob([f], { type: '.zip' }))
  await $axios.post('ingest', formData)
}

export const uploadAssignmentArtifact = async ({ $axios }, file, assignment_id) => {
  const f = await readFile(file)
  console.log(file)

  // Uploading File to server
  const formData = new FormData()
  formData.append('filename', file.name)
  formData.append('file', new Blob([f]))
  await $axios.post(`/assignments/${assignment_id}/artifacts`, formData)
}


function readFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsArrayBuffer(file)
  })
}


