const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#pass1');

// Add a click event listener to the togglePassword icon
togglePassword.addEventListener('click', function () {
    // Toggle the type attribute between 'password' and 'text'
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    
    // Toggle the eye / eye-slash icon
    this.classList.toggle('fa-eye-slash');
});
