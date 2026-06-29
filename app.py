import streamlit as st
from groq import Groq
from gtts import gTTS
import io

# 1. Page Configuration
st.set_page_config(page_title="Proxy Alpha", page_icon="🛡️")
st.title("🛡️ Proxy")
st.subheader("The Shadow-Self Agent")
st.write("Voice your chaotic thoughts. Proxy will structure the path forward and speak right back to you.")

# 2. Sidebar Configuration
st.sidebar.header("Setup Configuration")
user_key = st.sidebar.text_input("Paste your free Groq API Key:", type="password")

if not user_key:
    st.info("💡 To start, paste your free Groq API key in the sidebar.")
else:
    # Initialize the Groq Client natively
    client = Groq(api_key=user_key)
    
    # 3. Native Python Audio Recorder
    audio_data = st.audio_input("Record your thoughts:")

    if audio_data is not None:
        if st.button("🚀 Consult Proxy Agent", type="primary", use_container_width=True):
            
            # --- STEP A: Audio Transcribe via Groq ---
            with st.spinner("Proxy is listening..."):
                transcription = client.audio.transcriptions.create(
                    file=("voice_dump.wav", audio_data.read()),
                    model="whisper-large-v3",
                    response_format="text"
                )
            
            # --- STEP B: AI Strategy Generation via Llama ---
            with st.spinner("Formulating behavioral strategy..."):
                master_prompt = f"""
                You are Proxy, an elite behavioral psychologist and personal assistant.
                Analyze the user's unstructured task transcript and provide a highly supportive, concise plan containing:
                1. The Objective (Simple summary)
                2. Option A (A copy-paste text or email shield)
                3. Option B (A phone conversation script if necessary)

                User input: "{transcription}"
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": master_prompt}]
                )
                ai_strategy = completion.choices[0].message.content

            # --- STEP C: Bulletproof Python Text-to-Speech Generation ---
            with st.spinner("Synthesizing audio output..."):
                # Formulate a clean spoken intro text
                speech_text = f"Here is your strategic plan. {ai_strategy}"
                
                # Render using gTTS straight into a memory stream buffer
                tts = gTTS(text=speech_text, lang='en', tld='com')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                speech_bytes = fp.read()

            # --- STEP D: Render Strategy and Audio Natively ---
            st.markdown("---")
            st.header("🎯 Proxy's Verdict")
            
            # Play the assistant's voice response out loud natively
            st.audio(speech_bytes, format="audio/mp3", autoplay=True)
            
            # Display written details
            st.markdown(ai_strategy)
            st.balloons()