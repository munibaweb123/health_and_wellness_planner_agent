"use client";

import Link from "next/link";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Menu } from "lucide-react";

export default function Navbar() {
  return (
    <header className="w-full flex items-center justify-between px-4 py-3 border-b shadow-sm bg-white">
      <h1 className="text-lg font-bold">🏥 Health Planner</h1>

      {/* Desktop Navbar */}
      <nav className="hidden md:flex gap-6 text-sm font-medium">
        <Link href="/" className="hover:text-blue-600">Home</Link>
        <Link href="/track" className="hover:text-blue-600">Track Progress</Link>
        <Link href="/progress" className="hover:text-blue-600">View Logs</Link>
        <Link href="/report" className="hover:text-blue-600">Download Report</Link>
      </nav>

      {/* Mobile Menu Button */}
      <div className="md:hidden">
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="icon">
              <Menu className="w-5 h-5" />
            </Button>
          </SheetTrigger>

          <SheetContent side="right" className="w-64">
            <nav className="flex flex-col gap-4 mt-8">
              <Link href="/" className="text-lg font-medium hover:underline">Home</Link>
              <Link href="/track" className="text-lg font-medium hover:underline">Track Progress</Link>
              <Link href="/progress" className="text-lg font-medium hover:underline">View Logs</Link>
              <Link href="/report" className="text-lg font-medium hover:underline">Download Report</Link>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
