const Path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const webpack = require('webpack');
const WebpackAssetsManifest = require('webpack-assets-manifest');

module.exports = {
    entry: {
        app: Path.resolve(__dirname, '../scripts/index.js')
    },
    output: {
        path: Path.join(__dirname, '../../static'),
        filename: 'js/[name].js'
    },
    optimization: {
        splitChunks: {
            chunks: 'initial', // async // all
            name: false
        }
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        }),
        new CleanWebpackPlugin(['static'], { root: Path.resolve(__dirname, '../..') }),
        new CopyWebpackPlugin([
            {from: Path.resolve(__dirname, '../images'), to: '../static/images'}
        ]),
        new WebpackAssetsManifest()
    ],
    resolve: {
        alias: {
            '~': Path.resolve(__dirname, '../../assets')
        }
    },
    module: {
        rules: [
            {
                test: /\.mjs$/,
                include: /node_modules/,
                type: 'javascript/auto'
            },
            {
                test: /\.(ico|jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2)(\?.*)?$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[path][name].[ext]'
                    }
                }
            },
        ]
    }
};
