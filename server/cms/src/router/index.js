import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [

  {
    path: '/',
    name: '主页',
    component: Home,
    children: [{
        path: '/products',
        component: () => import('../views/products/ProductsListView.vue'),
        meta: {
          name: ['商品管理', '商品列表']
        }
      },
      {
        name: 'product_category_edit',
        path: '/products/category',
        component: () =>
          import('../views/products/ProductCategoryEditView.vue'),
        meta: {
          name: ['商品管理', '编辑类别']
        }
      },
      {
        name: 'product_add',
        path: '/products/add',
        component: () => import('../views/products/ProductEditView.vue'),
        meta: {
          name: ['商品管理', '新增商品']
        }
      },
      {
        name: 'product_edit',
        path: '/products/edit',
        component: () => import('../views/products/ProductEditView.vue'),
        meta: {
          name: ['商品管理', '编辑商品']
        }
      },
      {
        path: '/orders',
        component: () => import('../views/orders/OrdersListView.vue'),
        meta: {
          name: ['订单管理', '商品订单']
        }
      },
      {
        name: 'order_view',
        path: '/orders/view',
        component: () => import('../views/orders/OrderDetailView.vue'),
        meta: {
          name: ['订单管理', '商品订单', '订单详情']
        }
      },
      {
        path: '/intentions',
        component: () => import('../views/intentions/IntentionsListView.vue'),
        meta: {
          name: ['订单管理', '留言订单']
        }
      },
      {
        name: 'intention_view',
        path: '/intentions/view',
        component: () => import('../views/intentions/IntentionDetailView.vue'),
        meta: {
          name: ['订单管理', '留言订单', '订单详情']
        }
      },
      {
        path: '/users',
        component: () => import('../views/users/UsersListView.vue'),
        meta: {
          name: ['用户管理']
        }
      },
      {
        name: 'user_view',
        path: '/users/view',
        component: () => import('../views/users/UserDetailView.vue'),
        meta: {
          name: ['用户管理', '用户详情']
        }
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
