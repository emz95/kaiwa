"use client";

import { Scenario } from "@/types/scenario";

interface ScenarioCardProps {
  scenario: Scenario;
}

export default function ScenarioCard({ scenario }: ScenarioCardProps) {
  return (
    <div
      className="group aspect-square cursor-pointer rounded-lg border border-zinc-200 bg-zinc-100 p-4 transition-all hover:scale-[1.02] hover:border-zinc-300 hover:shadow-lg flex flex-col justify-center"
      onClick={() => {
        // Placeholder for future navigation
        console.log("Clicked scenario:", scenario.slug);
      }}
    >
      <h2 className="mb-1 text-lg font-semibold text-black transition-colors group-hover:text-zinc-700">
        {scenario.name}
      </h2>
      {scenario.description && (
        <p className="text-xs text-zinc-600">
          {scenario.description}
        </p>
      )}
    </div>
  );
}
