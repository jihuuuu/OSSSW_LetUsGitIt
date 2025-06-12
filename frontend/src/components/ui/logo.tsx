import React from "react";
import { Link } from "react-router-dom";

export default function Logo() {
  return (
    <Link to="/" className="block w-fit">
      {/* 로고 영역 */}
    <div className="text-3xl font-semibold tracking-tight font-sans hover:opacity-90 transition">
      HOT<span className="text-orange-400">🔥</span>ISSUE
    </div>
    </Link>
  );
}
