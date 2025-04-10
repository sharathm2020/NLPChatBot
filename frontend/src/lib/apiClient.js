const API_BASE_URL = "http://localhost:8000"; // Your FastAPI backend URL

async function handleResponse(response) {
  if (!response.ok) {
    let errorData;
    try {
        errorData = await response.json();
    } catch (e) {
        errorData = { detail: response.statusText || "Unknown error" };
    }
    console.error("API Error Response:", errorData);
    // Use the 'detail' field from FastAPI's HTTPException or default text
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  // Handle cases where response might be empty (e.g., 204 No Content)
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
       return response.json(); // Parse JSON body on success
  }
  return response.text(); // Or return text/empty if not JSON
}

export async function apiSignUp(email, password, fullName) {
  const response = await fetch(`${API_BASE_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password, full_name: fullName }), // Match FastAPI schema
  });
  return handleResponse(response);
}

export async function apiSignIn(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/signin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }), // Match FastAPI schema
  });
  return handleResponse(response);
}

export async function sendMessage(message, token) {
    const response = await fetch(`${API_BASE_URL}/chat/`, { // Ensure trailing slash if needed by FastAPI router
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`, // Send the token
      },
      body: JSON.stringify({ message }), // Match FastAPI schema ChatRequest
    });
    return handleResponse(response);
}

// --- NEW API Functions ---

export async function getTodos(token) {
    if (!token) throw new Error("Authentication token is required.");
    const response = await fetch(`${API_BASE_URL}/todos/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    });
    return handleResponse(response);
}

export async function getChatHistory(token) {
    if (!token) throw new Error("Authentication token is required.");
    const response = await fetch(`${API_BASE_URL}/chat/history`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    });
    return handleResponse(response);
}

// Add other API call functions here as needed (e.g., for fetching chat history, etc.)
