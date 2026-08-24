import { API_BASE_URL } from "@/api/config";
import type { StackCatalog } from "@/types/zenflow";

export async function getStacks(): Promise<StackCatalog> {
  const response = await fetch(`${API_BASE_URL}/stacks`);
  if (!response.ok) {
    throw new Error(`Failed to load stacks (${response.status})`);
  }
  return response.json();
}
