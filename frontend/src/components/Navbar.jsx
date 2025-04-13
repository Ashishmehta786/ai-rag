import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import Logo from "../assets/logo.png";
import { Menu, X } from "lucide-react";
import { ModeToggle } from "./Modetoggle";

function Navbar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="border-b border-gray-100 dark:border-gray-800 dark:border-gray-700 dark:text-white text-gray-800 bg-white top-0 sticky z-20  dark:bg-gray-900 dark:bg-opacity-[90%] backdrop-blur-md ">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 ">
          <div className="flex items-center">
            <span className="text-2xl font-bold  flex items-center dark:text-white">
              RAG
              <img
                className="h-8 w-8 inline dark:invert-0 invert"
                src={Logo}
                alt="Workflow"
              />
            </span>
          </div>
          <div className="flex sm:hidden">
            <button
              onClick={toggleMobileMenu}
              className="dark:text-gray-400 dark:hover:text-white hover:text-gray-800 text-gray-700 focus:outline-none"
            >
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
          <div className="hidden sm:flex sm:space-x-8 h-full">
            <a
              href="#features"
              className="border-transparent dark:text-gray-300 dark:hover:border-white dark:hover:text-white inline-flex items-center rounded px-1 pt-1 border-b-[3.9px] text-sm font-medium transition-all duration-300 text-gray-700 hover:border-gray-700 hover:text-gray-600"
            >
              Features
            </a>
            <a
              href="#how-it-works"
              className="border-transparent dark:text-gray-300 dark:hover:border-white dark:hover:text-white inline-flex items-center rounded px-1 pt-1 border-b-[3.9px] text-sm font-medium transition-all duration-300 text-gray-700 hover:border-gray-700 hover:text-gray-600"
            >
              How It Works
            </a>
            <a
              href="#about"
              className="border-transparent dark:text-gray-300 dark:hover:border-white dark:hover:text-white inline-flex items-center rounded px-1 pt-1 border-b-[3.9px] text-sm font-medium transition-all duration-300 text-gray-700 hover:border-gray-700 hover:text-gray-600"
            >
              About
            </a>
          </div>
          <div className="hidden sm:flex sm:items-center">
            <Link to="/Login">
              <Button
                variant=""
                className="mr-2 bg-slate-900 dark:hover:bg-neutral-600/10 text-gray-200 hover:text-white"
              >
                Sign In
              </Button>
            </Link>
            <Link to="/Signup">
              <Button>Get Started</Button>
            </Link>
            <div className="ml-4">
              <ModeToggle />
            </div>
          </div>
        </div>
        {isMobileMenuOpen && (
          <div className="sm:hidden mt-4 space-y-4 pb-4">
            <a
              href="#features"
              className="block dark:text-gray-300  dark:hover:text-white"
            >
              Features
            </a>
            <a
              href="#how-it-works"
              className="block dark:text-gray-300 dark:hover:text-white"
            >
              How It Works
            </a>
            <a
              href="#about"
              className="block dark:text-gray-300 dark:hover:text-white"
            >
              About
            </a>
            <div className="mt-4 space-y-2">
              <Button
                variant="outline"
                className="w-full bg-secondary dark:text-gray-200 dark:hover:text-white"
              >
                Sign In
              </Button>
              <Link to="/SignUp" className="w-full block">
                <Button className="w-full">Get Started</Button>
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
