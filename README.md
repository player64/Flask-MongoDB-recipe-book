# Awesome recipes
The application allows user to adding and managing cooking recipes. It allows user to register, like other recipes and displaying them in common way such as order by most recent, most popular, most liked. The recipes could be assigned to categories, cuisines each one has got detailed preparation instructions, allergens list.

## UX
The project is built in the minimal layout. Each recipe has got statistic such views, likes, date created so the user could ordered it own way on archive page. To add recipe a user need to register. The application has implemented simple ACL(access-control-list) protection for example author can't edit / delete recipe someone else.

[The wireframe](https://xd.adobe.com/view/634d2933-4989-4354-4df1-ba55f3eb927e-157c/?fullscreen)

### Features
* Registration user can create own account to add own recipes, like the others and display them
* Authentication by username and password
* Passwords are stored in database as a hash created by 256 bit algorithm
* Orders recipes by: most popular, most liked, most recent
* Displaying user recipes, user liked recipes

### Features to implement
* Add lost password
* Search recipe by name

## Technologies used
* HTML5
* [MongoDB](https://www.mongodb.com/)
    * for storing app data
* [Flask](http://flask.pocoo.org/)
    * for building app backend and app frontend (Jinja templates) 
* ES6 Support via [babel (v7)](https://babeljs.io/)
    * The project uses babel for compiling ES7 to ES5
* [JQuery](https://jquery.com/)
    * The project uses jquery for DOM manipulation and AJAX calls
* [SCSS](https://sass-lang.com/)
    * The project uses SCSS Preprocessors for compiling to CSS
* [Webpack](https://webpack.js.org/)
    * The project uses webpack for bundling the assets
* AdobeXD [wireframe](https://xd.adobe.com/view/634d2933-4989-4354-4df1-ba55f3eb927e-157c/?fullscreen)

## Testing
* Unit test are written to check functionality of the routes on events logins, edit, delete 
* Form unit test are written to check forms validation
* The website has been passed [HTML validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Fawesome-recipes-ci.herokuapp.com%2F)
* The website has been tested on various screen sizes

## Deployment
The application is deployed to [Heroku](https://awesome-recipes-ci.herokuapp.com/)

### Source files
Assets files are in assets folder

### Compiled files
Compiled files are in static folder

### Installation
`npm install`

### Start Dev Server
`npm start`

### Build production version
When you run npm run build we use the mini-css-extract-plugin to move the css to a separate file. The css file gets included in the head of the index.html.

`npm run build`


## Credits
* Recipes were scrapped from [Donal Skehan website](http://www.donalskehan.com/)
* Webpack [boilerplate](https://github.com/wbkd/webpack-starter)




