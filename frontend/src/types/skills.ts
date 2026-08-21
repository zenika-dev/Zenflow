// Skill-category data is a frontend-only concept for now — the backend deploys
// a fixed set of agents per tool and has no per-skill selection endpoint yet.

export type SkillMode = "none" | "skill" | "custom";

export interface Skill {
  id: string;
  label: string;
}

export interface SkillCategory {
  id: string;
  title: string;
  color: string;
  tint: string;
  skills: Skill[];
}
