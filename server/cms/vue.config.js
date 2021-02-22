module.exports = {
  assetsDir: "static",
  lintOnSave: false,
  devServer: {
    host: "localhost",
    port: 8081,
    https: false,
    open: true,
    proxy: {
      "/v1": {
        target: "http://localhost:8080/v1",
        changeOrigin: true,
        pathRewrite: {
          "^/v1": ""
        }
      }
    }
  }
};
