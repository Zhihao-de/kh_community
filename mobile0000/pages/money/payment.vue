<template>
    <view>
        <page-head :title="title"></page-head>
        <view class="uni-padding-wrap">
            <view style="background:#FFF; padding:50rpx 0;">
                <view class="uni-hello-text uni-center">支付金额</text></view>   
                <view class="uni-h1 uni-center uni-common-mt">
                    <text class="rmbLogo">￥</text>
                    <input class="price" type="digit" :value="price" maxlength="4" @input="priceChange" />
                </view>
            </view>
            <view class="uni-btn-v uni-common-mt">
                <!-- #ifdef MP-WEIXIN || MP-QQ -->
                <button type="primary" :loading="loading">微信支付</button>
                <!-- #endif -->
                <!-- #ifdef APP-PLUS -->
                <template v-if="providerList.length > 0">
                    <button v-for="(item,index) in providerList" :key="index" @click="requestPayment(item,index)"
                        :loading="item.loading">{{item.name}}支付</button>
                </template>
                <!-- #endif -->
            </view>
        </view>
    </view>
    </view>
</template>
<script>
    export default {
        data() {
            return {
                title: 'request-payment',
                loading: false,
                price: 1,
                providerList: []
            }
        },
        onLoad: function() {
            // #ifdef APP-PLUS
            uni.getProvider({
                service: "payment",
                success: (e) => {
                    console.log("payment success:" + JSON.stringify(e));
                    let providerList = [];
                    e.provider.map((value) => {
                        switch (value) {
                            case 'alipay':
                                providerList.push({
                                    name: '支付宝',
                                    id: value,
                                    loading: false
                                });
                                break;
                            case 'wxpay':
                                providerList.push({
                                    name: '微信',
                                    id: value,
                                    loading: false
                                });
                                break;
                            default:
                                break;
                        }
                    })
                    this.providerList = providerList;
                },
                fail: (e) => {
                    console.log("获取支付通道失败：", e);
                }
            });
            // #endif
        },
        methods: {
         }
    }
</script>

<style>
    .rmbLogo {
        font-size: 40rpx;
    }
    button {
        background-color: #007aff;
        color: #ffffff;
    }
    .uni-h1.uni-center {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: flex-end;
    }
    .price {
        border-bottom: 1px solid #eee;
        width: 200rpx;
        height: 80rpx;
        padding-bottom: 4rpx;
    }
    .ipaPayBtn {
        margin-top: 30rpx;
    }
</style>