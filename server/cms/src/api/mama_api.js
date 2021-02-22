import axios from 'axios'

export function listProxy () {
  return axios
    .get('/users', {
      params: {
        proxy: 1
      }
    })
    .then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
}
