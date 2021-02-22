import axios from 'axios'

export function defaultProductCategoryModel() {
  return {
    id: 0,
    parent: null,
    order: 0,
    name: '',
    description: '',
    pic_url: []
  }
}

/**
 * 生成默认产品模型
 * @returns {*}
 */
export function defaultProductModel(categoryId) {
  return {
    id: 0,
    category: categoryId,
    name: '',
    title: '',
    pic_url: [],
    carousal_urls: [],
    description: '',
    weight: 400.0,
    unit: '克',
    purchase_price: 0.0,
    retail_price: 0.0,
    stock: 0,
    flags: 2
  }
}

/**
 * 分割产品图像url列表
 * @param imageUrls 分号分隔的图像url列表
 * @returns {*}
 */
export function splitImageUrls(imageUrls) {
  var urls = []
  const s = imageUrls.trim()
  if (s) {
    // 掉末尾的分号分隔符，避免出现空元素
    urls = s.substring(0, s.length - 1).split(';')
  }
  return urls
}

/**
 * 获取产类类别列表
 * @returns {*}
 */
export function listProductCategories() {
  return axios.get('/products/categories').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 创建或更新产品分类模型
 * @param model 产品分类模型
 * @returns {*}
 */
export function postOrPatchProductCategory(model) {
  if (model.id > 0) {
    return axios.patch('/products/categories/' + model.id + '/', model).then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
  } else {
    return axios.post('/products/categories/', model).then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
  }
}

/**
 * 获取产类类别树
 * @returns {*}
 */
export function listProductCategoryTree() {
  return axios.get('/products/categories/tree').then(
    res => {
      return Promise.resolve(res)
    },
    err => {
      return Promise.reject(err)
    }
  )
}

/**
 * 获取指定类型的分页产品模型列表
 * @param category 产品分类
 * @param page 页索引
 * @returns {*}
 */
export function listProducts(category) {
  return axios
    .get('/products', {
      params: {
        category: category,
  
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

/**
 * 创建或更新产品模型
 * @param model 产品模型
 * @returns {*}
 */
export function postOrPatchProductModel(model) {
  if (model.id > 0) {
    return axios.patch('/products/' + model.id + '/', model).then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
  } else {
    return axios.post('/products/', model).then(
      res => {
        return Promise.resolve(res)
      },
      err => {
        return Promise.reject(err)
      }
    )
  }
}

/**
 * 更新产品状态
 * @param id 产品id
 * @param flags 产品状态
 * @returns {*}
 */
export function patchProductModelByFlags(id, flags) {
  return axios
    .patch('/products/' + id + '/', {
      id: id,
      flags: flags
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
