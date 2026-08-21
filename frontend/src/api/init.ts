import { API_BASE_URL } from "@/api/config";
import type { InitRequest, InitResponse } from "@/types/zenflow";

export async function initProject(request: InitRequest): Promise<InitResponse> {
  const response = await fetch(`${API_BASE_URL}/init`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = data && typeof data === "object" && "detail" in data ? String(data.detail) : undefined;
    throw new Error(detail ?? `Request failed (${response.status})`);
  }
  return data as InitResponse;
}
