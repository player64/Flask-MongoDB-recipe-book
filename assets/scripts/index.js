import '../styles/main.scss';
import 'materialize-css/dist/js/materialize';
import './common';
import {recipeEdit} from './recipes';

// clone fields = https://codepen.io/ALTELMA/pen/ObPdZG

if($('body').hasClass('edit_recipe')) {
     recipeEdit();
}