<template>
	<view class="content">
		<view class="title">
			<uni-list>
				<uni-list-item title="总支出:  " :showArrow="false">
					<template v-slot:right="">
						<text style='color:#e55e2a;'>-￥{{expenditure}}</text>
					</template>

				</uni-list-item>

				<uni-list-item title="总收入:  " :showArrow="false">
					<template v-slot:right="">
						<text style='color:#1fc640;'>+￥{{income}}</text>
					</template>

				</uni-list-item>
			</uni-list>
		</view>
		<view>
			<uni-list v-for="item in accountList" :key="item.id">
				<view v-if="item.flags==0" @click="manageAccount('edit',item)">
					<uni-list-item title="支出" :note="item.created_at" :showArrow="false">
						<template v-slot:right="">
							<text style='color:#e55e2a;'>-{{item.amount}}</text>
						</template>
					</uni-list-item>
				</view>
				<view v-else @click="manageAccount('edit',item)">
					<uni-list-item title="收入" :note="item.created_at" :showArrow="false">
						<template v-slot:right="">
							<text style='color:#1fc640;'>+{{item.amount}}</text>
						</template>
					</uni-list-item>
				</view>


			</uni-list>

		</view>
		<button class="add-btn" @click="manageAccount('create',item)">记账</button>

	</view>
</template>

<script>
	import uniList from '@/components/uni-list/uni-list.vue';
	import uniListItem from '@/components/uni-list-item/uni-list-item.vue';


	export default {
		components: {
			uniList,
			uniListItem
		},
		data() {
			return {
				accountList: [],
				income_bills: [],
				expenditure_bills: [],
				expenditure: 0,
				income: 0
			}
		},
		onShow() {
			this.loaddata();
		},
		onLoad() {
			this.income = 0;
			this.expenditure = 0;
		},

		methods: {
			async loaddata() {
				var accounts = await this.getAccountItems();
				this.accountList = accounts;
				this.caculate();
			},
			getAccountItems() {
				let that = this;

				return new Promise(resolve => {
					uni.request({
						header: {
							"content-type": "application/x-www-form-urlencoded"
						},
						url: this.api.ApiRoot + "users/" + uni.getStorageSync("userDetail").id + "/accounts/",

						method: "GET",
						success(res) {
							resolve(res.data);
							console.log(res.data);
						},
						fail(res) {
							console.log(res);
						}
					})
				}).catch((e) => {});
			},
			caculate() {
				for (var x in this.accountList) {
					if (this.accountList[x].flags == 0) {
						var expenditure = Number(this.expenditure) + Number(this.accountList[x].amount);
						this.expenditure = Number(expenditure.toFixed(2));
					} else {
						var income = Number(this.income) + Number(this.accountList[x].amount);
						this.income = Number(income.toFixed(2));
					}
				}
			},

			manageAccount(type, item) {
				uni.navigateTo({
					url: `/pages/account/manageAccount?type=${type}&data=${encodeURIComponent(JSON.stringify(item))}`
				})
			},

		}
	}
</script>

<style lang='scss'>
	.title {
		height: 200upx;
		display: flex;
		text-align: left;
		align-items: center;
		position: relative;

		font-weight: 600;
		color: $font-color-dark;

	}

	.info-box {
		height: 100upx;
		display: flex;
		align-items: center;
		position: relative;
		z-index: 1;

		.expenditure {
			font-size: $font-lg;
			font-weight: 400;
			color: $font-color-dark;
			margin-left: 20upx;
		}

		.income {
			font-size: $font-lg;
			font-weight: 400;
			color: $font-color-dark;
			margin-left: 20upx;
		}
	}


	.add-btn {
		position: fixed;
		left: 30upx;
		right: 30upx;
		bottom: 16upx;
		z-index: 95;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 690upx;
		height: 80upx;
		font-size: 32upx;

		color: #fff;
		background-color: $uni-color-primary;
		border-radius: 10upx;
		box-shadow: 1px 2px 5px rgba(219, 63, 96, 0.4);
	}
</style>
