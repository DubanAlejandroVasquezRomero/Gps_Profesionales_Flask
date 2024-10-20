document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');

    if (flashMessages.length > 0) {
        flashMessages.forEach(function(message) {
            
            setTimeout(() => {
                message.style.display = 'none';
            }, 3000);

            
            message.addEventListener('click', () => {
                message.style.display = 'none';
            });
        });
    }
});
