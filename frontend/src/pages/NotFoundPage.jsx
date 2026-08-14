import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/UI';
import { ArrowRight, Home } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-dark-900 flex items-center justify-center p-4">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-primary-600 mb-4">404</h1>
          <h2 className="text-4xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            Page Not Found
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-md mx-auto">
            Sorry, we couldn't find the page you're looking for. It might have been
            moved or deleted.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/">
            <Button variant="primary" size="lg" className="gap-2">
              <Home size={20} />
              Go Home
            </Button>
          </Link>
          <Link to="/dashboard">
            <Button variant="secondary" size="lg" className="gap-2">
              Dashboard
              <ArrowRight size={20} />
            </Button>
          </Link>
        </div>

        <div className="mt-16 text-gray-600 dark:text-gray-400">
          <p className="mb-4">Other helpful links:</p>
          <div className="flex flex-wrap gap-3 justify-center">
            {[
              { label: 'My Lectures', href: '/lectures' },
              { label: 'Upload', href: '/upload' },
              { label: 'AI Professor', href: '/ai-professor' },
              { label: 'Progress', href: '/progress' },
            ].map((link) => (
              <Link
                key={link.href}
                to={link.href}
                className="text-primary-600 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
