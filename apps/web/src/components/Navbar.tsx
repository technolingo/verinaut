'use client';

import { useState } from 'react';

export const Navbar = () => {
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileOpen(!isMobileOpen);
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-md border-b border-gray-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <div className="flex-shrink-0">
            <a href="/" className="text-xl font-bold text-white hover:text-blue-400 transition-colors">
              Varinaut
            </a>
          </div>

          {/* Desktop Nav */}
          <div className="hidden sm:flex sm:items-center sm:ml-10 sm:space-x-4">
            <a href="/predict" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Predict
            </a>
            <a href="/dashboard" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Dashboard
            </a>
          </div>

          {/* Mobile menu button */}
          <div className="sm:hidden flex items-center">
            <button
              onClick={toggleMobileMenu}
              className="text-gray-300 hover:text-white p-1 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-label="Toggle menu"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isMobileOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileOpen && (
        <div className="sm:hidden bg-gray-900 border-t border-gray-800">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <a
              href="/predict"
              className="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
            >
              Predict
            </a>
            <a
              href="/dashboard"
              className="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium transition-colors"
            >
              Dashboard
            </a>
          </div>
        </div>
      )}
    </nav>
  );
};
