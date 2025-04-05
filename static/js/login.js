const form = document.getElementById('form');
const toggleLink = document.getElementById('toggle-link');
const formTitle = document.getElementById('form-title');
const formSubtitle = document.getElementById('form-subtitle');
const formBtn = document.getElementById('form-btn');
const nameField = document.getElementById('name-field');
const phoneField = document.getElementById('phone-field');

let isLogin = true;

toggleLink.addEventListener('click', (e) => {
    e.preventDefault();
    isLogin = !isLogin;

    if (isLogin) {
        formTitle.textContent = 'Welcome Back';
        formSubtitle.textContent = 'Sign in to continue';
        formBtn.textContent = 'Login';
        toggleLink.textContent = 'Sign up';
        nameField.style.display = 'block';
        phoneField.style.display = 'block';
    } else {
        formTitle.textContent = 'Create Account';
        formSubtitle.textContent = 'Sign up to get started';
        formBtn.textContent = 'Sign Up';
        toggleLink.textContent = 'Login';
        nameField.style.display = 'block';
        phoneField.style.display = 'block';
    }
});

form.addEventListener('submit', function (event) {
    event.preventDefault();
    alert(isLogin ? 'Login submitted!' : 'Signup submitted!');
});
