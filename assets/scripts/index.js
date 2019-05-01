import '../styles/main.scss';
import 'materialize-css/dist/js/materialize';


const app = (opt) => {
    $('h1').css('color','red');
    console.log(`Hello ${opt}`);
};

app('webpack');


