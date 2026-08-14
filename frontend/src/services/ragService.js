import { mockAIResponses } from '../data/mockData';

// Mock RAG + AI service
export const ragService = {
  askQuestion: async (lectureId, question, strategy = 'step') => {
    return new Promise((resolve) => {
      setTimeout(() => {
        // Mock response based on strategy
        const baseResponse = mockAIResponses[strategy] || mockAIResponses.step;
        
        const response = {
          id: `response-${Date.now()}`,
          lectureId,
          question,
          answer: baseResponse,
          strategy,
          sources: [
            { title: 'Lecture Notes', page: 5, relevance: 0.95 },
            { title: 'Reference Material', page: 12, relevance: 0.87 },
          ],
          confidence: 0.92,
          timestamp: new Date().toISOString(),
          helpful: null,
        };

        resolve({ success: true, data: response });
      }, 2000); // Simulate AI thinking time
    });
  },

  followUpQuestion: async (conversationId, question, strategy) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const baseResponse = mockAIResponses[strategy] || mockAIResponses.step;
        
        const response = {
          id: `response-${Date.now()}`,
          conversationId,
          question,
          answer: `Building on that... ${baseResponse.substring(0, 200)}...`,
          strategy,
          timestamp: new Date().toISOString(),
        };

        resolve({ success: true, data: response });
      }, 1500);
    });
  },

  getRecommendedQuestions: async (lectureId) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const questions = [
          'Can you explain the time complexity of this algorithm?',
          'How would you optimize this solution?',
          'What are common edge cases for this problem?',
          'Can you provide a real-world example?',
          'How does this compare to other approaches?',
        ];

        resolve({ success: true, data: questions });
      }, 300);
    });
  },

  generateSummary: async (lectureId) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const summary = `This lecture covers fundamental concepts of algorithms and data structures. Key topics include sorting, searching, and optimization techniques. Students should focus on understanding time and space complexity trade-offs.`;

        resolve({ success: true, data: { summary, keypoints: [] } });
      }, 1000);
    });
  },

  markResponseHelpful: async (responseId, helpful) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ success: true, message: 'Feedback recorded' });
      }, 300);
    });
  },
};
