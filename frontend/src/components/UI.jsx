import React from 'react';
import { cn } from '../utils/helpers';

export const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md',
  disabled = false,
  loading = false,
  className,
  ...props 
}) => {
  const baseStyles = 'font-medium rounded-lg transition-colors inline-flex items-center justify-center gap-2 whitespace-nowrap focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500';
  
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 disabled:bg-gray-400',
    secondary: 'bg-gray-200 dark:bg-dark-700 text-gray-900 dark:text-gray-50 hover:bg-gray-300 dark:hover:bg-dark-600',
    outline: 'border border-gray-300 dark:border-dark-600 text-gray-900 dark:text-gray-50 hover:bg-gray-50 dark:hover:bg-dark-800',
    ghost: 'text-gray-900 dark:text-gray-50 hover:bg-gray-100 dark:hover:bg-dark-700',
    danger: 'bg-red-600 text-white hover:bg-red-700 disabled:bg-gray-400',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      disabled={disabled || loading}
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
      {...props}
    >
      {loading && (
        <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
      )}
      {children}
    </button>
  );
};

export const Card = ({ children, className, ...props }) => {
  return (
    <div
      className={cn(
        'bg-white dark:bg-dark-800 rounded-lg border border-gray-200 dark:border-dark-700 shadow-sm p-6',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const Badge = ({ children, variant = 'primary', className }) => {
  const variants = {
    primary: 'bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200',
    success: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200',
    warning: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200',
    danger: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200',
    gray: 'bg-gray-100 dark:bg-dark-700 text-gray-800 dark:text-gray-200',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
};

export const Input = ({ label, error, className, ...props }) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-900 dark:text-gray-50 mb-1.5">
          {label}
        </label>
      )}
      <input
        className={cn(
          'w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg',
          'bg-white dark:bg-dark-800 text-gray-900 dark:text-gray-50',
          'placeholder-gray-500 dark:placeholder-gray-400',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          'disabled:bg-gray-100 dark:disabled:bg-dark-700 disabled:cursor-not-allowed',
          error && 'border-red-500 focus:ring-red-500',
          className
        )}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-600 dark:text-red-400 mt-1">{error}</p>
      )}
    </div>
  );
};

export const Textarea = ({ label, error, className, ...props }) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-900 dark:text-gray-50 mb-1.5">
          {label}
        </label>
      )}
      <textarea
        className={cn(
          'w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg',
          'bg-white dark:bg-dark-800 text-gray-900 dark:text-gray-50',
          'placeholder-gray-500 dark:placeholder-gray-400',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          'disabled:bg-gray-100 dark:disabled:bg-dark-700 disabled:cursor-not-allowed',
          'resize-none',
          error && 'border-red-500 focus:ring-red-500',
          className
        )}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-600 dark:text-red-400 mt-1">{error}</p>
      )}
    </div>
  );
};

export const Select = ({ label, error, options, className, ...props }) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-900 dark:text-gray-50 mb-1.5">
          {label}
        </label>
      )}
      <select
        className={cn(
          'w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg',
          'bg-white dark:bg-dark-800 text-gray-900 dark:text-gray-50',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          'disabled:bg-gray-100 dark:disabled:bg-dark-700 disabled:cursor-not-allowed',
          error && 'border-red-500 focus:ring-red-500',
          className
        )}
        {...props}
      >
        {options?.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="text-sm text-red-600 dark:text-red-400 mt-1">{error}</p>
      )}
    </div>
  );
};

export const Loading = ({ size = 'md', className }) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className={cn('flex items-center justify-center', className)}>
      <div className={cn(
        'border-2 border-gray-300 dark:border-dark-600',
        'border-t-primary-600 dark:border-t-primary-400',
        'rounded-full animate-spin',
        sizes[size]
      )} />
    </div>
  );
};

export const Modal = ({ open, onClose, title, children, actions, size = 'md' }) => {
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
  };

  if (!open) return null;

  return (
    <>
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />
      <div className="fixed inset-0 flex items-center justify-center z-50 p-4">
        <Card className={cn('w-full', sizes[size])}>
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50">
              {title}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              ✕
            </button>
          </div>
          <div className="mb-6">
            {children}
          </div>
          {actions && (
            <div className="flex gap-3 justify-end">
              {actions}
            </div>
          )}
        </Card>
      </div>
    </>
  );
};

export const Alert = ({ variant = 'info', title, message, onClose }) => {
  const variants = {
    info: 'bg-blue-50 dark:bg-blue-900 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200',
    success: 'bg-green-50 dark:bg-green-900 border-green-200 dark:border-green-800 text-green-800 dark:text-green-200',
    warning: 'bg-yellow-50 dark:bg-yellow-900 border-yellow-200 dark:border-yellow-800 text-yellow-800 dark:text-yellow-200',
    error: 'bg-red-50 dark:bg-red-900 border-red-200 dark:border-red-800 text-red-800 dark:text-red-200',
  };

  return (
    <div className={cn(
      'border rounded-lg p-4 flex items-start justify-between',
      variants[variant]
    )}>
      <div>
        {title && <p className="font-semibold">{title}</p>}
        {message && <p className="text-sm mt-1">{message}</p>}
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-current opacity-70 hover:opacity-100"
        >
          ✕
        </button>
      )}
    </div>
  );
};
