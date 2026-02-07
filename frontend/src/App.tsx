import { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import { getToken, removeToken } from "./api";
import "./App.css";

function App() {
  // Check if user is already logged in (token exists in localStorage)
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(!!getToken());

  function handleLoginSuccess(): void {
    setIsLoggedIn(true);
  }

  function handleLogout(): void {
    removeToken();
    setIsLoggedIn(false);
  }

  // Simple: if no token → show Login, otherwise → show Dashboard
  if (!isLoggedIn) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return <Dashboard onLogout={handleLogout} />;
}

export default App;
