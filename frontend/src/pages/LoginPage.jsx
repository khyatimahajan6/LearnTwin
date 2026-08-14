import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authService } from '../services/authService';
import { Button, Input, Alert, Loading } from '../components/UI';
import { validateEmail, validatePassword } from '../utils/helpers';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false,
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [serverError, setServerError] = useState('');

  useEffect(() => {
    if (localStorage.getItem('twinalai_auth')) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const validate = () => {
    const newErrors = {};
    if (!formData.email) newErrors.email = 'Email is required';
    else if (!validateEmail(formData.email)) newErrors.email = 'Invalid email format';
    if (!formData.password) newErrors.password = 'Password is required';
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setServerError('');

    try {
      const result = await authService.login(
        formData.email,
        formData.password,
        formData.rememberMe
      );

      if (result.success) {
        login(result.user);
        navigate('/dashboard');
      } else {
        setServerError(result.error || 'Login failed. Please try again.');
      }
    } catch (err) {
      setServerError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <div className="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold text-xl mx-auto mb-4">
              T
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
              Welcome Back
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Sign in to continue your learning journey
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {serverError && (
              <Alert
                variant="error"
                message={serverError}
                onClose={() => setServerError('')}
              />
            )}

            <Input
              label="Email Address"
              type="email"
              placeholder="you@university.edu"
              value={formData.email}
              onChange={(e) => {
                setFormData({ ...formData, email: e.target.value });
                if (errors.email) setErrors({ ...errors, email: '' });
              }}
              error={errors.email}
            />

            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => {
                setFormData({ ...formData, password: e.target.value });
                if (errors.password) setErrors({ ...errors, password: '' });
              }}
              error={errors.password}
            />

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="rememberMe"
                checked={formData.rememberMe}
                onChange={(e) =>
                  setFormData({ ...formData, rememberMe: e.target.checked })
                }
                className="w-4 h-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
              />
              <label htmlFor="rememberMe" className="text-sm text-gray-700 dark:text-gray-300">
                Remember me
              </label>
            </div>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full"
              loading={loading}
              disabled={loading}
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </Button>
          </form>

          <div className="mt-6 space-y-3">
            <Link
              to="/forgot-password"
              className="block text-center text-primary-600 dark:text-primary-400 hover:underline text-sm font-medium"
            >
              Forgot password?
            </Link>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300 dark:border-dark-600" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white dark:bg-dark-800 text-gray-600 dark:text-gray-400">
                  Or
                </span>
              </div>
            </div>

            <p className="text-center text-gray-600 dark:text-gray-400 text-sm">
              Don't have an account?{' '}
              <Link
                to="/register"
                className="font-medium text-primary-600 dark:text-primary-400 hover:underline"
              >
                Sign up here
              </Link>
            </p>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200 dark:border-dark-700 text-center text-xs text-gray-600 dark:text-gray-400">
            <p>Demo credentials:</p>
            <p>Email: test@university.edu</p>
            <p>Password: password123</p>
          </div>
        </div>
      </div>
    </div>
  );
}
