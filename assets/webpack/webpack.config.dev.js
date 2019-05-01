const Path = require('path');
const Webpack = require('webpack');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = merge(common, {
    mode: 'development',
    devtool: 'cheap-eval-source-map',
    output: {
        chunkFilename: 'js/[name].chunk.js'
    },
    devServer: {
        inline: true,
    },
    plugins: [
        new Webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify('development')
        }),
        new MiniCssExtractPlugin({
            filename: 'css/app.css'
        }),
        new BrowserSyncPlugin(
            // BrowserSync options
            // https://www.browsersync.io/docs/options
            {
                // browse to http://localhost:3000/ during development
                host: 'localhost',
                port: 3000,
                // proxy the Webpack Dev Server endpoint
                // (which should be serving on http://localhost:3100/)
                // through BrowserSync
                proxy: 'http://127.0.0.1:5000/',
                watch: [
                    "*.py",
                    "templates/**/*.html"
                ],
                files: ['./static/css/!*.css', './static/js/!*.js']
            },
            // plugin options
            {
                //         // prevent BrowserSync from reloading the page
                //         // and let Webpack Dev Server take care of this
                // injectCss: true,
                reload: true,
                //         watch: [
                //             "*.py",
                //             "templates/!**/!*.html"
                //         ],
            }
        )
    ],
    module: {
        rules: [
            {
                test: /\.(js)$/,
                include: Path.resolve(__dirname, '../../assets'),
                enforce: 'pre',
                loader: 'eslint-loader',
                options: {
                    emitWarning: true,
                }
            },
            {
                test: /\.(js)$/,
                include: Path.resolve(__dirname, '../../assets'),
                loader: 'babel-loader'
            },
            {
                test: /\.s?css$/i,
                /*include: Path.resolve(__dirname, '../../assets'),
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]*/
                // include: Path.resolve(__dirname, '../../assets'),
                use: ['style-loader', 'css-loader?sourceMap=true', 'sass-loader']
            }
        ]
    },
});
