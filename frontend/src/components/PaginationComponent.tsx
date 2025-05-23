// src/components/PaginationComponent.tsx
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { ChevronLeft, ChevronRight } from "lucide-react";
import React from "react";
import type { Note } from "@/types/note"; 

type PaginationComponentProps = {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
};

const PaginationComponent = ({
  currentPage,
  totalPages,
  onPageChange,
}: PaginationComponentProps) => {
  const getPages = () => {
    const pages: (number | "...")[] = [];

    if (totalPages <= 5) {
      for (let i = 1; i <= totalPages; i++) pages.push(i);
    } else {
      pages.push(1);
      if (currentPage > 3) pages.push("...");

      const middleStart = Math.max(2, currentPage - 1);
      const middleEnd = Math.min(totalPages - 1, currentPage + 1);

      for (let i = middleStart; i <= middleEnd; i++) {
        pages.push(i);
      }

      if (currentPage < totalPages - 2) pages.push("...");
      pages.push(totalPages);
    }

    return pages;
  };

  return (
    <Pagination className="inline-flex items-center gap-[var(--size-space-200)]">
      <PaginationContent className="gap-[var(--size-space-200)]">
        <PaginationItem>
          <PaginationPrevious
            href="#"
            onClick={(e) => {
              e.preventDefault();
              if (currentPage > 1) onPageChange(currentPage - 1);
            }}
            className={`inline-flex items-center px-[var(--size-space-300)] py-[var(--size-space-200)] rounded-[var(--size-radius-200)] ${
              currentPage === 1 ? "opacity-50 pointer-events-none" : ""
            }`}
          >
            <ChevronLeft className="h-4 w-4" />
            <span className="text-sm">Previous</span>
          </PaginationPrevious>
        </PaginationItem>

        {getPages().map((page, index) =>
          page === "..." ? (
            <PaginationItem key={`ellipsis-${index}`}>
              <PaginationEllipsis />
            </PaginationItem>
          ) : (
            <PaginationItem key={page}>
              <PaginationLink
                href="#"
                isActive={page === currentPage}
                onClick={(e) => {
                  e.preventDefault();
                  onPageChange(page);
                }}
                className={`inline-flex items-center justify-center px-[var(--size-space-300)] py-[var(--size-space-200)] rounded-[var(--size-radius-200)] ${
                  page === currentPage ? "bg-[#77aafb]" : ""
                }`}
              >
                <span
                  className={`text-sm font-medium ${
                    page === currentPage
                      ? "text-color-text-brand-on-brand"
                      : "text-color-text-default-default"
                  }`}
                >
                  {page}
                </span>
              </PaginationLink>
            </PaginationItem>
          )
        )}

        <PaginationItem>
          <PaginationNext
            href="#"
            onClick={(e) => {
              e.preventDefault();
              if (currentPage < totalPages) onPageChange(currentPage + 1);
            }}
            className={`inline-flex items-center px-[var(--size-space-300)] py-[var(--size-space-200)] rounded-[var(--size-radius-200)] ${
              currentPage === totalPages ? "opacity-50 pointer-events-none" : ""
            }`}
          >
            <span className="text-sm">Next</span>
            <ChevronRight className="h-4 w-4" />
          </PaginationNext>
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
};

export default PaginationComponent;
