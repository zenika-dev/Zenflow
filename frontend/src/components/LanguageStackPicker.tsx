import { CheckboxRow } from "@/components/ui/CheckboxRow";
import type { FrameworkOption, StackCatalog } from "@/types/zenflow";

interface LanguageOption {
  key: string;
  label: string;
  archFile: string;
}

// Each language maps to a single row backed by its most specific (non-"None") framework,
// since the real GuidelineSelection stores exactly one backend and one frontend arch file.
function toLanguageOptions(stacks: Record<string, FrameworkOption[]>): LanguageOption[] {
  return Object.entries(stacks).map(([language, frameworks]) => {
    const framework = frameworks[frameworks.length - 1];
    const label = framework.label.startsWith("None") ? language : `${language} — ${framework.label}`;
    return { key: language, label, archFile: framework.arch_file };
  });
}

interface LanguageStackPickerProps {
  catalog: StackCatalog;
  backendArchFile: string;
  frontendArchFile: string;
  onSelectBackend: (archFile: string) => void;
  onSelectFrontend: (archFile: string) => void;
}

export function LanguageStackPicker({
  catalog,
  backendArchFile,
  frontendArchFile,
  onSelectBackend,
  onSelectFrontend,
}: LanguageStackPickerProps) {
  const backendOptions = toLanguageOptions(catalog.backend);
  const frontendOptions = toLanguageOptions(catalog.frontend);

  return (
    <div>
      <div className="mb-2.5 text-[11px] font-extrabold uppercase tracking-[0.1em] text-[#8a8290]">
        Language / Stack
      </div>
      <div className="flex flex-col gap-2.5">
        {backendOptions.map((option) => (
          <CheckboxRow
            key={option.key}
            label={option.label}
            checked={option.archFile === backendArchFile}
            onToggle={() => onSelectBackend(option.archFile === backendArchFile ? "" : option.archFile)}
          />
        ))}
        {frontendOptions.map((option) => (
          <CheckboxRow
            key={option.key}
            label={option.label}
            checked={option.archFile === frontendArchFile}
            onToggle={() => onSelectFrontend(option.archFile === frontendArchFile ? "" : option.archFile)}
          />
        ))}
      </div>
    </div>
  );
}
