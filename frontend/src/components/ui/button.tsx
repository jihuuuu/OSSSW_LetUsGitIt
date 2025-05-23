// src/components/ui/Button.tsx
import React from "react";

export function Button({
  children,
  onClick,
  variant = "default",
  size = "default",
  className = "",
}: {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "default" | "outline" | "ghost";
  size?: "default" | "icon";
  className?: string;
}) {
  const base = "rounded font-medium text-sm transition";

  const variants = {
    default: "bg-blue-600 text-white hover:bg-blue-700",
    outline: "border border-blue-600 text-blue-600 hover:bg-blue-50",
    ghost: "bg-transparent text-gray-700 hover:bg-gray-100",
  };

  const sizes = {
    default: "px-4 py-2",
    icon: "w-10 h-10 p-0 flex items-center justify-center",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}