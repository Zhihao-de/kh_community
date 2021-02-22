import axios from 'axios'

export const ATTACHMENT_TYPE = {
  PRODUCT_CATEGORY: 1,
  PRODUCT: 2,
  PRODUCT_CAROUSEL: 3,
  PRODUCT_DESCRIPTION: 4
}

/**
 * 删除文件
 * @param items
 * @returns {*}
 */
export function deleteFile (file) {
  return axios
    .delete('/attachments/' + file.response.id + '/', {
      data: {
        url: file.response.url
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
