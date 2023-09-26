document.addEventListener("DOMContentLoaded", function() {
    var passwordIcon1 = document.getElementById("password_icon1");
    var passwordField1 = document.getElementById("password1");

    passwordIcon1.addEventListener("click", function() {
        if (passwordField1.type === "password") {
            passwordField1.type = "text";
            passwordIcon1.classList.remove("fa-eye");
            passwordIcon1.classList.add("fa-eye-slash");
        } else {
            passwordField1.type = "password";
            passwordIcon1.classList.remove("fa-eye-slash");
            passwordIcon1.classList.add("fa-eye");
        }
    });

    var passwordIcon2 = document.getElementById("password_icon2");
    var passwordField2 = document.getElementById("password2");

    passwordIcon2.addEventListener("click", function() {
        if (passwordField2.type === "password") {
            passwordField2.type = "text";
            passwordIcon2.classList.remove("fa-eye");
            passwordIcon2.classList.add("fa-eye-slash");
        } else {
            passwordField2.type = "password";
            passwordIcon2.classList.remove("fa-eye-slash");
            passwordIcon2.classList.add("fa-eye");
        }
    });
});