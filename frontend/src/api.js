/**
 * API Helper - Handles all API calls and token management.
 *
 * Token is stored in localStorage so it survives page refreshes.
 * Every protected API call automatically includes the token.
 */

// ==================== Token Management ====================

function getToken() {
  return localStorage.getItem("token");
}

function saveToken(token) {
  localStorage.setItem("token", token);
}

function removeToken() {
  localStorage.removeItem("token");
}

// ==================== API Calls ====================

/**
 * Login - sends username & password to get an access token.
 * Note: FastAPI expects form-encoded data, NOT JSON.
 */
async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch("/auth/login", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Login failed");
  }

  const data = await response.json();
  saveToken(data.access_token);
  return data;
}

/**
 * Fetch with auth - automatically attaches the Bearer token.
 * If token is expired (401), clears token and reloads page.
 */
async function fetchWithAuth(url) {
  const token = getToken();

  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status === 401) {
    removeToken();
    window.location.reload();
    return null;
  }

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export { getToken, saveToken, removeToken, login, fetchWithAuth };
