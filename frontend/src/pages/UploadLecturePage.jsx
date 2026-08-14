import React, { useState } from 'react';
import { DashboardLayout } from '../components/Layout';
import { Card, Button, Input, Textarea, Select, Alert } from '../components/UI';
import { Upload, FileText, Music, Video, Link as LinkIcon, CheckCircle } from 'lucide-react';
import { cn } from '../utils/helpers';

const uploadTypes = [
  { id: 'pdf', name: 'PDF', icon: FileText, description: 'Upload PDF documents' },
  { id: 'ppt', name: 'PowerPoint', icon: FileText, description: 'PPT & PPTX files' },
  { id: 'doc', name: 'Word Document', icon: FileText, description: 'DOC & DOCX files' },
  { id: 'audio', name: 'Audio', icon: Music, description: 'MP3, WAV, M4A' },
  { id: 'video', name: 'Video', icon: Video, description: 'MP4, MOV, MKV' },
  { id: 'youtube', name: 'YouTube', icon: LinkIcon, description: 'YouTube URL' },
];

const processingStages = [
  { id: 'uploading', label: 'Uploading', icon: '📤' },
  { id: 'extracting', label: 'Extracting', icon: '📄' },
  { id: 'transcribing', label: 'Transcribing', icon: '🎙️' },
  { id: 'cleaning', label: 'Cleaning', icon: '🧹' },
  { id: 'nlp', label: 'NLP Analysis', icon: '🧠' },
  { id: 'embeddings', label: 'Embeddings', icon: '✨' },
  { id: 'ready', label: 'Ready', icon: '✅' },
];

