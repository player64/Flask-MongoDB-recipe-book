import M from 'materialize-css/dist/js/materialize.min.js';

// import 'materialize-css/dist/js/materialize.min.js';


// M.AutoInit();

// document.addEventListener('DOMContentLoaded', () => {
    const elems = document.querySelectorAll('#categoryChips');
    const options = {
        autocompleteOptions: {
            data: {
                'Apple': null,
                'Microsoft': null,
                'Google': null
            },
            limit: Infinity,
            minLength: 1
        },
        onChipAdd:  (e, chip) => {
            console.log(chip.innerHTML.indexOf("<i"));
            console.log(chip.innerHTML.substring(0, chip.innerHTML.indexOf("<i")));
        },
        onChipDelete:  (e, chip) => {
            console.log('removed');
            console.log(chip);
        },
    };
    M.Chips.init(elems, options);
// });

    const elems2 = document.querySelectorAll('#cuisineChips');
    const options2 = {
        onChipAdd:  (e, chip) => {
            console.log(chip.innerHTML.indexOf("<i"));
            console.log(chip.innerHTML.substring(0, chip.innerHTML.indexOf("<i")));
        },
        onChipDelete:  (e, chip) => {
            console.log('removed');
            console.log(chip);
        },
    };
    M.Chips.init(elems2, options2);