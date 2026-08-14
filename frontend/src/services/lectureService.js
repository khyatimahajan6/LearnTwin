import { mockLectures, mockTopics } from '../data/mockData';

// Mock lecture service
export const lectureService = {
  getLectures: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ success: true, data: mockLectures });
      }, 500);
    });
  },

  getLectureById: async (id) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const lecture = mockLectures.find(l => l.id === id);
        if (lecture) {
          resolve({ success: true, data: lecture });
        } else {
          resolve({ success: false, error: 'Lecture not found' });
        }
      }, 300);
    });
  },

  getTopics: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ success: true, data: mockTopics });
      }, 500);
    });
  },

  getTopicById: async (id) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const topic = mockTopics.find(t => t.id === id);
        if (topic) {
          resolve({ success: true, data: topic });
        } else {
          resolve({ success: false, error: 'Topic not found' });
        }
      }, 300);
    });
  },

  deleteLecture: async (id) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        // In real app, delete from backend
        const index = mockLectures.findIndex(l => l.id === id);
        if (index > -1) {
          mockLectures.splice(index, 1);
          resolve({ success: true, message: 'Lecture deleted' });
        } else {
          resolve({ success: false, error: 'Lecture not found' });
        }
      }, 800);
    });
  },

  updateProgress: async (lectureId, progress) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const lecture = mockLectures.find(l => l.id === lectureId);
        if (lecture) {
          lecture.progress = Math.min(100, progress);
          resolve({ success: true, data: lecture });
        } else {
          resolve({ success: false, error: 'Lecture not found' });
        }
      }, 500);
    });
  },

  searchLectures: async (query) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const results = mockLectures.filter(l =>
          l.title.toLowerCase().includes(query.toLowerCase()) ||
          l.subject.toLowerCase().includes(query.toLowerCase()) ||
          l.topic.toLowerCase().includes(query.toLowerCase())
        );
        resolve({ success: true, data: results });
      }, 400);
    });
  },

  filterLectures: async (filters) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        let results = [...mockLectures];
        
        if (filters.difficulty) {
          results = results.filter(l => l.difficulty === filters.difficulty);
        }
        if (filters.status) {
          results = results.filter(l => l.status === filters.status);
        }
        if (filters.subject) {
          results = results.filter(l => l.subject === filters.subject);
        }
        
        resolve({ success: true, data: results });
      }, 400);
    });
  },
};
