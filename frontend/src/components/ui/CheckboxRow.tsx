interface CheckboxRowProps {
  label: string;
  checked: boolean;
  onToggle: () => void;
}

export function CheckboxRow({ label, checked, onToggle }: CheckboxRowProps) {
  return (
    <label className="flex cursor-pointer items-center gap-2.5 text-sm font-semibold text-[#161217]">
      <input type="checkbox" checked={checked} onChange={onToggle} className="sr-only" />
      <span
        className={`flex h-[18px] w-[18px] flex-none items-center justify-center rounded-[5px] border-2 ${
          checked ? "border-[#c81c5c] bg-[#c81c5c]" : "border-[#e3c9d3] bg-transparent"
        }`}
      >
        {checked && (
          <svg
            width="11"
            height="11"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#fff"
            strokeWidth={3}
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polyline points="20 6 9 17 4 12" />
          </svg>
        )}
      </span>
      {label}
    </label>
  );
}
