// src/components/ui/pagination.tsx
import * as React from "react";
import { cn } from "@/lib/utils"; // 유틸 없으면 그냥 className 합쳐서 써도 됨

export function Pagination({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <nav role="navigation" aria-label="pagination" className={cn("flex justify-center", className)} {...props} />
  );
}

export function PaginationContent({ className, ...props }: React.HTMLAttributes<HTMLUListElement>) {
  return <ul className={cn("flex flex-wrap items-center", className)} {...props} />;
}

export function PaginationItem({ className, ...props }: React.LiHTMLAttributes<HTMLLIElement>) {
  return <li className={cn("list-none", className)} {...props} />;
}

export function PaginationLink({
  isActive = false,
  className,
  ...props
}: React.AnchorHTMLAttributes<HTMLAnchorElement> & { isActive?: boolean }) {
  return (
    <a
      aria-current={isActive ? "page" : undefined}
      className={cn(
        "px-4 py-2 rounded-[var(--size-radius-200)] text-sm font-medium transition-colors",
        isActive
          ? "bg-[#77aafb] text-color-text-brand-on-brand"
          : "text-color-text-default-default hover:bg-gray-100",
        className
      )}
      {...props}
    />
  );
}

export function PaginationPrevious({
  className,
  ...props
}: React.AnchorHTMLAttributes<HTMLAnchorElement>) {
  return (
    <a
      aria-label="Go to previous page"
      className={cn(
        "px-[var(--size-space-300)] py-[var(--size-space-200)] rounded-[var(--size-radius-200)] inline-flex items-center gap-[var(--size-space-200)] text-sm font-medium text-color-text-default-secondary hover:bg-gray-100",
        className
      )}
      {...props}
    />
  );
}

export function PaginationNext({
  className,
  ...props
}: React.AnchorHTMLAttributes<HTMLAnchorElement>) {
  return (
    <a
      aria-label="Go to next page"
      className={cn(
        "px-[var(--size-space-300)] py-[var(--size-space-200)] rounded-[var(--size-radius-200)] inline-flex items-center gap-[var(--size-space-200)] text-sm font-medium text-color-text-default-secondary hover:bg-gray-100",
        className
      )}
      {...props}
    />
  );
}

export function PaginationEllipsis({
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      aria-hidden
      className={cn(
        "px-[var(--size-space-400)] py-[var(--size-space-200)] inline-flex items-center justify-center text-sm font-semibold text-color-text-default-secondary",
        className
      )}
      {...props}
    >
      ...
    </span>
  );
}
