const API_BASE = "https://2crtp6hxqi.execute-api.us-west-1.amazonaws.com/prod";
let token = null;

async function register() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password })
  });

  const data = await res.json();
  if (res.ok) {
    alert("Registration successful.");
  } else {
    alert("Registration failed: " + (data.detail || "Unknown error"));
    console.error("Register error:", data);
  }
}

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (res.ok && data.access_token) {
    token = data.access_token;
    document.getElementById("task-section").style.display = "block";
    alert("Login successful!");
  } else {
    alert("Login failed: " + (data.detail || "Unknown error"));
    console.error("Login error:", data);
  }
}

function logout() {
  token = null;
  document.getElementById("task-section").style.display = "none";
  alert("Logged out.");
}

async function createTask() {
  const title = document.getElementById("task-title").value;
  const description = document.getElementById("task-description").value;

  const res = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, description })
  });

  const data = await res.json();
  if (res.ok) {
    alert("Task created: " + data.title);
    getTasks();
  } else {
    alert("Task creation failed: " + (data.detail || "Unknown error"));
    console.error("Create task error:", data);
  }
}

async function getTasks() {
  const res = await fetch(`${API_BASE}/tasks`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  const data = await res.json();
  if (res.ok) {
    const list = document.getElementById("task-list");
    list.innerHTML = "<h3>Task List:</h3>" + data.map(task =>
      `<div><strong>${task.title}</strong>: ${task.description}</div>`
    ).join("");
  } else {
    alert("Failed to load tasks: " + (data.detail || "Unknown error"));
    console.error("Get tasks error:", data);
  }
}
