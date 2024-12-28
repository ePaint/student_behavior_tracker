window.top.addEventListener('htmx:afterRequest', function (event) {
    console.log('HTMX request completed!', event.detail);
    // Scroll to top instantly after each HTMX request
    window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'instant',
    });
});