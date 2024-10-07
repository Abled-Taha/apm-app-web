function togglePasswordVisibility() {
  const passwordField = document.getElementById("id_password");
  const rePasswordField = document.getElementById("id_rePassword");
  const toggleIconPassword = document.getElementById("togglePassword");
  const toggleIconRePassword = document.getElementById("toggleRePassword");

  if (passwordField.type === "password") {
      passwordField.type = "text";
      rePasswordField.type = "text";
      toggleIconPassword.classList.remove("fa-eye");
      toggleIconPassword.classList.add("fa-eye-slash");
      toggleIconRePassword.classList.remove("fa-eye");
      toggleIconRePassword.classList.add("fa-eye-slash");
  } else {
      passwordField.type = "password";
      rePasswordField.type = "password";
      toggleIconPassword.classList.remove("fa-eye-slash");
      toggleIconPassword.classList.add("fa-eye");
      toggleIconRePassword.classList.remove("fa-eye-slash");
      toggleIconRePassword.classList.add("fa-eye");
  }
}