// 📄 src/components/NoteEditSheet.tsx
import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";
import React from "react";

interface NoteEditSheetProps {
  open: boolean;
  note: Note | null;
  articles: Article[];
  onClose: () => void;
  onChange: (note: Note) => void;
  onSave: () => void;
}

export default function NoteEditSheet({
  open,
  note,
  articles,
  onClose,
  onChange,
  onSave,
}: NoteEditSheetProps) {
  if (!note) return null;

  return (
    <Sheet open={open}>
      <SheetContent>
        <SheetHeader className="mb-4">
          <SheetTitle>노트</SheetTitle>
        </SheetHeader>
        <div className="flex flex-col gap-4">
          <input
            type="text"
            className="border p-6 h-[40px] rounded w-full text-base"
            value={note.title || ""}
            onChange={(e) => onChange({ ...note, title: e.target.value })}
          />
          <textarea
            className="border p-4 rounded w-full h-[400px] resize-none text-base"
            value={note.text || ""}
            onChange={(e) => onChange({ ...note, text: e.target.value })}
          />

          <div className="mt-8">
            <h3 className="font-semibold mb-2">연관 기사</h3>
            <ul className="list-disc list-inside text-sm space-y-1">
              {articles.map((article) => (
                <li key={article.id}>
                  <a
                    href={article.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {article.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <SheetFooter className="mt-6 flex justify-between">
          <button
            onClick={onSave}
            className="text-sm bg-blue-400 hover:bg-blue-500 text-white font-semibold rounded-md"
          >
            SAVE
          </button>
          <button
            onClick={onClose}
            className="bg-blue-400 hover:bg-blue-500 text-white font-semibold rounded-md px-4 py-2 "
          >
            CLOSE
          </button>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}