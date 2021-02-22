<template>
  <ProductEditor :model="model" @on-ok="reset"></ProductEditor>
</template>

<script>
import { defaultProductModel } from '@/api/product_api'
import ProductEditor from '@/components/ProductEditor'
export default {
  name: 'ProductEditView',
  components: { ProductEditor },
  data () {
    return {
      model: !this.$route.params.model
        ? defaultProductModel()
        : this.$route.params.model
    }
  },
  methods: {
    reset () {
      this.model = defaultProductModel()
    }
  }
}
</script>

<style></style>
