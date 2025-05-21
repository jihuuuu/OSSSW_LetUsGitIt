// src/components/ui/Separator.tsx
import React from "react";

export function Separator({ className = "" }: { className?: string }) {
  return <div className={`w-full h-px bg-gray-300 ${className}`} />;
}
