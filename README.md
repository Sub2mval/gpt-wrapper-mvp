# gpt-wrapper-mvp
# GPT Wrapper MVP

A secure, minimal GPT-powered Pythonic web app for two distinct agency clients (marketing and recruiting). This application uses Streamlit for the UI, the TogetherAI API for language model generation, and guarantees full data isolation between clients.

## Features

- **Secure Multi-Client Login**: Hardcoded login system ensures clients only see their own data.
- **Data Isolation**: Files and prompts are stored in client-specific directories (`uploads/marketing/`, `uploads/recruiting/`).
- **Text-to-Copy Generator**: Generates 3 variants of text copy based on user input, format, and tone.
- **Client-Specific Prompts**: Uses tailored prompt templates for marketing and recruiting needs.
- **Naive RAG**: Enhances prompts with context from uploaded `.txt` and `.md` files.
- **File Management**: Users can upload and delete their context files directly in the UI.
- **Streamlit Cloud Ready**: Designed to be easily deployed on Streamlit Cloud.

## Project Structure
/gpt-wrapper-mvp
├── app.py # Main Streamlit app
├── auth.py # User credentials and roles
├── prompt_templates.py # Client-specific prompt templates
├── utils.py # Helper functions (API calls, file I/O)
├── uploads/
│ ├── marketing/ # Marketing client's files (.gitkeep)
│ └── recruiting/ # Recruiting client's files (.gitkeep)
├── .env # API keys and environment variables
├── requirements.txt # Python dependencies
└── README.md