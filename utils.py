# utils.py
import streamlit as st
import os
from together import Together
from pathlib import Path
from typing import List

os.environ["TOGETHER_API_KEY"] = st.secrets["TOGETHER_AI_KEY"]
# Set up the base directory for uploads
UPLOAD_DIRECTORY = Path("uploads")
client = Together(api_key = st.secrets["TOGETHER_AI_KEY"])

def setup_client_directories():
    """Ensures that client-specific upload directories exist."""
    for client in ["marketing", "recruiting"]:
        (UPLOAD_DIRECTORY / client).mkdir(parents=True, exist_ok=True)

def get_rag_context(client: str) -> str:
    """
    Reads all .txt and .md files from a client's directory and concatenates their content
    to form a RAG context string.

    Args:
        client (str): The client identifier ('marketing' or 'recruiting').

    Returns:
        str: A single string containing the content of all context files.
    """
    client_dir = UPLOAD_DIRECTORY / client
    context_parts = []
    
    if not client_dir.exists():
        return "No context files found."

    files = list(client_dir.glob("*.txt")) + list(client_dir.glob("*.md"))

    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8').strip()
            if content:
                context_parts.append(f"--- Context from: {file_path.name} ---\n{content}")
        except Exception as e:
            context_parts.append(f"--- Could not read file: {file_path.name} (Error: {e}) ---")

    if not context_parts:
        return "No context files found for this client."
        
    return "\n\n".join(context_parts)

def save_uploaded_file(uploaded_file, client: str) -> Path:
    """Saves an uploaded file to the specific client's directory."""
    client_dir = UPLOAD_DIRECTORY / client
    file_path = client_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def get_client_files(client: str) -> List[Path]:
    """Lists all files for a given client."""
    client_dir = UPLOAD_DIRECTORY / client
    if not client_dir.exists():
        return []
    return [f for f in client_dir.iterdir() if f.is_file()]

def delete_client_file(file_path: Path) -> bool:
    """Deletes a specific file."""
    try:
        os.remove(file_path)
        return True
    except OSError:
        return False

def generate_content(prompt: str) -> str:
    """
    Generates content using the TogetherAI API.
    
    Args:
        prompt (str): The complete prompt to send to the LLM.
        
    Returns:
        str: The generated content from the LLM, or an error message.
    """
    api_key = st.secrets["TOGETHER_AI_KEY"]
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable not set.")
    
     
    
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that strictly follows user instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3072,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the TogetherAI API call: {e}"
