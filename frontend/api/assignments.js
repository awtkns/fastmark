export const uploadAssignmentFile = async ({ $axios }, file, assignment_id) => {
  const config = { headers: { 'Content-Type': 'multipart/form-data' } }
  const f = await readFile(file)

  // Uploading File to server
  const formData = new FormData()
  formData.append('filename', file.name)
  formData.append('assignment_id', assignment_id)
  formData.append('file', new Blob([f], { type: '.zip' }))
  await $axios.post('ingest', formData)
}


function readFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsArrayBuffer(file)
  })
}
