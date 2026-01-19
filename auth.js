function signup() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    alert("Please fill all fields");
    return;
  }

  if (localStorage.getItem(username)) {
    alert("Username already exists");
    return;
  }

  localStorage.setItem(username, JSON.stringify({ username, password }));
  alert("Signup successful");
  window.location.href = "login.html";
}

function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const user = JSON.parse(localStorage.getItem(username));

  if (user && user.password === password) {
    localStorage.setItem("currentUser", username);
    window.location.href = "dashboard.html";
  } else {
    alert("Invalid username or password");
  }
}
