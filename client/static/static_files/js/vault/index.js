function openPopup(website, username, password, url, id) {
  document.getElementById("popup-details-website").textContent = website;
  document.getElementById("popup-details-username").textContent = username;
  document.getElementById("popup-details-password").textContent = password;
  document.getElementById("popup-details-url").textContent = url;
  document.getElementById("popup-details-id").textContent = id;
  document.getElementById("popup-details-button-copy").onclick = function() {
    copyPassword(password)
  }
  document.getElementById("popup-details-button-edit").onclick = function() {
    editPassword(id, website, username, password, url)
  }
  document.getElementById("popup-details").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopup() {
  document.getElementById("popup-details").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function copyPassword(password) {
navigator.clipboard.writeText(password).then(function() {
    alert("Password copied!");
}, function(err) {
    console.error("Could not copy password: ", err);
});
}

function openPopupDelete(id) {
  document.getElementById("id_id").setAttribute('value', id)
  document.getElementById("popup-delete").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupDelete() {
  document.getElementById("popup-delete").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupAdd() {
  document.getElementById("popup-add").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupAdd() {
  document.getElementById("popup-add").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupEdit(id, name, username, password, url) {
  document.getElementById("id_newName").value = name;
  document.getElementById("id_newUsername").value = username;
  document.getElementById("id_newPassword").value = password;
  document.getElementById("id_newUrl").value = url;
  document.getElementById("id_popup-edit-id").value = id;
  document.getElementById("popup-edit").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupEdit() {
  document.getElementById("popup-edit").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function handleKeyDown(event) {
  if (event.key === "Escape") {
    closePopup();
    closePopupDelete();
    closePopupAdd();
    closePopupEdit();
  }
}

function filterVault() {
  const searchValue = document.getElementById('search').value.toLowerCase();
  const vaultItems = document.querySelectorAll('.vault-item');

  vaultItems.forEach(item => {
      const itemName = item.querySelector('h3').textContent.toLowerCase();
      const itemUsername = item.querySelector('p').textContent.toLowerCase();
      
      if (itemName.includes(searchValue) || itemUsername.includes(searchValue)) {
          item.style.display = '';
      } else {
          item.style.display = 'none';
      }
  });
}

function togglePasswordVisibility() {
  const passwordField = document.getElementById("id_password");
  const newPasswordField = document.getElementById("id_newPassword");
  const toggleIconPassword = document.getElementById("togglePassword");

  if (passwordField.type === "password") {
      passwordField.type = "text";
      newPasswordField.type = "text";
      toggleIconPassword.classList.remove("fa-eye");
      toggleIconPassword.classList.add("fa-eye-slash");
  } else {
      passwordField.type = "password";
      newPasswordField.type = "password";
      toggleIconPassword.classList.remove("fa-eye-slash");
      toggleIconPassword.classList.add("fa-eye");
  }
}

function editPassword(id, name, username, password, url) {
  closePopup()
  openPopupEdit(id, name, username, password, url)
}