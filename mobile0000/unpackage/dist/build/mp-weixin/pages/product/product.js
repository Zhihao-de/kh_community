(global["webpackJsonp"]=global["webpackJsonp"]||[]).push([["pages/product/product"],{"456e":function(t,e,n){"use strict";n.r(e);var r=n("9db1"),c=n("ad20");for(var u in c)"default"!==u&&function(t){n.d(e,t,(function(){return c[t]}))}(u);n("cd90");var o,i=n("f0c5"),a=Object(i["a"])(c["default"],r["b"],r["c"],!1,null,null,null,!1,r["a"],o);e["default"]=a.exports},"6cc5":function(t,e,n){"use strict";(function(t){Object.defineProperty(e,"__esModule",{value:!0}),e.default=void 0;var r=c(n("a34a"));function c(t){return t&&t.__esModule?t:{default:t}}function u(t,e,n,r,c,u,o){try{var i=t[u](o),a=i.value}catch(s){return void n(s)}i.done?e(a):Promise.resolve(a).then(r,c)}function o(t){return function(){var e=this,n=arguments;return new Promise((function(r,c){var o=t.apply(e,n);function i(t){u(o,r,c,i,a,"next",t)}function a(t){u(o,r,c,i,a,"throw",t)}i(void 0)}))}}function i(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var a=function(){n.e("components/uni-badge/uni-badge").then(function(){return resolve(n("22ae"))}.bind(null,n)).catch(n.oe)},s={components:{uniBadge:a},data:function(){var t;return{cart:[],productObj:(t={id:"",name:"榴莲",weight:"",purchase_price:0,retail_price:0,flag:1},i(t,"name",0),i(t,"title",0),i(t,"pic_url",""),i(t,"carousal_urls",[]),i(t,"description","这是产品描述"),i(t,"stock",0),t),number:1,role:0}},onShow:function(){},onLoad:function(e){var n=this;return o(r.default.mark((function c(){var u,o;return r.default.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(u=e.id,!u){r.next=17;break}return n.productObj.id=u,r.next=5,n.getGoodsDetail(u);case 5:o=r.sent,n.productObj.name=o.name,n.productObj.category=o.category,n.productObj.retail_price=o.retail_price,n.productObj.purchase_price=o.purchase_price,n.productObj.flags=o.flags,n.productObj.carousal_urls=o.carousal_urls,n.productObj.pic_url='<div style="text-align:center;"><img src="https://img-cdn-qiniu.dcloud.net.cn/uniapp/images/uni@2x.png"/></div>',n.productObj.stock=o.stock,n.productObj.unit=o.unit,n.productObj.description=o.description,n.productObj.created_at=o.created_at;case 17:n.cart=t.getStorageSync("cart"),n.role=t.getStorageSync("userDetail").flags;case 19:case"end":return r.stop()}}),c)})))()},methods:{getGoodsDetail:function(e){var n=this;return new Promise((function(r){t.request({header:{"content-type":"application/x-www-form-urlencoded"},url:n.api.ApiRoot+"products/"+e+"/",method:"GET",success:function(t){r(t.data)},fail:function(t){console.log(t)}})})).catch((function(t){}))},cutNumber:function(){this.number-1>1?this.number=this.number-1:this.number=1},addNumber:function(){this.number=this.number+1},submitCheck:function(){return this.productObj.stock>=this.number||(t.showModal({title:"提示",content:"购买数量大于库存数量,请修改数量！",success:function(t){}}),!1)},goCreateOrder:function(){if(this.submitCheck()){var e=this.productObj.purchase_price*this.number,n=this.number,r=Number(e.toFixed(2));t.navigateTo({url:"/pages/order/createOrder?source=1&total=".concat(r,"&quantity=").concat(n,"&product=").concat(encodeURIComponent(JSON.stringify(this.productObj)))})}},goCreateIntention:function(){if(this.submitCheck()){var e=this.productObj.retail_price*this.number,n=Number(e.toFixed(2));t.navigateTo({url:"/pages/order/createIntention?source=1&quantity=".concat(this.number,"&total=").concat(n,"&product=").concat(encodeURIComponent(JSON.stringify(this.productObj)))})}},addCart:function(){if(this.submitCheck()){var e={product:this.productObj,quantity:this.number};t.setTabBarBadge({index:0,text:"1"}),t.showToast({title:"已加入购物车",content:"已加入购物车"});var n=t.getStorageSync("cart");if(0===n.length)n.push(e);else{for(var r=!1,c=0;c<n.length;c++)n[c].product.id==e.product.id&&(n[c].quantity=n[c].quantity+e.quantity,r=!0);0==r&&n.push(e)}t.setStorageSync("cart",n),t.redirectTo({url:"/pages/category/category"})}}}};e.default=s}).call(this,n("543d")["default"])},"9db1":function(t,e,n){"use strict";n.d(e,"b",(function(){return c})),n.d(e,"c",(function(){return u})),n.d(e,"a",(function(){return r}));var r={uniBadge:function(){return n.e("components/uni-badge/uni-badge").then(n.bind(null,"22ae"))}},c=function(){var t=this,e=t.$createElement;t._self._c},u=[]},ad20:function(t,e,n){"use strict";n.r(e);var r=n("6cc5"),c=n.n(r);for(var u in r)"default"!==u&&function(t){n.d(e,t,(function(){return r[t]}))}(u);e["default"]=c.a},c951:function(t,e,n){},cd90:function(t,e,n){"use strict";var r=n("c951"),c=n.n(r);c.a},dbcb:function(t,e,n){"use strict";(function(t){n("351e"),n("921b");r(n("66fd"));var e=r(n("456e"));function r(t){return t&&t.__esModule?t:{default:t}}t(e.default)}).call(this,n("543d")["createPage"])}},[["dbcb","common/runtime","common/vendor"]]]);