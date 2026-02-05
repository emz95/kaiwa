import { Scenario } from "@/types/scenario";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getScenarios(): Promise<Scenario[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/scenarios`, {
      cache: "no-store", // Always fetch fresh data
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch scenarios: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching scenarios:", error);
    throw error;
  }
}
