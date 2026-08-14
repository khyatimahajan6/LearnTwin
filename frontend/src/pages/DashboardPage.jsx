import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { lectureService } from '../services/lectureService';
import { DashboardLayout } from '../components/Layout';
import { Card, Badge, Loading, Button } from '../components/UI';
import { mockUserProfile, mockLearningProgress } from '../data/mockData';
import { BarChart3, Flame, BookOpen, MessageSquare, TrendingUp } from 'lucide-react';
import { formatDate } from '../utils/helpers';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const { user } = useAuth();
  const [lectures, setLectures] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const result = await lectureService.getLectures();
      if (result.success) {
        setLectures(result.data.slice(0, 4)); // Recent lectures
      }
      setLoading(false);
    };
    loadData();
  }, []);

  const stats = [
    {
      icon: BookOpen,
      label: 'Total Lectures',
      value: mockUserProfile.totalLectures,
      color: 'text-blue-600 dark:text-blue-400',
    },
    {
      icon: Tags,
      label: 'Topics Learned',
      value: mockUserProfile.topicsLearned,
      color: 'text-green-600 dark:text-green-400',
    },
    {
      icon: MessageSquare,
      label: 'Questions Asked',
      value: mockUserProfile.questionsAsked,
      color: 'text-purple-600 dark:text-purple-400',
    },
    {
      icon: Flame,
      label: 'Learning Streak',
      value: `${mockUserProfile.learningStreak} days`,
      color: 'text-orange-600 dark:text-orange-400',
    },
  ];

  const chartData = [
    { day: 'Mon', progress: 20 },
    { day: 'Tue', progress: 35 },
    { day: 'Wed', progress: 48 },
    { day: 'Thu', progress: 42 },
    { day: 'Fri', progress: 55 },
    { day: 'Sat', progress: 52 },
    { day: 'Sun', progress: 58 },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Welcome Section */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            Welcome back, {user?.name?.split(' ')[0]}! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Keep up your {mockUserProfile.learningStreak}-day streak and continue mastering new topics
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-4 gap-4">
          {stats.map((stat, i) => (
            <Card key={i} className="p-6">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    {stat.label}
                  </p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-gray-50">
                    {stat.value}
                  </p>
                </div>
                <stat.icon size={24} className={stat.color} />
              </div>
            </Card>
          ))}
        </div>

        {/* Progress Overview */}
        <Card>
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            This Week's Progress
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="day" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Line
                type="monotone"
                dataKey="progress"
                stroke="#0ea5e9"
                strokeWidth={2}
                dot={{ fill: '#0ea5e9', r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Continue Learning */}
          <Card className="lg:col-span-2">
            <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
              Continue Learning
            </h2>
            {loading ? (
              <div className="flex justify-center py-8">
                <Loading />
              </div>
            ) : (
              <div className="space-y-4">
                {lectures.map((lecture) => (
                  <div
                    key={lecture.id}
                    className="p-4 border border-gray-200 dark:border-dark-700 rounded-lg hover:bg-gray-50 dark:hover:bg-dark-700 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-gray-900 dark:text-gray-50">
                        {lecture.title}
                      </h3>
                      <Badge variant="primary">{lecture.difficulty}</Badge>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      {lecture.topic}
                    </p>
                    <div className="flex items-center gap-4">
                      <div className="flex-1 bg-gray-200 dark:bg-dark-600 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${lecture.progress}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {lecture.progress}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Quick Actions */}
          <Card>
            <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
              Quick Actions
            </h2>
            <div className="space-y-3">
              <Button variant="primary" className="w-full justify-center">
                + Upload Lecture
              </Button>
              <Button variant="secondary" className="w-full justify-center">
                Ask AI Professor
              </Button>
              <Button variant="secondary" className="w-full justify-center">
                View Topics
              </Button>
              <Button variant="secondary" className="w-full justify-center">
                Check Progress
              </Button>
            </div>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card>
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
            Recent Activity
          </h2>
          <div className="space-y-3">
            {[
              { action: 'Asked 3 questions on Binary Search', time: '2 hours ago' },
              { action: 'Completed SQL Joins lecture - 85% mastery', time: '5 hours ago' },
              { action: 'Started Dynamic Programming module', time: '1 day ago' },
              { action: 'Bookmarked 2 explanations', time: '2 days ago' },
            ].map((activity, i) => (
              <div
                key={i}
                className="flex items-start justify-between py-3 border-b border-gray-200 dark:border-dark-700 last:border-0"
              >
                <p className="text-gray-700 dark:text-gray-300">{activity.action}</p>
                <span className="text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap ml-2">
                  {activity.time}
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
}

import { Tags } from 'lucide-react';
