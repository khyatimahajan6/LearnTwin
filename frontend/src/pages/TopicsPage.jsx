import React, { useState, useEffect } from 'react';
import { DashboardLayout } from '../components/Layout';
import { lectureService } from '../services/lectureService';
import { Card, Badge, Button, Input, Loading, Select } from '../components/UI';
import { Search, Filter, TrendingUp } from 'lucide-react';

export default function TopicsPage() {
  const [topics, setTopics] = useState([]);
  const [filteredTopics, setFilteredTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState('');

  useEffect(() => {
    loadTopics();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [topics, searchQuery, filterDifficulty]);

  const loadTopics = async () => {
    setLoading(true);
    const result = await lectureService.getTopics();
    if (result.success) {
      setTopics(result.data);
    }
    setLoading(false);
  };

  const applyFilters = () => {
    let filtered = [...topics];

    if (searchQuery) {
      filtered = filtered.filter((t) =>
        t.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (filterDifficulty) {
      filtered = filtered.filter((t) => t.difficulty === filterDifficulty);
    }

    setFilteredTopics(filtered);
  };

  const getMasteryColor = (mastery) => {
    if (mastery === 0) return 'from-gray-400 to-gray-500';
    if (mastery < 40) return 'from-red-400 to-red-500';
    if (mastery < 70) return 'from-yellow-400 to-yellow-500';
    return 'from-green-400 to-green-500';
  };

  const getMasteryText = (mastery) => {
    if (mastery === 0) return 'Not Started';
    if (mastery < 40) return 'Needs Work';
    if (mastery < 70) return 'Good Progress';
    return 'Mastered';
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            Topics
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            View and track your mastery across all learning topics
          </p>
        </div>

        {/* Search and Filter */}
        <Card className="p-4">
          <div className="grid md:grid-cols-3 gap-4">
            <Input
              placeholder="Search topics..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              icon={Search}
            />
            <Select
              options={[
                { value: '', label: 'All Difficulties' },
                { value: 'Beginner', label: 'Beginner' },
                { value: 'Intermediate', label: 'Intermediate' },
                { value: 'Advanced', label: 'Advanced' },
              ]}
              value={filterDifficulty}
              onChange={(e) => setFilterDifficulty(e.target.value)}
            />
            <Button variant="secondary" className="w-full justify-center">
              <Filter size={18} />
              More Filters
            </Button>
          </div>
        </Card>

        {/* Topics Grid */}
        {loading ? (
          <div className="flex justify-center py-12">
            <Loading size="lg" />
          </div>
        ) : filteredTopics.length === 0 ? (
          <Card className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">
              No topics found. Upload a lecture to start learning!
            </p>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredTopics.map((topic) => (
              <Card key={topic.id} className="p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-gray-50">
                    {topic.name}
                  </h3>
                  <Badge variant="primary">{topic.difficulty}</Badge>
                </div>

                {/* Mastery Circle */}
                <div className="flex items-center justify-center mb-6">
                  <div className="relative w-32 h-32">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        fill="none"
                        stroke="#e5e7eb"
                        strokeWidth="8"
                      />
                      <circle
                        cx="64"
                        cy="64"
                        r="56"
                        fill="none"
                        stroke={`url(#gradient-${topic.id})`}
                        strokeWidth="8"
                        strokeDasharray={`${topic.mastery * 3.52} 352`}
                        strokeLinecap="round"
                      />
                      <defs>
                        <linearGradient
                          id={`gradient-${topic.id}`}
                          x1="0%"
                          y1="0%"
                          x2="100%"
                          y2="100%"
                        >
                          <stop offset="0%" stopColor="#60a5fa" />
                          <stop offset="100%" stopColor="#0ea5e9" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center">
                        <p className="text-3xl font-bold text-gray-900 dark:text-gray-50">
                          {topic.mastery}%
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400">
                          Mastery
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-3 mb-4">
                  <div className="text-center">
                    <Badge
                      variant={
                        topic.mastery >= 70
                          ? 'success'
                          : topic.mastery >= 40
                            ? 'warning'
                            : 'danger'
                      }
                    >
                      {getMasteryText(topic.mastery)}
                    </Badge>
                  </div>

                  <div className="text-sm text-gray-600 dark:text-gray-400 text-center">
                    <p>
                      <strong>{topic.questions}</strong> questions asked
                    </p>
                  </div>
                </div>

                <Button variant="outline" className="w-full justify-center">
                  <TrendingUp size={18} />
                  Continue Learning
                </Button>
              </Card>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
