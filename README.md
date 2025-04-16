# YouTube Comment Reply Bot

This project is an intelligent automation tool that analyzes the content of a YouTube video and automatically replies to comments using context-aware LLMs like Groq. It leverages video transcripts, YouTube Data API, and language models to make smart, relevant replies — perfect for content creators and corporate channels.

---

## Features

-  Extracts transcript from YouTube videos
-  Understands the context of user comments
-  Auto-generates smart replies using LLMs (Groq/GPT)
-  Modular scripts for easy integration with bots or extensions

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

---

### 2. Install Dependencies

There are two options for dependency installation depending on your need:

#### Basic Setup (minimal & recommended):
```bash
pip install -r requirementsfinal.txt
```

#### Full Setup (includes optional tools/utilities):
```bash
pip install -r requirementsfull.txt
```

> **Tip:** If you're not sure, start with `requirementsfinal.txt`.

---

### 3. Set Environment Variables

Create a `.env` file in the root directory and paste the following:

```env
API_KEY=YOUR_GOOGLE_API_KEY
groq_api_key=YOUR_GROQ_API_KEY
secret_key=YOUR_CLIENT_SECRET_KEY
token=YOUR_OAUTH_TOKEN
```

> ⚠️ Never share your actual keys publicly. This file must remain **private**.

To make sure Python reads the variables, you can use the `python-dotenv` package or load them manually in your scripts.

---

### 4. Run Credential Setup

This step verifies your authentication credentials and sets up required tokens.

```bash
python credential.py
```

---

### 5. Run the Bot

This will start analyzing the video content and automatically reply to YouTube comments based on transcript and comment context.

```bash
python reply.py
```

---

## 📌 Notes

- Make sure the video has **public captions/transcripts** available.
- You must enable **YouTube Data API v3** in your Google Cloud Console.
- The bot can be extended to reply via:
  - YouTube Studio (browser extension)
  - Telegram or Discord bots
  - Cron jobs or deployment pipelines

---

## 📁 Project Structure

```
.
├── credential.py       # Handles API authentication
├── reply.py            # Main logic for generating replies
├── requirementsfinal.txt
├── requirementsfull.txt
├── .env                # Your environment variables (not committed)
└── README.md
```

---

##  Example Use Case

1. You paste a YouTube video link.
2. The bot pulls the transcript.
3. It reads the comment section.
4. It generates a smart reply based on the video content and comment context.
5. It posts or stores the reply.

---

##  Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 🛡 Disclaimer

This project is for educational and automation purposes. Use responsibly and in compliance with YouTube's terms of service.
