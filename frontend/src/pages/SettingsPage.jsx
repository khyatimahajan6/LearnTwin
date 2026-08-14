import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { DashboardLayout } from '../components/Layout';
import { Card, Button, Input, Select, Alert } from '../components/UI';
import { Moon, Sun, LogOut, Mail, User, MapPin, BookOpen } from 'lucide-react';
import { teachingStrategies, mockUserProfile } from '../data/mockData';

export default function SettingsPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { darkMode, toggleDarkMode } = useTheme();
  const [profile, setProfile] = useState({
    name: user?.name || '',
    email: user?.email || '',
    university: user?.university || '',
    course: user?.course || '',
  });
  const [preferences, setPreferences] = useState({
    teachingStrategy: mockUserProfile.preferredTeachingStrategy,
    difficulty: mockUserProfile.preferredDifficulty,
    notifications: true,
    emailUpdates: true,
  });
  const [successMessage, setSuccessMessage] = useState('');
  const [changesSaved, setChangesSaved] = useState(false);

  const handleProfileUpdate = () => {
    setSuccessMessage('Profile updated successfully');
    setChangesSaved(true);
    setTimeout(() => setSuccessMessage(''), 3000);
  };

  const handleLogout = () => {
    logout();
    localStorage.removeItem('twinalai_auth');
    navigate('/login');
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 max-w-2xl">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            Settings
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your profile and preferences
          </p>
        </div>

        {successMessage && (
          <Alert
            variant="success"
            message={successMessage}
            onClose={() => setSuccessMessage('')}
          />
        )}

        {/* Profile Section */}
        <Card className="p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            Profile Information
          </h2>

          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
              {user?.name?.[0] || 'U'}
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-gray-50">
                {user?.name}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {user?.email}
              </p>
            </div>
            <Button variant="secondary" className="ml-auto">
              Change Avatar
            </Button>
          </div>

          <div className="space-y-4">
            <Input
              label="Full Name"
              value={profile.name}
              onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              icon={User}
            />

            <Input
              label="Email Address"
              type="email"
              value={profile.email}
              onChange={(e) => setProfile({ ...profile, email: e.target.value })}
              icon={Mail}
              disabled
            />

            <Input
              label="University"
              value={profile.university}
              onChange={(e) =>
                setProfile({ ...profile, university: e.target.value })
              }
              icon={MapPin}
            />

            <Input
              label="Course"
              value={profile.course}
              onChange={(e) => setProfile({ ...profile, course: e.target.value })}
              icon={BookOpen}
            />

            <Button
              variant="primary"
              className="w-full"
              onClick={handleProfileUpdate}
            >
              Save Changes
            </Button>
          </div>
        </Card>

        {/* Learning Preferences */}
        <Card className="p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            Learning Preferences
          </h2>

          <div className="space-y-4">
            <Select
              label="Preferred Teaching Strategy"
              options={teachingStrategies.map((s) => ({
                value: s.id,
                label: s.name,
              }))}
              value={preferences.teachingStrategy}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  teachingStrategy: e.target.value,
                })
              }
            />

            <Select
              label="Preferred Difficulty Level"
              options={[
                { value: 'Beginner', label: 'Beginner' },
                { value: 'Intermediate', label: 'Intermediate' },
                { value: 'Advanced', label: 'Advanced' },
              ]}
              value={preferences.difficulty}
              onChange={(e) =>
                setPreferences({ ...preferences, difficulty: e.target.value })
              }
            />

            <Button
              variant="primary"
              className="w-full"
              onClick={handleProfileUpdate}
            >
              Save Preferences
            </Button>
          </div>
        </Card>

        {/* Appearance */}
        <Card className="p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            Appearance
          </h2>

          <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-700 rounded-lg">
            <div className="flex items-center gap-3">
              {darkMode ? (
                <Moon size={24} className="text-gray-600 dark:text-gray-400" />
              ) : (
                <Sun size={24} className="text-gray-600 dark:text-gray-400" />
              )}
              <div>
                <p className="font-semibold text-gray-900 dark:text-gray-50">
                  Dark Mode
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {darkMode ? 'Enabled' : 'Disabled'}
                </p>
              </div>
            </div>
            <button
              onClick={toggleDarkMode}
              className={`relative w-12 h-6 rounded-full transition-colors ${
                darkMode
                  ? 'bg-primary-600'
                  : 'bg-gray-300 dark:bg-dark-600'
              }`}
            >
              <div
                className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform ${
                  darkMode ? 'translate-x-6' : ''
                }`}
              />
            </button>
          </div>
        </Card>

        {/* Notifications */}
        <Card className="p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            Notifications
          </h2>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-700 rounded-lg">
              <div>
                <p className="font-semibold text-gray-900 dark:text-gray-50">
                  In-app Notifications
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Get notified about new questions, progress updates
                </p>
              </div>
              <button
                onClick={() =>
                  setPreferences({
                    ...preferences,
                    notifications: !preferences.notifications,
                  })
                }
                className={`relative w-12 h-6 rounded-full transition-colors ${
                  preferences.notifications
                    ? 'bg-primary-600'
                    : 'bg-gray-300 dark:bg-dark-600'
                }`}
              >
                <div
                  className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform ${
                    preferences.notifications ? 'translate-x-6' : ''
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-700 rounded-lg">
              <div>
                <p className="font-semibold text-gray-900 dark:text-gray-50">
                  Email Updates
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Weekly learning summary and tips
                </p>
              </div>
              <button
                onClick={() =>
                  setPreferences({
                    ...preferences,
                    emailUpdates: !preferences.emailUpdates,
                  })
                }
                className={`relative w-12 h-6 rounded-full transition-colors ${
                  preferences.emailUpdates
                    ? 'bg-primary-600'
                    : 'bg-gray-300 dark:bg-dark-600'
                }`}
              >
                <div
                  className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform ${
                    preferences.emailUpdates ? 'translate-x-6' : ''
                  }`}
                />
              </button>
            </div>
          </div>
        </Card>

        {/* Danger Zone */}
        <Card className="p-6 border-red-200 dark:border-red-900">
          <h2 className="text-xl font-bold text-red-600 dark:text-red-400 mb-6">
            Danger Zone
          </h2>

          <div className="space-y-3">
            <Button
              variant="danger"
              className="w-full justify-center"
              onClick={handleLogout}
            >
              <LogOut size={18} />
              Logout
            </Button>
            <Button variant="danger" className="w-full justify-center opacity-50 cursor-not-allowed" disabled>
              Delete Account
            </Button>
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
}
