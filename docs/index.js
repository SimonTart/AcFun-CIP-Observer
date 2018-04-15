(function() {
    function closeAllAlert() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            alert.classList.remove('active');
        });
    }

    function intialAlert(name) {
        const button = document.querySelector('.' + name);
        const alert = document.querySelector('.' + name + '-alert');
        button.addEventListener('click', function() {
            closeAllAlert();
            alert.classList.add('active')
        });
    }


    intialAlert('upgrade-log');
    intialAlert('public-notice');
    intialAlert('contact-author');

    document.querySelectorAll('.alert .alert-close').forEach(function(close) {
        close.addEventListener('click', function() {
            closeAllAlert();
        });
    });
})();