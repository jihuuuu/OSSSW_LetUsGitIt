import * as AccordionPrimitive from "@radix-ui/react-accordion";
import * as React from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

// 기본 Accordion 구성요소들
const Accordion = AccordionPrimitive.Root;
const AccordionItem = AccordionPrimitive.Item;

// ✅ AccordionTrigger
const AccordionTrigger = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger>
>(({ children, className, ...props }, ref) => (
  <AccordionPrimitive.Header>
    <AccordionPrimitive.Trigger
  ref={ref}
  className={cn(
    "flex w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-4 py-3 text-left text-lg font-medium shadow-sm hover:bg-gray-50 transition-all",
    className
  )}
  {...props}
>
  {children}
  <ChevronDown className="h-5 w-5 text-gray-500 transition-transform duration-200 group-data-[state=open]:rotate-180" />
</AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
));
AccordionTrigger.displayName = AccordionPrimitive.Trigger.displayName;

// ✅ AccordionContent
const AccordionContent = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content>
>(({ children, className, ...props }, ref) => (
  <AccordionPrimitive.Content
  ref={ref}
  className={cn(
    "overflow-hidden text-gray-700 px-4 pt-2 pb-4 border border-t-0 border-gray-300 bg-gray-50 rounded-b-lg transition-all data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down",
    className
  )}
  {...props}
>
  {children}
</AccordionPrimitive.Content>
));
AccordionContent.displayName = AccordionPrimitive.Content.displayName;

export {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
};
