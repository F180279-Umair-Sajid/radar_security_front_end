document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        fetch('logout/', {
            method: 'POST', headers: {
                'X-CSRFToken': csrfToken
            },
        })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/';
                } else {
                    alert('Error on Logout ');
                }
            });
    });
});
