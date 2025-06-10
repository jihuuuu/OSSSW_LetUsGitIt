import React from "react";
import { Link } from "react-router-dom";

export default function Logo() {
  return (
    <Link to="/" className="block w-fit">
      <div className="bg-blue-500 w-fit px-5 py-5 rounded">
      <div className="text-white font-bmjua text-5xl">
        <div className="flex items-center">
          <span>H</span>
          <span>🔥</span>
          <span>T</span>
        </div>
        <div>ISSUE</div>
      </div>
    </div>
    </Link>
  );
}
