import { SkillRow } from "@/components/SkillRow";
import type { SkillCategory, SkillMode } from "@/types/skills";

interface CategoryCardProps {
  category: SkillCategory;
  expanded: boolean;
  selections: Record<string, SkillMode>;
  onToggleExpand: () => void;
  onSetMode: (skillId: string, mode: SkillMode) => void;
}

export function CategoryCard({ category, expanded, selections, onToggleExpand, onSetMode }: CategoryCardProps) {
  const selectedCount = category.skills.filter((skill) => (selections[skill.id] ?? "none") !== "none").length;

  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-[0_12px_28px_-18px_rgba(60,20,50,0.25)]">
      <button
        type="button"
        onClick={onToggleExpand}
        className="flex w-full cursor-pointer items-center gap-3 px-5 py-4 text-left"
      >
        <div
          className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-[13px] font-bold"
          style={{ background: category.tint, color: category.color }}
        >
          {category.title}
        </div>
        <span className="text-xs font-extrabold text-[#8a8290]">{selectedCount} selected</span>
        <span className="flex-1" />
        <span
          className="inline-block text-[#8a8290] transition-transform duration-150"
          style={{ transform: expanded ? "rotate(180deg)" : "rotate(0deg)" }}
        >
          ▾
        </span>
      </button>
      {expanded && (
        <div className="px-5 pb-5">
          <div
            className="grid gap-2 border-b-[1.5px] border-[#f0e6ec] px-1 pb-2 text-[11px] font-extrabold tracking-[0.08em] text-[#8a8290] uppercase"
            style={{ gridTemplateColumns: "1fr 56px 56px 76px" }}
          >
            <div>Agent</div>
            <div className="text-center">None</div>
            <div className="text-center">Skill</div>
            <div className="text-center leading-tight">Custom agent</div>
          </div>
          {category.skills.map((skill) => (
            <SkillRow
              key={skill.id}
              skill={skill}
              mode={selections[skill.id] ?? "none"}
              color={category.color}
              onChange={(mode) => onSetMode(skill.id, mode)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
