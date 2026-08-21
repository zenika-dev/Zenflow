interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary";
}

export function Button({ children, onClick, variant = "secondary" }: ButtonProps) {
  const variantClasses =
    variant === "primary"
      ? "border-none bg-[#c81c5c] text-white"
      : "border-[1.5px] border-[#e3c9d3] bg-white text-[#161217]";

  return (
    <button
      type="button"
      onClick={onClick}
      className={`cursor-pointer rounded-full px-7 py-3.5 text-[15px] font-bold ${variantClasses}`}
    >
      {children}
    </button>
  );
}
