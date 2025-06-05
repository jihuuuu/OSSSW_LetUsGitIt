// src/components/ui/Button.tsx
import React from "react";

type ButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "default" | "outline" | "ghost";
  size?: "default" | "icon";
  className?: string;
  disabled?: boolean;
};

export function Button({
  children,
  onClick,
  variant = "default",
  size = "default",
  className = "",
  disabled = false,
}: ButtonProps) {
  const base = "rounded-md font-medium text-sm transition-colors duration-200 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed";

  const variants = {
    default: "bg-sky-500 text-white hover:bg-sky-600",
    outline: "border border-sky-500 text-sky-500 hover:bg-sky-50",
    ghost: "bg-transparent text-sky-600 hover:bg-sky-100",
  };

  const sizes = {
    default: "px-4 py-2",
    icon: "w-10 h-10 p-0 flex items-center justify-center",
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
    >
      {children}
    </button>
  );
}
