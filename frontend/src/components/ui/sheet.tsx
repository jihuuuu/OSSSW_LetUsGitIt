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
    <div className={`bg-white h-full shadow-lg ${className}`}>
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
  return <div className={className}>{children}</div>;
}

export function SheetFooter({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={className}>{children}</div>;
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
