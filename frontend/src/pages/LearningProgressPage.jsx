import React, { useState, useEffect } from 'react';
import { DashboardLayout } from '../components/Layout';
import { lectureService } from '../services/lectureService';
import { mockLearningProgress } from '../data/mockData';
import { Card, Badge, Loading } from '../components/UI';
import { TrendingUp, Target, Flame } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

export default function LearningProgressPage() {
  const [loading, setLoading] = useState(false);

  const progressData = [
    { subject: 'DSA', progress: 48 },
    { subject: 'OOP', progress: 30 },
    { subject: 'DB', progress: 60 },
    { subject: 'OS', progress: 0 },
  ];

  const masteryData = [
    { name: 'Binary Search', value: 75 },
    { name: 'Recursion', value: 45 },
    { name: 'SQL Joins', value: 60 },
    { name: 'Java OOP', value: 30 },
    { name: 'DP', value: 25 },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            Learning Progress
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Track your progress across all subjects and topics
          </p>
        </div>

        {/* Overall Stats */}
        <div className="grid md:grid-cols-3 gap-4">
          <Card className="p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  Overall Progress
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-gray-50">
                  {mockLearningProgress.overallProgress}%
                </p>
              </div>
              <TrendingUp size={24} className="text-primary-600" />
            </div>
            <div className="mt-4 w-full bg-gray-200 dark:bg-dark-700 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full"
                style={{ width: `${mockLearningProgress.overallProgress}%` }}
              />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  Current Streak
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-gray-50">
                  {mockLearningProgress.learningStreak} days
                </p>
              </div>
              <Flame size={24} className="text-orange-600" />
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-4">
              Best: {mockLearningProgress.bestStreak} days
            </p>
          </Card>

          <Card className="p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  Topics Mastered
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-gray-50">
                  {mockLearningProgress.topicMastery.filter((t) => t.mastery >= 70).length}
                </p>
              </div>
              <Target size={24} className="text-green-600" />
            </div>
          </Card>
        </div>

        {/* Subject Progress Chart */}
        <Card>
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            Subject-wise Progress
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={progressData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="subject" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Bar dataKey="progress" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Topic Mastery Radar */}
          <Card>
            <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
              Topic Mastery
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={masteryData}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="name" stroke="#9ca3af" />
                <PolarRadiusAxis stroke="#9ca3af" />
                <Radar
                  name="Mastery %"
                  dataKey="value"
                  stroke="#0ea5e9"
                  fill="#0ea5e9"
                  fillOpacity={0.6}
                />
              </RadarChart>
            </ResponsiveContainer>
          </Card>

          {/* Strong vs Weak Topics */}
          <Card>
            <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
              Topic Breakdown
            </h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm font-semibold text-green-600 dark:text-green-400 mb-3">
                  Strong Topics
                </p>
                <div className="space-y-2">
                  {mockLearningProgress.topicMastery
                    .filter((t) => t.strong)
                    .map((topic) => (
                      <div
                        key={topic.topic}
                        className="flex items-center justify-between"
                      >
                        <span className="text-gray-700 dark:text-gray-300">
                          {topic.topic}
                        </span>
                        <Badge variant="success">{topic.mastery}%</Badge>
                      </div>
                    ))}
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200 dark:border-dark-700">
                <p className="text-sm font-semibold text-yellow-600 dark:text-yellow-400 mb-3">
                  Areas to Improve
                </p>
                <div className="space-y-2">
                  {mockLearningProgress.topicMastery
                    .filter((t) => !t.strong)
                    .map((topic) => (
                      <div
                        key={topic.topic}
                        className="flex items-center justify-between"
                      >
                        <span className="text-gray-700 dark:text-gray-300">
                          {topic.topic}
                        </span>
                        <Badge variant="warning">{topic.mastery}%</Badge>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
