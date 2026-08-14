import React, { useState, useEffect } from 'react';
import { DashboardLayout } from '../components/Layout';
import { bookmarkService } from '../services/bookmarkService';
import { Card, Badge, Button, Loading, Alert } from '../components/UI';
import { Trash2, FileText, MessageSquare, BookMarked, Search } from 'lucide-react';
import { formatDateTime } from '../utils/helpers';

export default function BookmarksPage() {
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    setLoading(true);
    const result = await bookmarkService.getBookmarks();
    if (result.success) {
      setBookmarks(result.data);
    }
    setLoading(false);
  };

  const handleDeleteBookmark = async (bookmarkId) => {
    const result = await bookmarkService.removeBookmark(bookmarkId);
    if (result.success) {
      setBookmarks(bookmarks.filter((b) => b.id !== bookmarkId));
      setSuccessMessage('Bookmark removed');
      setTimeout(() => setSuccessMessage(''), 3000);
    }
  };

  const getBookmarkIcon = (type) => {
    switch (type) {
      case 'explanation':
        return <FileText size={18} className="text-blue-600 dark:text-blue-400" />;
      case 'question':
        return <MessageSquare size={18} className="text-purple-600 dark:text-purple-400" />;
      case 'section':
        return <BookMarked size={18} className="text-green-600 dark:text-green-400" />;
      default:
        return <BookMarked size={18} className="text-gray-600 dark:text-gray-400" />;
    }
  };

  const getBookmarkTypeLabel = (type) => {
    switch (type) {
      case 'explanation':
        return 'Explanation';
      case 'question':
        return 'Question';
      case 'section':
        return 'Section';
      default:
        return type;
    }
  };

  const groupedBookmarks = bookmarks.reduce((acc, bookmark) => {
    if (!acc[bookmark.type]) {
      acc[bookmark.type] = [];
    }
    acc[bookmark.type].push(bookmark);
    return acc;
  }, {});

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            Bookmarks
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Save and organize important explanations and questions
          </p>
        </div>

        {successMessage && (
          <Alert
            variant="success"
            message={successMessage}
            onClose={() => setSuccessMessage('')}
          />
        )}

        {loading ? (
          <div className="flex justify-center py-12">
            <Loading size="lg" />
          </div>
        ) : bookmarks.length === 0 ? (
          <Card className="text-center py-12">
            <BookMarked size={48} className="text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              No bookmarks yet. Start bookmarking important content!
            </p>
            <Button variant="primary">Upload a Lecture</Button>
          </Card>
        ) : (
          <div className="space-y-6">
            {Object.entries(groupedBookmarks).map(([type, typeBookmarks]) => (
              <div key={type}>
                <div className="flex items-center gap-2 mb-4">
                  {getBookmarkIcon(type)}
                  <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50">
                    {getBookmarkTypeLabel(type)}
                    <span className="text-sm text-gray-600 dark:text-gray-400 ml-2">
                      ({typeBookmarks.length})
                    </span>
                  </h2>
                </div>

                <div className="grid gap-4">
                  {typeBookmarks.map((bookmark) => (
                    <Card
                      key={bookmark.id}
                      className="p-6 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            {getBookmarkIcon(bookmark.type)}
                            <h3 className="font-semibold text-gray-900 dark:text-gray-50">
                              {bookmark.type === 'explanation'
                                ? 'Saved Explanation'
                                : bookmark.type === 'question'
                                  ? 'Saved Question'
                                  : 'Saved Section'}
                            </h3>
                          </div>
                          <p className="text-gray-700 dark:text-gray-300 mb-3 line-clamp-3">
                            {bookmark.content}
                          </p>
                          <p className="text-xs text-gray-600 dark:text-gray-400">
                            Saved{' '}
                            {new Date(bookmark.createdAt).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                            })}
                          </p>
                        </div>

                        <div className="flex gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            title="Delete"
                            onClick={() =>
                              handleDeleteBookmark(bookmark.id)
                            }
                            className="text-red-600 hover:bg-red-50 dark:hover:bg-red-900"
                          >
                            <Trash2 size={18} />
                          </Button>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
