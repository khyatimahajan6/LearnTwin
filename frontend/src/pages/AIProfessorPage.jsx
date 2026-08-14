import React, { useState, useEffect, useRef } from 'react';
import { DashboardLayout } from '../components/Layout';
import { lectureService } from '../services/lectureService';
import { ragService } from '../services/ragService';
import { Card, Button, Input, Badge, Loading, Select } from '../components/UI';
import {
  Send, Lightbulb, BookMarked, Smile, Code, Copy, Check,
  Volume2, MessageCircleQuestion, Sparkles,
} from 'lucide-react';
import { teachingStrategies, mockAIResponses } from '../data/mockData';
import { formatDateTime } from '../utils/helpers';
import clsx from 'clsx';

export default function AIProfessorPage() {
  const [lectures, setLectures] = useState([]);
  const [selectedLecture, setSelectedLecture] = useState(null);
  const [strategy, setStrategy] = useState('step');
  const [messages, setMessages] = useState([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI Twin Professor. Select a lecture and ask me anything about it. You can also choose how you prefer to learn!',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [lectureLoading, setLectureLoading] = useState(true);
  const [copiedId, setCopiedId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadLectures();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadLectures = async () => {
    setLectureLoading(true);
    const result = await lectureService.getLectures();
    if (result.success) {
      setLectures(result.data);
      setSelectedLecture(result.data[0]);
    }
    setLectureLoading(false);
  };

  const handleSendMessage = async () => {
    if (!input.trim() || !selectedLecture || loading) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const result = await ragService.askQuestion(
        selectedLecture.id,
        input,
        strategy
      );

      if (result.success) {
        const aiMessage = {
          id: `ai-${Date.now()}`,
          role: 'assistant',
          content: result.data.answer,
          sources: result.data.sources,
          strategy,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, aiMessage]);
      }
    } catch (err) {
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const renderMessageContent = (content, isCode = false) => {
    if (isCode) {
      return (
        <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
          <code>{content}</code>
        </pre>
      );
    }

    // Handle basic formatting
    return (
      <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
        {content}
      </p>
    );
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 h-full">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            AI Professor
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Chat with your AI tutor about any lecture
          </p>
        </div>

        {lectureLoading ? (
          <div className="flex justify-center py-12">
            <Loading size="lg" />
          </div>
        ) : (
          <div className="grid lg:grid-cols-4 gap-6 h-[calc(100vh-300px)]">
            {/* Sidebar */}
            <Card className="lg:col-span-1 p-4 flex flex-col">
              <h2 className="font-bold text-gray-900 dark:text-gray-50 mb-4">
                Lectures
              </h2>
              <div className="space-y-2 flex-1 overflow-y-auto">
                {lectures.map((lecture) => (
                  <button
                    key={lecture.id}
                    onClick={() => setSelectedLecture(lecture)}
                    className={clsx(
                      'w-full text-left p-3 rounded-lg transition-colors border-2',
                      selectedLecture?.id === lecture.id
                        ? 'border-primary-600 bg-primary-50 dark:bg-primary-900'
                        : 'border-gray-200 dark:border-dark-700 hover:border-primary-400'
                    )}
                  >
                    <p className="font-semibold text-sm text-gray-900 dark:text-gray-50 truncate">
                      {lecture.title}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400 truncate">
                      {lecture.topic}
                    </p>
                  </button>
                ))}
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-dark-700">
                <h3 className="font-semibold text-sm text-gray-900 dark:text-gray-50 mb-3">
                  Teaching Strategy
                </h3>
                <Select
                  options={teachingStrategies.map((s) => ({
                    value: s.id,
                    label: s.name,
                  }))}
                  value={strategy}
                  onChange={(e) => setStrategy(e.target.value)}
                />
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-2">
                  {teachingStrategies.find((s) => s.id === strategy)?.description}
                </p>
              </div>
            </Card>

            {/* Chat Area */}
            <Card className="lg:col-span-3 flex flex-col">
              {/* Header */}
              <div className="border-b border-gray-200 dark:border-dark-700 p-4">
                {selectedLecture && (
                  <div>
                    <h2 className="font-bold text-gray-900 dark:text-gray-50">
                      {selectedLecture.title}
                    </h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {selectedLecture.topic} • {selectedLecture.difficulty}
                    </p>
                  </div>
                )}
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={clsx(
                      'flex gap-3',
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    )}
                  >
                    {message.role === 'assistant' && (
                      <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white flex-shrink-0">
                        <Sparkles size={18} />
                      </div>
                    )}

                    <div
                      className={clsx(
                        'max-w-xs lg:max-w-md xl:max-w-lg rounded-lg p-4',
                        message.role === 'user'
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 dark:bg-dark-800 text-gray-900 dark:text-gray-50'
                      )}
                    >
                      {renderMessageContent(message.content)}

                      {message.role === 'assistant' && (
                        <div className="mt-3 pt-3 border-t border-gray-300 dark:border-dark-600">
                          <div className="flex gap-2 flex-wrap">
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-xs"
                              onClick={() =>
                                copyToClipboard(message.content, message.id)
                              }
                            >
                              {copiedId === message.id ? (
                                <>
                                  <Check size={14} /> Copied
                                </>
                              ) : (
                                <>
                                  <Copy size={14} /> Copy
                                </>
                              )}
                            </Button>
                            <Button variant="ghost" size="sm" className="text-xs">
                              <Volume2 size={14} /> Read
                            </Button>
                            <Button variant="ghost" size="sm" className="text-xs">
                              <BookMarked size={14} /> Bookmark
                            </Button>
                          </div>

                          {message.sources && (
                            <div className="mt-3 text-xs">
                              <p className="font-semibold mb-1 text-gray-700 dark:text-gray-300">
                                Sources:
                              </p>
                              {message.sources.map((source, i) => (
                                <p key={i} className="text-gray-600 dark:text-gray-400">
                                  • {source.title} (p. {source.page})
                                </p>
                              ))}
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {message.role === 'user' && (
                      <div className="w-8 h-8 bg-gray-300 dark:bg-dark-600 rounded-full flex items-center justify-center text-gray-700 dark:text-gray-300 flex-shrink-0 text-sm font-bold">
                        U
                      </div>
                    )}
                  </div>
                ))}

                {loading && (
                  <div className="flex gap-3">
                    <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white">
                      <Sparkles size={18} />
                    </div>
                    <div className="bg-gray-100 dark:bg-dark-800 rounded-lg p-4 flex gap-2">
                      <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" />
                      <div
                        className="w-2 h-2 bg-primary-600 rounded-full animate-bounce"
                        style={{ animationDelay: '0.2s' }}
                      />
                      <div
                        className="w-2 h-2 bg-primary-600 rounded-full animate-bounce"
                        style={{ animationDelay: '0.4s' }}
                      />
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Quick Questions */}
              {messages.length <= 1 && (
                <div className="border-t border-gray-200 dark:border-dark-700 p-4">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    Quick questions to get started:
                  </p>
                  <div className="grid grid-cols-2 gap-2">
                    {[
                      'What are the key concepts?',
                      'How do I apply this?',
                      'Can you explain it simply?',
                      'What are common mistakes?',
                    ].map((q, i) => (
                      <button
                        key={i}
                        onClick={() => setInput(q)}
                        className="text-left text-sm p-2 bg-gray-100 dark:bg-dark-700 hover:bg-gray-200 dark:hover:bg-dark-600 rounded text-gray-700 dark:text-gray-300"
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Input */}
              <div className="border-t border-gray-200 dark:border-dark-700 p-4">
                <div className="flex gap-2">
                  <Input
                    placeholder="Ask anything about this lecture..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage();
                      }
                    }}
                    disabled={loading}
                  />
                  <Button
                    variant="primary"
                    size="md"
                    onClick={handleSendMessage}
                    loading={loading}
                    disabled={loading || !input.trim()}
                  >
                    <Send size={18} />
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
