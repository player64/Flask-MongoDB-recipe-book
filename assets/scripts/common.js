'use strict';
// mobile menu handler
$('#menuOpener').click(() => {
    const _body = $('body');
    const ico = (_body.hasClass('navRolled')) ? 'menu' : 'close';

    $('#menuOpener i').text(ico);
    _body.toggleClass('navRolled');
});