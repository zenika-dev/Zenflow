interface RadioRowProps {
  label: string;
  checked: boolean;
  onSelect: () => void;
}

export function RadioRow({ label, checked, onSelect }: RadioRowProps) {
  return (
    <label className="flex cursor-pointer items-center gap-2.5 text-sm font-semibold text-[#161217]">
      <input type="radio" checked={checked} onChange={onSelect} className="sr-only" />
      <span
        className={`h-[18px] w-[18px] flex-none rounded-full border-2 ${
          checked
            ? "border-[#c81c5c] bg-[radial-gradient(circle,#c81c5c_42%,transparent_46%)]"
            : "border-[#e3c9d3]"
        }`}
      />
      {label}
    </label>
  );
}
