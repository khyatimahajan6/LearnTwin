import React, { useState, useEffect } from 'react';
import { DashboardLayout } from '../components/Layout';
import { lectureService } from '../services/lectureService';
import { Card, Badge, Button, Input, Select, Loading, Modal, Alert } from '../components/UI';
import { Trash2, Play, MessageSquare, Search, Filter, MoreVertical } from 'lucide-react';
import { formatDate, getDifficultyColor } from '../utils/helpers';

export default function MyLecturesPage() {
  const [lectures, setLectures] = useState([]);
  const [filteredLectures, setFilteredLectures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [deleteModal, setDeleteModal] = useState({ open: false, lectureId: null });
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    loadLectures();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [lectures, searchQuery, filterDifficulty, filterStatus]);

  const loadLectures = async () => {
    setLoading(true);
    const result = await lectureService.getLectures();
    if (result.success) {
      setLectures(result.data);
    }
    setLoading(false);
  };

  const applyFilters = () => {
    let filtered = [...lectures];

    if (searchQuery) {
      filtered = filtered.filter(
        (l) =>
          l.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          l.topic.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (filterDifficulty) {
      filtered = filtered.filter((l) => l.difficulty === filterDifficulty);
    }

    if (filterStatus) {
      filtered = filtered.filter((l) => l.status === filterStatus);
    }

    setFilteredLectures(filtered);
  };

  const handleDelete = async () => {
    setDeleteLoading(true);
    const result = await lectureService.deleteLecture(deleteModal.lectureId);
    setDeleteLoading(false);

    if (result.success) {
      setLectures(lectures.filter((l) => l.id !== deleteModal.lectureId));
      setSuccessMessage('Lecture deleted successfully');
      setDeleteModal({ open: false, lectureId: null });
      setTimeout(() => setSuccessMessage(''), 3000);
    }
  };

  const getStatusBadgeVariant = (status) => {
    switch (status) {
      case 'Completed':
        return 'success';
      case 'In Progress':
        return 'warning';
      default:
        return 'gray';
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            My Lectures
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage and learn from your uploaded lecture materials
          </p>
        </div>

        {successMessage && (
          <Alert
            variant="success"
            message={successMessage}
            onClose={() => setSuccessMessage('')}
          />
        )}

        {/* Search and Filters */}
        <Card className="p-4">
          <div className="grid md:grid-cols-4 gap-4">
            <Input
              placeholder="Search lectures..."
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
            <Select
              options={[
                { value: '', label: 'All Status' },
                { value: 'Not Started', label: 'Not Started' },
                { value: 'In Progress', label: 'In Progress' },
                { value: 'Completed', label: 'Completed' },
              ]}
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            />
            <Button variant="secondary" className="w-full justify-center">
              <Filter size={18} />
              More Filters
            </Button>
          </div>
        </Card>

        {/* Lectures List */}
        {loading ? (
          <div className="flex justify-center py-12">
            <Loading size="lg" />
          </div>
        ) : filteredLectures.length === 0 ? (
          <Card className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              No lectures found. Try adjusting your filters or upload a new lecture.
            </p>
            <Button variant="primary">Upload Your First Lecture</Button>
          </Card>
        ) : (
          <div className="grid gap-4">
            {filteredLectures.map((lecture) => (
              <Card key={lecture.id} className="p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-50">
                        {lecture.title}
                      </h3>
                      <Badge variant={getStatusBadgeVariant(lecture.status)}>
                        {lecture.status}
                      </Badge>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4 text-sm">
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Subject</p>
                        <p className="font-medium text-gray-900 dark:text-gray-50">
                          {lecture.subject}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Topic</p>
                        <p className="font-medium text-gray-900 dark:text-gray-50">
                          {lecture.topic}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Difficulty</p>
                        <p className="font-medium text-gray-900 dark:text-gray-50">
                          {lecture.difficulty}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Duration</p>
                        <p className="font-medium text-gray-900 dark:text-gray-50">
                          {lecture.duration}
                        </p>
                      </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="mb-4">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          Progress
                        </span>
                        <span className="text-sm font-semibold text-gray-900 dark:text-gray-50">
                          {lecture.progress}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-dark-700 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${lecture.progress}%` }}
                        />
                      </div>
                    </div>

                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Uploaded {formatDate(lecture.uploadedAt)}
                      {lecture.lastAccessed && (
                        <> • Last accessed {formatDate(lecture.lastAccessed)}</>
                      )}
                    </p>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm" title="Continue Learning">
                      <Play size={18} />
                    </Button>
                    <Button variant="ghost" size="sm" title="Ask AI">
                      <MessageSquare size={18} />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() =>
                        setDeleteModal({ open: true, lectureId: lecture.id })
                      }
                      title="Delete"
                      className="text-red-600 hover:bg-red-50 dark:hover:bg-red-900"
                    >
                      <Trash2 size={18} />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Delete Modal */}
      <Modal
        open={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, lectureId: null })}
        title="Delete Lecture"
        actions={[
          <Button
            key="cancel"
            variant="secondary"
            onClick={() => setDeleteModal({ open: false, lectureId: null })}
          >
            Cancel
          </Button>,
          <Button
            key="delete"
            variant="danger"
            loading={deleteLoading}
            onClick={handleDelete}
          >
            Delete
          </Button>,
        ]}
      >
        <p>
          Are you sure you want to delete this lecture? This action cannot be undone.
        </p>
      </Modal>
    </DashboardLayout>
  );
}
