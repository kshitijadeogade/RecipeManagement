// Highlight active nav link (optional improvement)
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function () {
        document.querySelectorAll('nav a').forEach(el => el.classList.remove('active'));
        this.classList.add('active');
    });
});
