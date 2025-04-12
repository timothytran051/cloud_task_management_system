const API_BASE = "https://2crtp6hxqi.execute-api.us-west-1.amazonaws.com/prod";
let token = null;

async function registerUser() {
  const username = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;

  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password })
  });

  const data = await res.json();
  alert(data.message || data.detail || "Register response logged.");
  console.log(data);
}

async function loginUser() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (data.access_token) {
    token = data.access_token;
    alert("Login successful!");
    loadTasks();
  } else {
    alert(data.detail || "Login failed.");
  }
}

async function loadTasks() {
  if (!token) return alert("Login first.");
  const res = await fetch(`${API_BASE}/tasks`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const tasks = await res.json();
  console.log("Tasks:", tasks);
  alert(`Loaded ${tasks.length} task(s).`);
}
