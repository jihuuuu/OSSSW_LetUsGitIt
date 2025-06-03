import React from "react";
import { Link } from "react-router-dom";

export default function Logo() {
  return (
    <Link to="/" className="block w-fit">
      <img
        src="/logo.png"
        alt="Hot Issue Logo"
        className="w-[150px] h-auto select-none cursor-pointer"
      />
    </Link>
  );
}
