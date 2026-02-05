import { getScenarios } from "@/lib/api";
import { Scenario } from "@/types/scenario";
import ScenarioCard from "@/components/ScenarioCard";

export default async function Home() {
  let scenarios: Scenario[] = [];
  let error: string | null = null;

  try {
    scenarios = await getScenarios();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load scenarios";
    console.error("Error loading scenarios:", e);
  }

  return (
    <div className="min-h-screen bg-zinc-50 font-sans">
      <main className="container mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-semibold tracking-tight text-black">
            Scenarios
          </h1>
          <p className="mt-2 text-lg text-zinc-600">
            Choose a scenario to practice your conversation skills
          </p>
        </div>

        {error ? (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4">
            <p className="text-red-800">
              Error: {error}. Make sure the API server is running on port 8000.
            </p>
          </div>
        ) : scenarios.length === 0 ? (
          <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-8 text-center">
            <p className="text-zinc-600">
              No scenarios available.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
            {scenarios.map((scenario) => (
              <ScenarioCard key={scenario.id} scenario={scenario} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
