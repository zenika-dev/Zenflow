interface RadioDotProps {
  name: string;
  checked: boolean;
  color: string;
  onSelect: () => void;
}

// Bare radio dot with a runtime-supplied color (skill categories each have their own
// accent), unlike RadioRow's fixed brand-pink dot used in the Assistant list.
export function RadioDot({ name, checked, color, onSelect }: RadioDotProps) {
  return (
    <label className="flex cursor-pointer justify-center">
      <input type="radio" name={name} checked={checked} onChange={onSelect} className="sr-only" />
      <span
        className="h-[18px] w-[18px] flex-none rounded-full border-2"
        style={{
          borderColor: checked ? color : "#e3c9d3",
          background: checked ? `radial-gradient(circle, ${color} 42%, transparent 46%)` : "transparent",
        }}
      />
    </label>
  );
}
