// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            button.classList.add('liked');
            setTimeout(() => {
                window.location.href = button.href;
            }, 500); // Adjust the delay to match the animation duration
        });
    });
});
