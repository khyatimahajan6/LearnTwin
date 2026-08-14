import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  Menu, X, Home, BookOpen, Upload, MessageSquare, BarChart3,
  Tags, Bookmark, Settings, LogOut, Search, Bell, Moon, Sun,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { cn } from '../utils/helpers';

const SidebarLink = ({ to, icon: Icon, label, active, onClick }) => {
  return (
    <Link
      to={to}
      onClick={onClick}
      className={cn(
        'flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
        active
          ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700'
      )}
    >
      <Icon size={20} />
      <span>{label}</span>
    </Link>
  );
};

export const Sidebar = ({ open, onClose }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    { to: '/dashboard', icon: Home, label: 'Dashboard' },
    { to: '/lectures', icon: BookOpen, label: 'My Lectures' },
    { to: '/upload', icon: Upload, label: 'Upload Lecture' },
    { to: '/ai-professor', icon: MessageSquare, label: 'AI Professor' },
    { to: '/progress', icon: BarChart3, label: 'Learning Progress' },
    { to: '/topics', icon: Tags, label: 'Topics' },
    { to: '/bookmarks', icon: Bookmark, label: 'Bookmarks' },
    { to: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <>
      {open && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
          onClick={onClose}
        />
      )}
      <div
        className={cn(
          'fixed left-0 top-0 h-screen w-64 bg-white dark:bg-dark-900 border-r border-gray-200 dark:border-dark-700 z-40 transform transition-transform duration-300 overflow-y-auto',
          'lg:relative lg:translate-x-0',
          open ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="p-6 border-b border-gray-200 dark:border-dark-700">
          <Link to="/dashboard" className="flex items-center gap-2 text-2xl font-bold">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold">
              T
            </div>
            <span className="bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
              TwinLearnAI
            </span>
          </Link>
        </div>

        <nav className="p-4 space-y-2">
          {menuItems.map(item => (
            <SidebarLink
              key={item.to}
              to={item.to}
              icon={item.icon}
              label={item.label}
              active={location.pathname === item.to}
              onClick={onClose}
            />
          ))}
        </nav>
      </div>
    </>
  );
};

export const Topbar = ({ onSidebarOpen }) => {
  const { user, logout } = useAuth();
  const { darkMode, toggleDarkMode } = useTheme();
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);

  const handleLogout = () => {
    logout();
    localStorage.removeItem('twinalai_auth');
    navigate('/login');
  };

  return (
    <header className="sticky top-0 bg-white dark:bg-dark-900 border-b border-gray-200 dark:border-dark-700 z-20">
      <div className="flex items-center justify-between h-16 px-4 lg:px-6">
        <button
          onClick={onSidebarOpen}
          className="lg:hidden p-2 hover:bg-gray-100 dark:hover:bg-dark-800 rounded-lg"
        >
          <Menu size={24} />
        </button>

        <div className="flex-1 hidden md:flex items-center gap-4 max-w-md mx-4">
          <Search size={20} className="text-gray-400" />
          <input
            type="text"
            placeholder="Search lectures..."
            className="w-full bg-transparent text-sm focus:outline-none placeholder-gray-400"
          />
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={toggleDarkMode}
            className="p-2 hover:bg-gray-100 dark:hover:bg-dark-800 rounded-lg transition-colors"
          >
            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>

          <button className="relative p-2 hover:bg-gray-100 dark:hover:bg-dark-800 rounded-lg transition-colors">
            <Bell size={20} />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-600 rounded-full" />
          </button>

          <div className="relative">
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              className="flex items-center gap-2 p-2 hover:bg-gray-100 dark:hover:bg-dark-800 rounded-lg transition-colors"
            >
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                {user?.name?.[0] || 'U'}
              </div>
            </button>

            {showDropdown && (
              <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-dark-800 border border-gray-200 dark:border-dark-700 rounded-lg shadow-lg overflow-hidden">
                <div className="p-4 border-b border-gray-200 dark:border-dark-700">
                  <p className="font-semibold text-gray-900 dark:text-gray-50">
                    {user?.name || 'User'}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {user?.email}
                  </p>
                </div>
                <nav className="p-2">
                  <Link
                    to="/settings"
                    className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700 rounded transition-colors"
                  >
                    Settings
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-dark-700 rounded transition-colors flex items-center gap-2"
                  >
                    <LogOut size={18} />
                    Logout
                  </button>
                </nav>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export const DashboardLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-dark-900">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Topbar onSidebarOpen={() => setSidebarOpen(true)} />
        <main className="flex-1 overflow-auto">
          <div className="max-w-7xl mx-auto p-4 lg:p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
