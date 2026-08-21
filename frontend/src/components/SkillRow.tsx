import { RadioDot } from "@/components/ui/RadioDot";
import type { Skill, SkillMode } from "@/types/skills";

interface SkillRowProps {
  skill: Skill;
  mode: SkillMode;
  color: string;
  onChange: (mode: SkillMode) => void;
}

export function SkillRow({ skill, mode, color, onChange }: SkillRowProps) {
  return (
    <div
      className="grid items-center gap-2 border-b border-[#f6f0f3] py-2.5"
      style={{ gridTemplateColumns: "1fr 56px 56px 76px" }}
    >
      <div className={`text-[13px] font-bold ${mode === "none" ? "opacity-40" : ""}`}>{skill.label}</div>
      <RadioDot name={skill.id} color="#8a8290" checked={mode === "none"} onSelect={() => onChange("none")} />
      <RadioDot name={skill.id} color={color} checked={mode === "skill"} onSelect={() => onChange("skill")} />
      <RadioDot name={skill.id} color={color} checked={mode === "custom"} onSelect={() => onChange("custom")} />
    </div>
  );
}
