import { CategoryCard } from "@/components/CategoryCard";
import type { SkillCategory, SkillMode } from "@/types/skills";

interface SkillCategoryAccordionProps {
  categories: SkillCategory[];
  expandedCategory: string | null;
  selections: Record<string, SkillMode>;
  onToggleExpand: (categoryId: string) => void;
  onSetMode: (skillId: string, mode: SkillMode) => void;
}

export function SkillCategoryAccordion({
  categories,
  expandedCategory,
  selections,
  onToggleExpand,
  onSetMode,
}: SkillCategoryAccordionProps) {
  return (
    <div className="flex flex-col gap-3">
      {categories.map((category) => (
        <CategoryCard
          key={category.id}
          category={category}
          expanded={expandedCategory === category.id}
          selections={selections}
          onToggleExpand={() => onToggleExpand(category.id)}
          onSetMode={onSetMode}
        />
      ))}
    </div>
  );
}
