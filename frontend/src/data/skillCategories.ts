import type { SkillCategory } from "@/types/skills";

export const SKILL_CATEGORIES: SkillCategory[] = [
  {
    id: "discovery",
    title: "Product and Design",
    color: "#c81c5c",
    tint: "#fbe7ee",
    disabled: true, // no backend support yet
    skills: [
      { id: "prd-generation", label: "PRD generation" },
      { id: "low-fi-design", label: "Low-fi design" },
      { id: "dynamic-prototyping", label: "Dynamic prototyping" },
      { id: "data-exploration", label: "Data exploration" },
    ],
  },
  {
    id: "developer",
    title: "Development",
    color: "#1c8a5c",
    tint: "#e6f5ee",
    skills: [
      { id: "backend", label: "Backend" },
      { id: "frontend", label: "Frontend" },
      { id: "documentation", label: "Documentation" },
      { id: "tech-migration", label: "Tech Migration" },
      { id: "code-review", label: "Code review" },
    ],
  },
  {
    id: "qa",
    title: "QA",
    color: "#7c4fd6",
    tint: "#efe9fc",
    skills: [
      { id: "playwright-scripts", label: "Script generation with Playwright" },
      { id: "playwright-exploratory", label: "Exploratory testing with Playwright" },
    ],
  },
];
