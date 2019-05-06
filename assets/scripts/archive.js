import M from 'materialize-css/dist/js/materialize.min.js';

export function archiveView() {
    document.addEventListener('DOMContentLoaded', function () {
        const elems = document.querySelectorAll('select');
        M.FormSelect.init(elems, {});
        $("#orderBy").on('change', function () {
            window.location.href = $(this).val();
        });
    });
}