// src/components/ui/Sheet.tsx
import React from "react";

export function Sheet({
  open,
  children,
}: {
  open: boolean;
  children: React.ReactNode;
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-20 flex justify-end">
      {children}
    </div>
  );
}

export function SheetContent({
  children,
  className = "",
  showCloseButton = true,
}: {
  children: React.ReactNode;
  className?: string;
  showCloseButton?: boolean;
}) {
  return (
    <div className={`w-[400px] max-w-full h-full bg-[var(--card)] text-[var(--card-foreground)] shadow-xl p-6 ${className}`}>
      {children}
    </div>
  );
}

export function SheetHeader({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={`mb-4 ${className}`}>{children}</div>;
}

export function SheetFooter({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={`mt-4 flex justify-end ${className}`}>{children}</div>;
}

export function SheetTitle({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <h2 className={`text-lg font-semibold ${className}`}>{children}</h2>;
}
