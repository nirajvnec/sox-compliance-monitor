/**
 * API Helper - Handles all API calls and token management.
 *
 * Token is stored in localStorage so it survives page refreshes.
 * Every protected API call automatically includes the token.
 */

// ==================== Types ====================

export interface LoginResponse {
  access_token: string;
  token_type: string;
  username: string;
  role: string;
  message: string;
}

export interface SystemInfo {
  hostname: string;
  platform: string;
  python_version: string;
  requested_by: string;
}

export interface CpuData {
  cpu_percent: number;
  cpu_cores: number;
}

export interface MemoryData {
  memory_percent: number;
  total_gb: number;
  used_gb: number;
  free_gb: number;
}

export interface DiskData {
  disk_percent: number;
  total_gb: number;
  used_gb: number;
  free_gb: number;
}

export interface ComplianceCheck {
  check: string;
  value: string;
  threshold: string;
  status: "PASS" | "FAIL";
}

export interface ComplianceData {
  report_time: string;
  score: string;
  overall: "COMPLIANT" | "NON-COMPLIANT";
  checks: ComplianceCheck[];
  checked_by: string;
}

// ==================== Token Management ====================

export function getToken(): string | null {
  return localStorage.getItem("token");
}

export function saveToken(token: string): void {
  localStorage.setItem("token", token);
}

export function removeToken(): void {
  localStorage.removeItem("token");
}

// ==================== API Calls ====================

/**
 * Login - sends username & password to get an access token.
 * Note: FastAPI expects form-encoded data, NOT JSON.
 */
export async function login(
  username: string,
  password: string
): Promise<LoginResponse> {
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

  const data: LoginResponse = await response.json();
  saveToken(data.access_token);
  return data;
}

/**
 * Fetch with auth - automatically attaches the Bearer token.
 * If token is expired (401), clears token and reloads page.
 */
export async function fetchWithAuth<T>(url: string): Promise<T | null> {
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

  return response.json() as Promise<T>;
}
