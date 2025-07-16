// components/Navbar.js
"use client";

export default function Navbar() {
  return (
    <header className="bg-[#f4c29b] shadow-md">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <h1 className="text-2xl md:text-3xl font-extrabold text-[#006f6a]">
          PolicyPulse
        </h1>
        <nav className="hidden md:flex gap-6 text-[#006f6a] font-medium">
          <a href="#" className="hover:text-[#004c47] transition">Home</a>
          <a href="#" className="hover:text-[#004c47] transition">About</a>
          <a href="#" className="hover:text-[#004c47] transition">Contact</a>
        </nav>
      </div>
    </header>
  );
}
