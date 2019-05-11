import '../styles/main.scss';
import 'materialize-css/dist/js/materialize';
import './common';
import {recipeEdit} from './recipes';
import {archiveView} from './archive';
import {createStatsChart} from './recipe_stats';


const _body = $('body');

if(_body.hasClass('edit_recipe')) {
     recipeEdit();
}

if(_body.hasClass('archive')) {
     archiveView();
}

if (_body.hasClass('single_recipe')) {
     createStatsChart();
}
