import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, BookOpen, Brain, Zap, Users, Trophy, Sparkles, ChevronDown } from 'lucide-react';
import { Button } from '../components/UI';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white dark:bg-dark-900">
      {/* Navbar */}
      <nav className="sticky top-0 bg-white dark:bg-dark-900 border-b border-gray-200 dark:border-dark-700 z-50">
        <div className="max-w-7xl mx-auto px-4 lg:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-2xl font-bold">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold">
              T
            </div>
            <span className="bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
              TwinLearnAI
            </span>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={() => navigate('/login')}>
              Sign In
            </Button>
            <Button variant="primary" onClick={() => navigate('/register')}>
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 lg:px-6 py-20 lg:py-32">
        <div className="text-center space-y-6">
          <div className="inline-block">
            <span className="px-4 py-2 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
              ✨ AI-Powered Learning Platform
            </span>
          </div>
          <h1 className="text-5xl lg:text-7xl font-bold text-gray-900 dark:text-gray-50 leading-tight">
            Your AI Twin<br />
            <span className="bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
              Professor
            </span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Upload your lecture materials and get instant AI-powered tutoring. Learn smarter, faster, and ace your exams with personalized teaching strategies.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate('/register')}
              className="gap-2"
            >
              Start Learning Free <ArrowRight size={20} />
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => navigate('/login')}
            >
              Sign In
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 lg:px-6 py-20 border-t border-gray-200 dark:border-dark-700">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-gray-50 mb-4">
            Features Built for Student Success
          </h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Everything you need to master your courses
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: BookOpen,
              title: 'Upload Lectures',
              description: 'Support for PDF, PPT, audio, video, and YouTube URLs',
            },
            {
              icon: Brain,
              title: 'AI Tutoring',
              description: 'Get instant answers with contextual explanations',
            },
            {
              icon: Sparkles,
              title: '9 Teaching Styles',
              description: 'From story-based to exam-oriented learning',
            },
            {
              icon: Zap,
              title: 'Smart Processing',
              description: 'Automatic transcription, extraction, and indexing',
            },
            {
              icon: Trophy,
              title: 'Track Progress',
              description: 'Visualize your mastery across all topics',
            },
            {
              icon: Users,
              title: 'Bookmarks',
              description: 'Save important explanations and questions',
            },
          ].map((feature, i) => (
            <div key={i} className="p-8 rounded-xl border border-gray-200 dark:border-dark-700 hover:shadow-lg transition-shadow">
              <feature.icon className="w-12 h-12 text-primary-600 mb-4" />
              <h3 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="max-w-7xl mx-auto px-4 lg:px-6 py-20 border-t border-gray-200 dark:border-dark-700">
        <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-gray-50 text-center mb-16">
          How It Works
        </h2>

        <div className="space-y-8">
          {[
            { step: 1, title: 'Upload', description: 'Upload your lecture materials in any format' },
            { step: 2, title: 'Process', description: 'AI automatically extracts and processes content' },
            { step: 3, title: 'Learn', description: 'Chat with your AI professor anytime, anywhere' },
            { step: 4, title: 'Master', description: 'Track progress and identify weak topics' },
          ].map((item, i) => (
            <div key={i} className="flex gap-6 items-start">
              <div className="w-12 h-12 rounded-full bg-primary-600 text-white flex items-center justify-center flex-shrink-0 font-bold text-lg">
                {item.step}
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {item.description}
                </p>
              </div>
              {i < 3 && (
                <ChevronDown className="text-gray-400 hidden md:block mt-2" size={24} />
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Teaching Strategies */}
      <section className="max-w-7xl mx-auto px-4 lg:px-6 py-20 border-t border-gray-200 dark:border-dark-700">
        <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-gray-50 text-center mb-16">
          9 Personalized Teaching Strategies
        </h2>

        <div className="grid md:grid-cols-3 gap-4">
          {['Story Based', 'Diagram Based', 'Step by Step', 'Code Based', 'Example Based', 'Exam Oriented', 'Interview Oriented', 'Simple', 'Detailed'].map((strategy, i) => (
            <div
              key={i}
              className="p-6 rounded-lg bg-gray-50 dark:bg-dark-800 border border-gray-200 dark:border-dark-700 text-center"
            >
              <p className="font-semibold text-gray-900 dark:text-gray-50">{strategy}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 lg:px-6 py-20 border-t border-gray-200 dark:border-dark-700">
        <div className="bg-gradient-to-r from-primary-600 to-primary-900 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">
            Ready to Transform Your Learning?
          </h2>
          <p className="text-lg opacity-90 max-w-2xl mx-auto mb-8">
            Join thousands of students using TwinLearnAI to excel in their courses
          </p>
          <Button
            variant="ghost"
            size="lg"
            onClick={() => navigate('/register')}
            className="text-white hover:bg-white hover:bg-opacity-10 border-white"
          >
            Get Started Free <ArrowRight size={20} />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-dark-700 py-12">
        <div className="max-w-7xl mx-auto px-4 lg:px-6 text-center text-gray-600 dark:text-gray-400">
          <p>&copy; 2024 TwinLearnAI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
