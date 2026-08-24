interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

export function Button({ children, onClick, variant = "secondary", disabled = false }: ButtonProps) {
  const variantClasses =
    variant === "primary"
      ? "border-none bg-[#c81c5c] text-white"
      : "border-[1.5px] border-[#e3c9d3] bg-white text-[#161217]";

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`rounded-full px-7 py-3.5 text-[15px] font-bold disabled:cursor-not-allowed disabled:opacity-50 ${
        disabled ? "" : "cursor-pointer"
      } ${variantClasses}`}
    >
      {children}
    </button>
  );
}
