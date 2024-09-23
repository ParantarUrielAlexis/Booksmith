document.addEventListener('DOMContentLoaded', function () {
    const birthdateInput = document.getElementById("birthdate");

    
    flatpickr(birthdateInput, {
        dateFormat: "Y-m-d", 
        maxDate: "today",    
        onChange: function(selectedDates, dateStr) {
            birthdateInput.value = dateStr;
        },
        onOpen: function() {
            if (birthdateInput.value === "") {
                birthdateInput.setAttribute("placeholder", "");
            }
        },
        onClose: function() {
            if (birthdateInput.value === "") {
                birthdateInput.setAttribute("placeholder", "Birthdate");
            }
        }
    });

    if (!birthdateInput.value) {
        birthdateInput.setAttribute("placeholder", "Birthdate");
    }
});
const genderInput = document.getElementById('gender');
const dropdownMenu = document.querySelector('.dropdown-menu');
const dropdownItems = document.querySelectorAll('.dropdown-menu li');

genderInput.addEventListener('click', function() {
    genderInput.placeholder = ''; 
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
});

dropdownItems.forEach(function(item) {
    item.addEventListener('click', function() {
        genderInput.value = item.textContent; 
        genderInput.setAttribute('data-value', item.getAttribute('data-value')); 
        dropdownMenu.style.display = 'none'; 
    });
});

document.addEventListener('click', function(event) {
    if (!genderInput.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.style.display = 'none';
        
        if (genderInput.value === '') {
            genderInput.placeholder = 'Gender'; 
        }
    }
});


