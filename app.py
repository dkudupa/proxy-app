import streamlit as st
from groq import Groq
import requests

# 1. Setting up the App Page Style
st.set_page_config(page_title="Proxy Alpha", page_icon="🛡️")
st.title("🛡️ Proxy")
st.subheader("The Shadow-Self Agent")

# 2. Sidebar setup for your Keys
st.sidebar.header("Setup Configuration")
user_key = st.sidebar.text_input("Paste your free Groq API Key:", type="password")

# Fixed Vapi credentials for backend processing
VAPI_PRIVATE_KEY = "c0a19fb2-3eb8-45e5-b4ee-f3688564bb6e" # Change to private key if using advanced endpoints
VAPI_AGENT_ID = "7cb60ce4-684d-4f58-af4e-f156d89f2e60"

# Main Application Router
st.markdown("### 🎙️ Talk to Your Proxy")
st.write("Record your anxious thoughts below. Your agent will analyze your friction points and speak back to you natively.")

if not user_key:
    st.info("💡 To start, paste your free Groq API key in the sidebar.")
else:
    client = Groq(api_key=user_key)
    
    # Pure Python Native Microphone Widget
    audio_data = st.audio_input("Record your voice message:")

    if audio_data is not None:
        # Save and playback recorded file natively
        st.audio(audio_data)
        
        if st.button("🚀 Send to Proxy Agent", type="primary", use_container_width=True):
            
            # --- STEP A: Transcribe the Audio via Groq ---
            with st.spinner("Proxy is listening..."):
                transcription = client.audio.transcriptions.create(
                    file=("voice_dump.wav", audio_data.read()),
                    model="whisper-large-v3",
                    response_format="text"
                )
            
            # --- STEP B: Run AI Strategic Processing ---
            with st.spinner("Formulating strategy..."):
                master_prompt = f"""
                You are Proxy, an elite behavioral psychologist and personal assistant.
                Analyze the user's unstructured task transcript and provide:
                1. The Objective (Simple summary)
                2. Option A (A frictionless message shield they can copy-paste)
                3. Option B (A clean phone call script if a conversation is required)

                User input: "{transcription}"
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": master_prompt}]
                )
                ai_strategy = completion.choices[0].message.content

            # --- STEP C: Display outputs directly in application layer ---
            st.markdown("---")
            st.header("🎯 Your Strategic Plan")
            st.markdown(ai_strategy)
            st.balloons()