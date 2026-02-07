import { useState } from "react";
import { login } from "../api";
import "./Login.css";

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault(); // Prevent page reload
    setError(""); // Clear previous errors
    setLoading(true);

    try {
      await login(username, password);
      onLoginSuccess(); // Tell App.jsx that login worked
    } catch (err) {
      setError(err.message); // Show error to user
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h1>SOX Compliance Monitor</h1>
        <p className="login-subtitle">Sign in to view system metrics</p>

        {error && <div className="error-message">{error}</div>}

        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
          required
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter password"
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Sign In"}
        </button>

        <p className="login-hint">
          Sample: <strong>admin / admin123</strong> or{" "}
          <strong>viewer / viewer123</strong>
        </p>
      </form>
    </div>
  );
}

export default Login;
