import '../styles/main.scss';
import 'materialize-css/dist/js/materialize';

// mobile menu handler
$('.menuOpener').click(function () {
    const _this = $(this);
    const _body = $('body');
    const ico = (_body.hasClass('navRolled')) ? 'menu' : 'close';

    _this.find('i').text(ico);

    _body.toggleClass('navRolled');
});


