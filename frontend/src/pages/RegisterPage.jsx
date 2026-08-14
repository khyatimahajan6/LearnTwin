import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authService } from '../services/authService';
import { Button, Input, Select, Alert } from '../components/UI';
import { validateEmail, validatePassword } from '../utils/helpers';

const universities = [
  { value: 'mit', label: 'MIT' },
  { value: 'stanford', label: 'Stanford' },
  { value: 'harvard', label: 'Harvard' },
  { value: 'berkeley', label: 'UC Berkeley' },
  { value: 'cmu', label: 'Carnegie Mellon' },
  { value: 'other', label: 'Other' },
];

export default function RegisterPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    university: '',
    course: '',
    semester: 'Fall 2024',
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
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    else if (!validateEmail(formData.email)) newErrors.email = 'Invalid email';
    if (!formData.password) newErrors.password = 'Password is required';
    else if (!validatePassword(formData.password))
      newErrors.password = 'Password must be at least 6 characters';
    if (!formData.confirmPassword) newErrors.confirmPassword = 'Please confirm password';
    else if (formData.password !== formData.confirmPassword)
      newErrors.confirmPassword = 'Passwords do not match';
    if (!formData.university) newErrors.university = 'University is required';
    if (!formData.course.trim()) newErrors.course = 'Course is required';
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
      const result = await authService.register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        university: formData.university,
        course: formData.course,
        semester: formData.semester,
      });

      if (result.success) {
        login(result.user);
        navigate('/dashboard');
      } else {
        setServerError(result.error || 'Registration failed');
      }
    } catch (err) {
      setServerError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center p-4 py-12">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <div className="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold text-xl mx-auto mb-4">
              T
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
              Create Account
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Start your AI-powered learning journey
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
              label="Full Name"
              placeholder="John Doe"
              value={formData.name}
              onChange={(e) => {
                setFormData({ ...formData, name: e.target.value });
                if (errors.name) setErrors({ ...errors, name: '' });
              }}
              error={errors.name}
            />

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

            <Input
              label="Confirm Password"
              type="password"
              placeholder="••••••••"
              value={formData.confirmPassword}
              onChange={(e) => {
                setFormData({ ...formData, confirmPassword: e.target.value });
                if (errors.confirmPassword) setErrors({ ...errors, confirmPassword: '' });
              }}
              error={errors.confirmPassword}
            />

            <Select
              label="University"
              options={universities}
              value={formData.university}
              onChange={(e) => {
                setFormData({ ...formData, university: e.target.value });
                if (errors.university) setErrors({ ...errors, university: '' });
              }}
              error={errors.university}
            />

            <Input
              label="Course"
              placeholder="e.g., Computer Science"
              value={formData.course}
              onChange={(e) => {
                setFormData({ ...formData, course: e.target.value });
                if (errors.course) setErrors({ ...errors, course: '' });
              }}
              error={errors.course}
            />

            <Select
              label="Semester"
              options={[
                { value: 'Fall 2024', label: 'Fall 2024' },
                { value: 'Spring 2025', label: 'Spring 2025' },
                { value: 'Summer 2025', label: 'Summer 2025' },
              ]}
              value={formData.semester}
              onChange={(e) =>
                setFormData({ ...formData, semester: e.target.value })
              }
            />

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full"
              loading={loading}
              disabled={loading}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Already have an account?{' '}
              <Link
                to="/login"
                className="font-medium text-primary-600 dark:text-primary-400 hover:underline"
              >
                Sign in here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
