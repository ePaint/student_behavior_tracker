window.top.addEventListener('htmx:afterSwap', function (event) {
    window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'instant',
    });
});