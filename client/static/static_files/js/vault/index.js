function openPopup(website, username, password, url, note, id) {
  document.getElementById("popup-details-website").textContent = website;
  document.getElementById("popup-details-username").textContent = username;
  document.getElementById("popup-details-password").textContent = password;
  document.getElementById("popup-details-url").textContent = url;
  document.getElementById("popup-details-note").textContent = note;
  document.getElementById("popup-details-id").textContent = id;
  document.getElementById("popup-details-button-copy").onclick = function() {
    copyPassword(password)
  }
  document.getElementById("popup-details-button-edit").onclick = function() {
    editPassword(id, website, username, password, url, note)
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

function openPopupAddPassword() {
  closePopupAdd()
  document.getElementById("popup-addPassword").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
  document.getElementById("id_password").addEventListener("input", function() {
    updateStrengthBar(calculateStrengthBarRank(passwordStrength(document.getElementById("id_password").value)));
  })
}

function closePopupAddPassword() {
  document.getElementById("popup-addPassword").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupChangeMasterPassword() {
  closePopupUserSettings()
  document.getElementById("popup-changeMasterPassword").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupChangeMasterPassword() {
  document.getElementById("popup-changeMasterPassword").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupSettings() {
  document.getElementById("popup-settings").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupSettings() {
  document.getElementById("popup-settings").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupSessions() {
  closePopupSettings()
  document.getElementById("popup-sessions").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupSessions() {
  document.getElementById("popup-sessions").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupSession(name, sessionId) {
  closePopupSessions()
  document.getElementById("id_newSessionName").value = name;
  document.getElementById("id_sessionIdW").value = sessionId;
  document.getElementById("id_SessionDeleteSessionIdW").value = sessionId;
  document.getElementById("popup-session").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupSession() {
  document.getElementById("popup-session").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupUserSettings() {
  closePopupSettings()
  document.getElementById("username").textContent = "Username: " + getCookie('username')
  document.getElementById("email").textContent = "Email: " + getCookie('email')
  document.getElementById('id_image').onchange = function() {
    document.getElementById('image-form').submit();
  };
  document.getElementById("popup-userSettings").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupUserSettings() {
  document.getElementById("popup-userSettings").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupEdit(id, name, username, password, url, note) {
  document.getElementById("id_newName").value = name;
  document.getElementById("id_newUsername").value = username;
  document.getElementById("id_newPassword").value = password;
  document.getElementById("id_newUrl").value = url;
  document.getElementById("id_newNote").value = note;
  document.getElementById("id_popup-edit-id").value = id;
  document.getElementById("popup-edit").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupEdit() {
  document.getElementById("popup-edit").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupExport() {
  closePopupVaultSettings()
  document.getElementById("popup-export").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupExport() {
  document.getElementById("popup-export").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupImport() {
  closePopupVaultSettings()
  document.getElementById('id_file').onchange = function() {
    document.getElementById('import-form').submit();
  };
  document.getElementById("popup-import").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupImport() {
  document.getElementById("popup-import").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupVaultSettings() {
  closePopupSettings()
  document.getElementById("popup-vaultSettings").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupVaultSettings() {
  document.getElementById("popup-vaultSettings").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function openPopupPGConfig() {
  closePopupSettings()
  document.getElementById("id_length").value = getCookie("pGConfigLength")
  document.getElementById("id_smallLetters").checked = getCookie("pGConfigSmallLetters")
  document.getElementById("id_capitalLetters").checked = getCookie("pGConfigCapitalLetters")
  document.getElementById("id_numbers").checked = getCookie("pGConfigNumbers")
  document.getElementById("id_symbols").checked = getCookie("pGConfigSymbols")

  document.getElementById("id_smallLetters").checked = false
  document.getElementById("id_capitalLetters").checked = false
  document.getElementById("id_numbers").checked = false
  document.getElementById("id_symbols").checked = false

  if (getCookie("pGConfigSmallLetters") === "True") {
    document.getElementById("id_smallLetters").checked = true
  }
  if (getCookie("pGConfigCapitalLetters") === "True") {
    document.getElementById("id_capitalLetters").checked = true
  }
  if (getCookie("pGConfigNumbers") === "True") {
    document.getElementById("id_numbers").checked = true
  }
  if (getCookie("pGConfigSymbols") === "True") {
    document.getElementById("id_symbols").checked = true
  }

  document.getElementById("popup-pGConfig").style.display = "flex";
  document.addEventListener('keydown', handleKeyDown);
}

function closePopupPGConfig() {
  document.getElementById("popup-pGConfig").style.display = "none";
  document.removeEventListener('keydown', handleKeyDown);
}

function handleKeyDown(event) {
  if (event.key === "Escape") {
    closePopup();
    closePopupAdd();
    closePopupAddPassword();
    closePopupChangeMasterPassword();
    closePopupDelete();
    closePopupEdit();
    closePopupExport();
    closePopupImport();
    closePopupPGConfig();
    closePopupSession();
    closePopupSessions();
    closePopupSettings();
    closePopupVaultSettings();
  }
}

function handleKeyDownMain(event) {
  if (
    document.activeElement.id === 'search' || 
    document.activeElement.id === 'id_name' || 
    document.activeElement.id === 'id_newName' || 
    document.activeElement.id === 'id_username' || 
    document.activeElement.id === 'id_newUsername' || 
    document.activeElement.id === 'id_password' || 
    document.activeElement.id === 'id_oldPassword' || 
    document.activeElement.id === 'id_newPassword' ||  
    document.activeElement.id === 'id_url' || 
    document.activeElement.id === 'id_newUrl' || 
    document.activeElement.id === 'id_note' || 
    document.activeElement.id === 'id_newNote' ||
    document.activeElement.id === 'id_newSessionName' || 
    document.activeElement.id === 'id_length' || 
    document.getElementById("popup-details").style.display === "flex" ||
    document.getElementById("popup-add").style.display === "flex" ||
    document.getElementById("popup-addPassword").style.display === "flex" ||
    document.getElementById("popup-changeMasterPassword").style.display === "flex" ||
    document.getElementById("popup-delete").style.display === "flex" ||
    document.getElementById("popup-edit").style.display === "flex" ||
    document.getElementById("popup-export").style.display === "flex" ||
    document.getElementById("popup-import").style.display === "flex" ||
    document.getElementById("popup-pGConfig").style.display === "flex" ||
    document.getElementById("popup-session").style.display === "flex" ||
    document.getElementById("popup-sessions").style.display === "flex" ||
    document.getElementById("popup-settings").style.display === "flex" ||
    document.getElementById("popup-userSettings").style.display === "flex" ||
    document.getElementById("popup-vaultSettings").style.display === "flex"
  ) {
    return;
  }
  if (event.key === "a") {
    openPopupAdd();
  }
  if (event.key === "s") {
    openPopupSettings();
  }
  if (event.key === "/") {
    if (event.ctrlKey) {
      document.getElementById('search').value = '';
      document.getElementById('search').focus();
      event.preventDefault();
    } else {
      document.getElementById('search').focus();
      event.preventDefault();
    }
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
  const id_oldPasswordField = document.getElementById("id_oldPassword");
  const newPasswordField = document.getElementById("id_newPassword");
  const toggleIconPassword = document.getElementById("togglePassword");

  if (passwordField.type === "password") {
      passwordField.type = "text";
      id_oldPasswordField.type = "text";
      newPasswordField.type = "text";
      toggleIconPassword.classList.remove("fa-eye");
      toggleIconPassword.classList.add("fa-eye-slash");
  } else {
      passwordField.type = "password";
      id_oldPasswordField.type = "password";
      newPasswordField.type = "password";
      toggleIconPassword.classList.remove("fa-eye-slash");
      toggleIconPassword.classList.add("fa-eye");
  }
}

function editPassword(id, name, username, password, url, note) {
  closePopup()
  openPopupEdit(id, name, username, password, url, note)
}

function simulateAnchorClick(href) {
  const a = document.createElement('a');
  a.href = href;
  a.click();
}

function simulateFieldClick(id) {
  const field = document.getElementById(id);
  field.click();
}

function getCookie(name) {
  let cookie = {};
  document.cookie.split(';').forEach(function(el) {
    let split = el.split('=');
    let value = split.slice(1).join("=").replace(/"/g, '');
    cookie[split[0].trim()] = value;
  })
  return cookie[name];
}

function generatePassword() {
  const smallLetters = getCookie("pGConfigSmallLetters");
  const capitalLetters = getCookie("pGConfigCapitalLetters");
  const numbers = getCookie("pGConfigNumbers");
  const symbols = getCookie("pGConfigSymbols");

  const length = getCookie("pGConfigLength");

  const smallLettersList = 'abcdefghijklmnopqrstuvwxyz';
  const capitalLettersList = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const numbersList = '0123456789';
  const symbolsList = '!@#$%^&*()_+~`|}{[]\?,.';

  let characters = '';
  if (smallLetters === "True") {
    characters += smallLettersList;
  }
  if (capitalLetters === "True") {
    characters += capitalLettersList;
  }
  if (numbers === "True") {
    characters += numbersList;
  }
  if (symbols === "True") {
    characters += symbolsList;
  }

  let result = '';
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    result += characters.charAt(randomIndex);
  }

  document.getElementById("id_password").value = result;
  document.getElementById("id_newPassword").value = result;
}

function passwordStrength(password) {
  let score = 2;

  // Check for length
  if (password.length >= 8) {
    score += 1;
  }

  if (password.length >= 16) {
    score += 1;
  }

  // Check for uppercase letters
  if (/[A-Z]/.test(password)) {
    score += 1;
  }

  // Check for lowercase letters
  if (/[a-z]/.test(password)) {
    score += 1;
  }

  // Check for numbers
  if (/[0-9]/.test(password)) {
    score += 1;
  }

  // Check for special characters
  if (/[^A-Za-z0-9]/.test(password)) {
    score += 1;
  }

  // Check for common patterns (e.g. "qwerty", "123456")
  const commonPatterns = ["qwerty", "123456", "password", "iloveyou"];
  if (commonPatterns.includes(password.toLowerCase())) {
    score -= 2;
  }

  // Check for sequential characters (e.g. "abcde", "12345")
  let sequentialChars = 0;
  for (let i = 0; i < password.length - 2; i++) {
    if (password.charCodeAt(i) === password.charCodeAt(i + 1) - 1 &&
        password.charCodeAt(i + 1) === password.charCodeAt(i + 2) - 1) {
      sequentialChars++;
    }
  }
  if (sequentialChars > 2) {
    score -= 1;
  }

  // Check if password is in common passwords list
  // const fs = require('fs');
  // const commonPasswordsFile = '../../../common-passwords.txt';
  // const commonPasswords = fs.readFileSync(commonPasswordsFile, 'utf8').split('\n');
  // if (commonPasswords.includes(password.toLowerCase())) {
  //   score = 0;
  // }

  // Return the score
  return score;
}

function updateStrengthBar(stage) {
  const strengthBar = document.getElementById('strength-bar');
  const strengthBarInner = document.getElementById('strength-bar-inner');

  strengthBarInner.classList.remove('zero', 'low', 'medium', 'high');
  strengthBarInner.classList.add(stage);
  switch (stage) {
    case 'low':
      strengthBarInner.style.width = '25%';
      break;
    case 'medium':
      strengthBarInner.style.width = '50%';
      break;
    case 'high':
      strengthBarInner.style.width = '100%';
      break;
    case 'zero':
      strengthBarInner.style.width = '100%';
      break;
  }
}

function calculateStrengthBarRank(score) {
  if (score <= 2) {
    return 'zero';
  } else if (score <= 7) {
    return 'low';
  } else if (score <= 11) {
    return 'medium';
  } else {
    return 'high';
  }
}

document.addEventListener('keydown', handleKeyDownMain)