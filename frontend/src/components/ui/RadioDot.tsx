interface RadioDotProps {
  name: string;
  checked: boolean;
  color: string;
  onSelect: () => void;
  disabled?: boolean;
}

// Bare radio dot with a runtime-supplied color (skill categories each have their own
// accent), unlike RadioRow's fixed brand-pink dot used in the Assistant list.
export function RadioDot({ name, checked, color, onSelect, disabled = false }: RadioDotProps) {
  return (
    <label className={`flex justify-center ${disabled ? "cursor-not-allowed" : "cursor-pointer"}`}>
      <input
        type="radio"
        name={name}
        checked={checked}
        onChange={onSelect}
        disabled={disabled}
        className="sr-only"
      />
      <span
        className={`h-[18px] w-[18px] flex-none rounded-full border-2 ${disabled ? "opacity-40" : ""}`}
        style={{
          borderColor: checked ? color : "#e3c9d3",
          background: checked ? `radial-gradient(circle, ${color} 42%, transparent 46%)` : "transparent",
        }}
      />
    </label>
  );
}
