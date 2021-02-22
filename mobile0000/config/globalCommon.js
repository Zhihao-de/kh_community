export default {
	gData: {
		hasLogin: false
	},
	setGdata(data){
		this.gData = Object.assign({},this.gData,data)
	}
}