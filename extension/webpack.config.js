const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const copys = [{
  from: './app/manifest.json',
}, {
  from: './app/icon.png',
}]

module.exports = {
  entry: './app/content.ts',
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
    new CopyWebpackPlugin(copys)
  ],
  resolve: {
    extensions: [".ts", ".js" ]
  },
  output: {
    filename: 'content_script.js',
    path: path.resolve(__dirname, 'dist')
  }
};