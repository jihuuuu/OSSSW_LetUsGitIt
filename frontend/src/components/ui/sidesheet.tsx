import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { X } from "lucide-react";
import React from "react";

export default function SideSheet() {
  const isOpen = true;

  return (
    <Sheet open={isOpen}>
      <SheetContent
        className="flex flex-col w-[400px] max-w-[400px] p-0 border-l"
        showCloseButton={false}
      >
        <SheetHeader className="flex items-start pl-6 pr-3 pt-3 pb-4 border-none">
          <div className="flex items-start justify-between w-full">
            <SheetTitle className="flex-1 mt-3 text-lg font-semibold text-[#49454f] tracking-wide leading-snug">
              Title
            </SheetTitle>

            <Button
              variant="ghost"
              size="icon"
              className="w-12 h-12 rounded-full"
            >
              <X className="w-6 h-6" />
            </Button>
          </div>
        </SheetHeader>

        {/* 본문 컨텐츠 자리 */}
        <div className="flex-1 w-full" />

        <div className="w-full">
          <Separator className="w-full" />

          <SheetFooter className="flex justify-start gap-2 p-6 pt-4">
            <Button className="h-10 px-6 py-2.5 bg-[#77aafb] text-white rounded-full text-sm font-medium">
              Save
            </Button>

            <Button
              variant="outline"
              className="h-10 px-6 py-2.5 border-[#79747e] text-[#77aafb] rounded-full text-sm font-medium"
            >
              Cancel
            </Button>
          </SheetFooter>
        </div>
      </SheetContent>
    </Sheet>
  );
}
