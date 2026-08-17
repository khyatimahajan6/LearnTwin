# 🧠 LearnTwin AI Professor

### An Adaptive AI Learning System using NLP, RAG, Embeddings, Generative AI and Learning-Twin Feedback

---

## 📌 Project Overview

**LearnTwin AI Professor** is an adaptive AI-powered learning platform designed to provide students with a personalized learning experience.

The system allows students to upload lecture material in different formats such as documents, audio, video and YouTube lectures. The uploaded content is processed, converted into structured text, analyzed using NLP, divided into chunks, converted into embeddings and stored in a vector database.

When a student asks a question, the system retrieves the most relevant information from the student's lecture and provides it to Gemini as context through a **Retrieval-Augmented Generation (RAG)** pipeline.

The system also generates quizzes, evaluates student performance, identifies weak topics and maintains a **Learning Twin** representing the student's learning state.

The overall learning cycle is:

> **Teach → Assess → Analyze → Adapt**

---

# 🎯 Problem Statement

Traditional learning systems generally provide the same explanation to every student.

However, every student has different:

- Learning speed
- Understanding level
- Strong topics
- Weak topics
- Preferred learning approaches

A normal chatbot also does not automatically know the exact content of a student's lecture.

Therefore, there is a need for a system that can:

1. Understand the student's lecture material.
2. Answer questions using lecture-specific information.
3. Assess student understanding.
4. Identify weak topics.
5. Maintain a representation of the student's learning state.
6. Adapt future teaching accordingly.

---

# 💡 Proposed Solution

LearnTwin AI Professor combines multiple AI technologies into one learning pipeline.

The system:

- Accepts lecture material.
- Extracts or transcribes lecture content.
- Cleans and normalizes the text.
- Performs NLP processing.
- Extracts topics and keywords.
- Detects difficulty information.
- Splits lectures into chunks.
- Generates embeddings.
- Stores embeddings in ChromaDB.
- Retrieves relevant content using semantic similarity.
- Uses RAG to provide context to Gemini.
- Generates personalized explanations.
- Generates quizzes.
- Analyzes quiz performance.
- Identifies weak topics.
- Updates the Learning Twin.
- Supports adaptive teaching strategies.

---

# 🏗️ System Architecture

```text
                         LEARN TWIN AI PROFESSOR
                                  │
                                  ▼
                           Lecture Input
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                Documents                    Media
             PDF/DOCX/PPTX             Audio/Video/YouTube
                    │                           │
                    ▼                           ▼
             Text Extraction              Faster Whisper
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                            Text Cleaning
                                  │
                                  ▼
                            NLP Processing
                                  │
                       ┌──────────┼──────────┐
                       ▼          ▼          ▼
                    Topics    Keywords   Difficulty
                       │
                       ▼
                    Chunking
                       │
                       ▼
                  Embeddings
                       │
                       ▼
                    ChromaDB
                       │
                       ▼
               Semantic Retrieval
                       │
                       ▼
                 Context Building
                       │
                       ▼
                     Gemini
                       │
                       ▼
                  AI Professor
                       │
                       ▼
                     Quiz
                       │
                       ▼
              Performance Analysis
                       │
                       ▼
                 Learning Twin
                       │
                       ▼
              Adaptive Strategy
                       │
                       └──────────────► Teach Again
