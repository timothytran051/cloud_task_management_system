const API_BASE = "https://8ldm9cwpbk.execute-api.us-west-1.amazonaws.com/prod";
let token = null;

async function register() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();
    if (res.ok) {
      alert("Registration successful. You can now log in.");
    } else {
      alert("Registration failed: " + (data.detail || "Unknown error"));
      console.error("Register error:", data);
    }
  } catch (error) {
    console.error("Registration error:", error);
    alert("Registration failed: Network error. Please try again.");
  }
}

async function login() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json" 
      },
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();
    if (res.ok && data.access_token) {
      token = data.access_token;
      document.getElementById("task-section").style.display = "block";
      alert("Login successful!");
      getTasks(); // Automatically load tasks on login
    } else {
      alert("Login failed: " + (data.detail || "Unknown error"));
      console.error("Login error:", data);
    }
  } catch (error) {
    console.error("Login error:", error);
    alert("Login failed: Network error. Please try again.");
  }
}

function logout() {
  token = null;
  document.getElementById("task-section").style.display = "none";
  document.getElementById("task-list").innerHTML = "";
  alert("Logged out successfully.");
}

async function createTask() {
  const title = document.getElementById("task-title").value;
  const description = document.getElementById("task-description").value;
  
  if (!title.trim()) {
    alert("Task title cannot be empty");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ 
        title, 
        description, 
        completed: false 
      })
    });

    const data = await res.json();
    if (res.ok) {
      alert("Task created successfully!");
      document.getElementById("task-title").value = "";
      document.getElementById("task-description").value = "";
      getTasks();
    } else {
      alert("Failed to create task: " + (data.detail || "Unknown error"));
      console.error("Create task error:", data);
    }
  } catch (error) {
    console.error("Create task error:", error);
    alert("Failed to create task: Network error. Please try again.");
  }
}

async function getTasks() {
  try {
    const res = await fetch(`${API_BASE}/tasks`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (res.ok) {
      const data = await res.json();
      const list = document.getElementById("task-list");
      
      if (data.length === 0) {
        list.innerHTML = "<h3>Task List:</h3><p>No tasks found. Create a new task to get started!</p>";
      } else {
        list.innerHTML = `
          <h3>Task List:</h3>
          ${data.map(task => `
            <div class="task-item" style="margin-bottom: 10px; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
              <strong>${task.title}</strong>
              <p>${task.description || '(No description)'}</p>
              <button onclick="deleteTask(${task.id})">Delete</button>
              <button onclick="toggleTaskComplete(${task.id}, ${!task.completed})">
                ${task.completed ? 'Mark Incomplete' : 'Mark Complete'}
              </button>
            </div>
          `).join("")}
        `;
      }
    } else {
      const data = await res.json();
      console.error("Get tasks error:", data);
      if (res.status === 401) {
        alert("Session expired. Please log in again.");
        logout();
      } else {
        alert("Failed to load tasks: " + (data.detail || "Unknown error"));
      }
    }
  } catch (error) {
    console.error("Get tasks error:", error);
    alert("Failed to load tasks: Network error. Please try again.");
  }
}

async function deleteTask(taskId) {
  if (!confirm("Are you sure you want to delete this task?")) {
    return;
  }
  
  try {
    const res = await fetch(`${API_BASE}/tasks/${taskId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (res.ok) {
      alert("Task deleted successfully!");
      getTasks();
    } else {
      const data = await res.json();
      alert("Failed to delete task: " + (data.detail || "Unknown error"));
      console.error("Delete task error:", data);
    }
  } catch (error) {
    console.error("Delete task error:", error);
    alert("Failed to delete task: Network error. Please try again.");
  }
}

async function toggleTaskComplete(taskId, newCompletedState) {
  try {
    const res = await fetch(`${API_BASE}/tasks/${taskId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        completed: newCompletedState
      })
    });

    if (res.ok) {
      getTasks();
    } else {
      const data = await res.json();
      alert("Failed to update task: " + (data.detail || "Unknown error"));
      console.error("Update task error:", data);
    }
  } catch (error) {
    console.error("Update task error:", error);
    alert("Failed to update task: Network error. Please try again.");
  }
}