// This should probably be moved into @unrest/react-api along with the two forms that use them
// could be an POSTForm component

const getCSRF = (cookie=document.cookie) => {
  const match = cookie.match(/csrftoken=([^;]+)/)
  return match && match[1]
}

export default (url, data) => {
  return fetch(url, {
    body: JSON.stringify(data),
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      "X-CSRFToken": getCSRF()
    }
  }).then(r => r.json())
}