// JavaScript for QuickCom
console.log('QuickCom initialized');

// Mobile menu toggle
const mobileMenuButton = document.querySelector('.md\\:hidden button');
if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', () => {
        console.log('Mobile menu clicked');
        // Add mobile menu functionality here
    });
}

// Form validation
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        // Add custom validation logic here if needed
        console.log('Form submitted');
    });
});
function showMessageData(button) {
    const id = button.getAttribute('data-id');
    const name = button.getAttribute('data-name');
    const email = button.getAttribute('data-email');
    const subject = button.getAttribute('data-subject');
    const message = button.getAttribute('data-message');
    
    document.getElementById('modalName').textContent = name;
    document.getElementById('modalEmail').textContent = email;
    document.getElementById('modalSubject').textContent = subject;
    document.getElementById('modalMessage').textContent = message;
    document.getElementById('messageModal').classList.remove('hidden');
}

function showMessage(id, name, email, subject, message) {
    document.getElementById('modalName').textContent = name;
    document.getElementById('modalEmail').textContent = email;
    document.getElementById('modalSubject').textContent = subject;
    document.getElementById('modalMessage').textContent = message;
    document.getElementById('messageModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('messageModal').classList.add('hidden');
}

// Close modal on escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});