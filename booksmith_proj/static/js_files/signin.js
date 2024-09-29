<script>
{% if messages %}
{% for message in messages %}
    Swal.fire({
        icon: '{% if message.tags == "success" %}success{% elif message.tags == "error" %}error{% else %}info{% endif %}',
        title: '{{ message }}',
        showConfirmButton: true,
        timer: 3000
    }).then(() => {
        {% if message.tags == "success" %}
            window.location.href = "{% url 'home' %}";
        {% elif message.tags == "error" %}
        {% endif %}
    });
{% endfor %}
{% endif %}
</script>
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
