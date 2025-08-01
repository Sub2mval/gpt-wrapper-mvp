# app.py

import streamlit as st
from dotenv import load_dotenv
import os

from auth import USERS
from prompt_templates import PROMPT_TEMPLATES
from utils import (
    setup_client_directories,
    get_rag_context,
    save_uploaded_file,
    get_client_files,
    delete_client_file,
    generate_content
)

# Load environment variables from .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Agency GPT Wrapper",
    page_icon="🤖",
    layout="wide"
)

# --- Function Definitions ---

def login_form():
    """Displays the login form and handles authentication logic."""
    st.header("🔑 Secure Client Login")
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username").lower()
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user_data = USERS.get(username)
            if user_data and user_data["password"] == password:
                st.session_state.authenticated = True
                st.session_state.client = user_data["client"]
                st.rerun()  # Rerun to show the main app
            else:
                st.error("Invalid username or password")

def logout():
    """Logs the user out by clearing relevant session state variables."""
    st.session_state.authenticated = False
    st.session_state.client = None
    # Clear other potential session data if needed
    if 'generated_content' in st.session_state:
        del st.session_state.generated_content
    st.success("You have been logged out.")
    st.rerun()

def display_file_manager():
    """Manages file uploads, display, and deletion in the sidebar."""
    st.subheader("RAG Context Files (.txt, .md)")
    
    client = st.session_state.get('client')
    if not client:
        st.warning("No client context found.")
        return

    # File Uploader
    uploaded_files = st.file_uploader(
        "Upload files to add context to your prompts",
        type=["txt", "md"],
        accept_multiple_files=True,
        key=f"uploader_{client}"  # Unique key to prevent state issues on rerun
    )
    if uploaded_files:
        with st.spinner("Saving files..."):
            for uploaded_file in uploaded_files:
                save_uploaded_file(uploaded_file, client)
        st.success("File(s) uploaded successfully!")
        st.rerun()
    
    # Display and manage existing files
    st.markdown("---")
    st.markdown("##### Current Context Files")
    client_files = get_client_files(client)
    if not client_files:
        st.info("No files uploaded for this client yet.")
    else:
        for i, file_path in enumerate(client_files):
            col1, col2 = st.columns([4, 1])
            col1.text(file_path.name)
            if col2.button("Delete", key=f"del_{i}_{file_path.name}", use_container_width=True):
                if delete_client_file(file_path):
                    st.success(f"Deleted {file_path.name}")
                    st.rerun()
                else:
                    st.error("Failed to delete file.")

def main_app():
    """The main application interface shown after successful login."""
    client = st.session_state.client
    
    # --- Sidebar ---
    with st.sidebar:
        st.success(f"Logged in as: **{client.capitalize()} Agency**")
        st.button("Logout", on_click=logout, use_container_width=True)
        st.markdown("---")
        display_file_manager()

    # --- Main Content Area ---
    st.title("🚀 GPT-Powered Content Generator")
    st.markdown(f"Welcome! You are using the **{client.capitalize()}** prompt style.")

    with st.form("generation_form"):
        user_input = st.text_area(
            "**Enter your base content (e.g., product description, job details):**",
            height=200,
            placeholder="e.g., A new AI-powered coffee mug that keeps your drink at the perfect temperature."
        )
        
        col1, col2 = st.columns(2)
        output_format = col1.selectbox(
            "**Select Output Format:**",
            ["LinkedIn Post", "Cold Email", "Instagram Caption", "Ad Copy"]
        )
        tone = col2.selectbox(
            "**Select Tone:**",
            ["Professional", "Friendly", "Persuasive", "Playful"]
        )

        submit_button = st.form_submit_button("✨ Generate 3 Variants", use_container_width=True)

    # --- Generation and Display Logic ---
    if submit_button:
        if not user_input.strip():
            st.warning("Please enter some base content to generate from.")
        elif not os.getenv("TOGETHER_AI_KEY"): # Corrected env var name
            st.error("TOGETHER_API_KEY is not set. The app cannot contact the LLM.")
        else:
            with st.spinner("Brewing up some fresh copy... 🤖"):
                rag_context = get_rag_context(client)
                prompt_template = PROMPT_TEMPLATES[client]
                full_prompt = prompt_template.format(
                    output_format=output_format,
                    tone=tone,
                    user_input=user_input,
                    context=rag_context
                )
                
                generated_text = generate_content(full_prompt)
                st.session_state.generated_content = generated_text

    if 'generated_content' in st.session_state:
        st.markdown("---")
        st.subheader("Generated Variants")
        variants = st.session_state.generated_content.split("---VARIANT---")
        
        if len(variants) > 1 and any(v.strip() for v in variants):
            for i, variant in enumerate(variants):
                variant_text = variant.strip()
                if variant_text:
                    st.markdown(f"**Variant {i+1}**")
                    st.code(variant_text, language='text')
        else:
            st.error("Could not parse distinct variants from the output. Displaying raw result:")
            st.code(st.session_state.generated_content, language='text')


# --- App Entrypoint ---
def main():
    """Main function to run the Streamlit app."""
    # Ensure client directories exist on startup
    setup_client_directories()

    # Initialize session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "client" not in st.session_state:
        st.session_state.client = None

    if st.session_state.authenticated:
        main_app()
    else:
        login_form()

if __name__ == "__main__":
    main()