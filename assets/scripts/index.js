import '../styles/main.scss';

const app = (opt) => {
    $('h1').css('color','red');
    console.log(`init ${opt}`);

    $('body').append(`<h1>Smash !!</h1>`);
};

app('webpack');


