// src/components/ui/pagination.tsx
import * as React from "react";
import { cn } from "@/lib/utils"; // className join helper

export function Pagination({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <nav role="navigation" aria-label="pagination" className={cn("flex justify-center mt-6", className)} {...props} />
  );
}

export function PaginationContent({ className, ...props }: React.HTMLAttributes<HTMLUListElement>) {
  return <ul className={cn("flex flex-wrap items-center gap-2", className)} {...props} />;
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
        "px-4 py-2 rounded-xl text-sm font-medium transition-colors duration-200 shadow-sm",
        isActive
          ? "bg-blue-500 text-white"
          : "bg-white text-gray-700 hover:bg-gray-100 border border-gray-300",
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
        "px-3 py-2 rounded-md inline-flex items-center text-sm font-medium text-gray-600 hover:bg-gray-100 border border-gray-300",
        className
      )}
      {...props}
    >
      ◀ 이전
    </a>
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
        "px-3 py-2 rounded-md inline-flex items-center text-sm font-medium text-gray-600 hover:bg-gray-100 border border-gray-300",
        className
      )}
      {...props}
    >
      다음 ▶
    </a>
  );
}

export function PaginationEllipsis({
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      aria-hidden
      className={cn("px-3 py-2 text-sm font-medium text-gray-400", className)}
      {...props}
    >
      ...
    </span>
  );
}
