# 🎥 YouTube Video Chat — AI-Powered Q&A from YouTube Videos  

A web app that lets you **chat with YouTube videos** — just paste a video link, and start asking questions related to that video!  
The app extracts the video’s transcript and allows you to interact with it conversationally using natural language processing.  

---

## 🧩 Project Overview

This project enables users to query YouTube video content using an AI model.  
It takes a YouTube URL, processes its transcript (or captions), and allows you to ask context-aware questions — just like chatting with the video itself.

**✨ Key Features**
- Paste any public YouTube video link.  
- Automatically fetch and process the video’s transcript.  
- Ask questions about the video content in plain English.  
- Get summarized, context-based answers.  
- Lightweight and easy to run locally or deploy online.  

---

## ⚙️ Tech Stack

- **Frontend:** streamlit  
- **Backend:** Python (FastAPI)  
- **Libraries & APIs:**
  - `whisper-api` — for fetching video transcripts from the audios   
  - `langchain` / `transformers` / `openai` — for question answering (depending on your implementation) 
- **Languages:** 100% Python (with HTML templates)

---

## 🖥️ Getting Started

### 1. Clone the repository  
```bash
git clone https://github.com/sh-momina/Youtube-video-chat.git
cd Youtube-video-chat
streamlit run ui.py

<img width="920" height="439" alt="image" src="https://github.com/user-attachments/assets/91e43073-b596-4b91-bb65-c3304747f48d" />
![App Preview](https://github.com/user-attachments/assets/91e43073-b596-4b91-bb65-c3304747f48d)
