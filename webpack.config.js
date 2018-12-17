const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: path.resolve(__dirname, 'static/js/index.js'),
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['css-loader'],
            },
        ],
    },
    output: {
      path: path.resolve(__dirname, 'static'),
      filename: 'script.js'
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery"
        })
    ],
};