export default function UploadLecturePage() {
  const [selectedType, setSelectedType] = useState('pdf');
  const [uploading, setUploading] = useState(false);
  const [currentStage, setCurrentStage] = useState(0);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [lectureData, setLectureData] = useState({
    title: '',
    subject: '',
    topic: '',
    description: '',
    fileUrl: '',
  });
  const [extractedData, setExtractedData] = useState({
    topic: 'Binary Search',
    keywords: ['algorithm', 'divide and conquer', 'O(log n)', 'efficiency'],
    difficulty: 'Intermediate',
    objectives: ['Understand the concept', 'Implement the algorithm', 'Analyze time complexity'],
  });

  const handleUpload = async () => {
    if (!lectureData.title || !lectureData.subject) {
      alert('Please fill in all required fields');
      return;
    }

    setUploading(true);
    setUploadComplete(false);

    // Simulate processing stages
    for (let i = 0; i < processingStages.length; i++) {
      setCurrentStage(i);
      await new Promise((resolve) => setTimeout(resolve, 1200));
    }

    setUploadComplete(true);
    setUploading(false);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-2">
            Upload Lecture Material
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Upload your lecture in any format and let AI process it
          </p>
        </div>

        {uploadComplete ? (
          <Card className="p-8 text-center">
            <div className="mb-6">
              <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-50 mb-2">
                Upload Successful!
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Your lecture has been processed and is ready for learning
              </p>
            </div>

            <div className="grid md:grid-cols-4 gap-4 mb-6">
              <div className="p-4 bg-gray-50 dark:bg-dark-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400">Topic</p>
                <p className="font-semibold text-gray-900 dark:text-gray-50">
                  {extractedData.topic}
                </p>
              </div>
              <div className="p-4 bg-gray-50 dark:bg-dark-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400">Difficulty</p>
                <p className="font-semibold text-gray-900 dark:text-gray-50">
                  {extractedData.difficulty}
                </p>
              </div>
              <div className="p-4 bg-gray-50 dark:bg-dark-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400">Keywords</p>
                <p className="font-semibold text-gray-900 dark:text-gray-50">
                  {extractedData.keywords.length} found
                </p>
              </div>
              <div className="p-4 bg-gray-50 dark:bg-dark-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400">Objectives</p>
                <p className="font-semibold text-gray-900 dark:text-gray-50">
                  {extractedData.objectives.length} identified
                </p>
              </div>
            </div>

            <div className="mb-6 text-left">
              <h3 className="font-semibold text-gray-900 dark:text-gray-50 mb-3">
                Learning Objectives
              </h3>
              <ul className="space-y-2">
                {extractedData.objectives.map((obj, i) => (
                  <li key={i} className="flex items-start gap-3 text-gray-700 dark:text-gray-300">
                    <CheckCircle size={18} className="text-green-600 mt-0.5 flex-shrink-0" />
                    {obj}
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex gap-3 justify-center">
              <Button
                variant="primary"
                onClick={() => {
                  setUploadComplete(false);
                  setCurrentStage(0);
                  setLectureData({
                    title: '',
                    subject: '',
                    topic: '',
                    description: '',
                    fileUrl: '',
                  });
                }}
              >
                Upload Another
              </Button>
              <Button variant="secondary">
                Start Learning
              </Button>
            </div>
          </Card>
        ) : uploading ? (
          <Card className="p-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-50 text-center mb-8">
              Processing Your Lecture...
            </h2>

            <div className="space-y-4 mb-8">
              {processingStages.map((stage, i) => (
                <div
                  key={stage.id}
                  className={cn(
                    'flex items-center gap-4 p-4 rounded-lg transition-colors',
                    i < currentStage
                      ? 'bg-green-50 dark:bg-green-900'
                      : i === currentStage
                        ? 'bg-blue-50 dark:bg-blue-900 ring-2 ring-blue-500'
                        : 'bg-gray-50 dark:bg-dark-700'
                  )}
                >
                  <span className="text-2xl">{stage.icon}</span>
                  <div className="flex-1">
                    <p
                      className={cn(
                        'font-semibold',
                        i < currentStage
                          ? 'text-green-700 dark:text-green-300'
                          : i === currentStage
                            ? 'text-blue-700 dark:text-blue-300'
                            : 'text-gray-700 dark:text-gray-300'
                      )}
                    >
                      {stage.label}
                    </p>
                  </div>
                  {i < currentStage && (
                    <CheckCircle className="text-green-600" size={20} />
                  )}
                  {i === currentStage && (
                    <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                  )}
                </div>
              ))}
            </div>

            <div className="text-center text-gray-600 dark:text-gray-400">
              <p>
                Stage {currentStage + 1} of {processingStages.length}
              </p>
            </div>
          </Card>
        ) : (
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Upload Form */}
            <Card className="lg:col-span-2 p-6">
              <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-6">
                Lecture Details
              </h2>

              <form className="space-y-4">
                <Input
                  label="Lecture Title *"
                  placeholder="e.g., Binary Search Fundamentals"
                  value={lectureData.title}
                  onChange={(e) =>
                    setLectureData({ ...lectureData, title: e.target.value })
                  }
                />

                <Input
                  label="Subject *"
                  placeholder="e.g., Data Structures"
                  value={lectureData.subject}
                  onChange={(e) =>
                    setLectureData({ ...lectureData, subject: e.target.value })
                  }
                />

                <Input
                  label="Topic"
                  placeholder="e.g., Searching Algorithms"
                  value={lectureData.topic}
                  onChange={(e) =>
                    setLectureData({ ...lectureData, topic: e.target.value })
                  }
                />

                <Textarea
                  label="Description"
                  placeholder="Add notes or description about this lecture..."
                  rows={4}
                  value={lectureData.description}
                  onChange={(e) =>
                    setLectureData({ ...lectureData, description: e.target.value })
                  }
                />

                {selectedType === 'youtube' ? (
                  <Input
                    label="YouTube URL"
                    placeholder="https://youtube.com/watch?v=..."
                    value={lectureData.fileUrl}
                    onChange={(e) =>
                      setLectureData({ ...lectureData, fileUrl: e.target.value })
                    }
                  />
                ) : (
                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-gray-50 mb-2">
                      Upload File
                    </label>
                    <div className="border-2 border-dashed border-gray-300 dark:border-dark-600 rounded-lg p-8 text-center cursor-pointer hover:border-primary-500 transition-colors">
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                      <p className="text-gray-700 dark:text-gray-300 font-medium mb-1">
                        Click to upload or drag and drop
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Supported: PDF, PPT, DOC, Audio, Video
                      </p>
                    </div>
                  </div>
                )}

                <Button
                  type="button"
                  variant="primary"
                  size="lg"
                  className="w-full"
                  onClick={handleUpload}
                >
                  Process Lecture
                </Button>
              </form>
            </Card>

            {/* Upload Types */}
            <Card className="p-6">
              <h2 className="text-xl font-bold text-gray-900 dark:text-gray-50 mb-4">
                Supported Formats
              </h2>

              <div className="space-y-2">
                {uploadTypes.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setSelectedType(type.id)}
                    className={cn(
                      'w-full text-left p-3 rounded-lg border-2 transition-colors',
                      selectedType === type.id
                        ? 'border-primary-600 bg-primary-50 dark:bg-primary-900'
                        : 'border-gray-200 dark:border-dark-700 hover:border-primary-400'
                    )}
                  >
                    <type.icon
                      size={18}
                      className={cn(
                        'mb-1',
                        selectedType === type.id
                          ? 'text-primary-600'
                          : 'text-gray-600 dark:text-gray-400'
                      )}
                    />
                    <p
                      className={cn(
                        'font-semibold text-sm',
                        selectedType === type.id
                          ? 'text-primary-700 dark:text-primary-300'
                          : 'text-gray-900 dark:text-gray-50'
                      )}
                    >
                      {type.name}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {type.description}
                    </p>
                  </button>
                ))}
              </div>

              <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  💡 <strong>Pro Tip:</strong> Supported formats are automatically extracted,
                  transcribed, and processed. Content is indexed in our vector database for
                  intelligent searching.
                </p>
              </div>
            </Card>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
