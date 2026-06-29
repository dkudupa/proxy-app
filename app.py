import streamlit as st
from groq import Groq

# 1. Setting up the App Page Style
st.set_page_config(page_title="Proxy Alpha", page_icon="🛡️")
st.title("🛡️ Proxy")
st.subheader("The Shadow-Self Agent")
st.write("Record your anxious, messy thoughts. Let the AI clear the logistical friction.")

# 2. Sidebar setup for your Key
st.sidebar.header("Setup Configuration")
user_key = st.sidebar.text_input("Paste your free Groq API Key:", type="password")

# Fixed Active Credentials for Vapi Voice Infrastructure
VAPI_PUBLIC_KEY = "c0a19fb2-3eb8-45e5-b4ee-f3688564bb6e"
VAPI_AGENT_ID = "7cb60ce4-684d-4f58-af4e-f156d89f2e60"

if not user_key:
    st.info("💡 To start, paste your free Groq API key in the sidebar.")
else:
    # Connect securely to Groq
    client = Groq(api_key=user_key)
    
    # 3. Native Microphone Input Widget
    audio_data = st.audio_input("Click the microphone icon below to record your voice dump:")

    if audio_data is not None:
        # Play the recorded message out loud
        st.audio(audio_data)
        if st.button("🚀 Process & Generate Strategy"):
            
            # --- STEP A: Transcribe the Audio ---
            with st.spinner("Transcribing your speech..."):
                transcription = client.audio.transcriptions.create(
                    file=("voice_dump.wav", audio_data.read()),
                    model="whisper-large-v3",
                    response_format="text"
                )
            
            st.success("Speech captured successfully!")
            with st.expander("Show Transcript"):
                st.write(transcription)
                
            # --- STEP B: Run AI Strategic Processing ---
            with st.spinner("Analyzing friction points and drafting solutions..."):
                master_prompt = f"""
                You are Proxy, an elite behavioral psychologist and personal assistant.
                You are helping a client who is severely anxious and avoidant regarding an everyday administrative task.
                
                Here is their unstructured, panicked raw voice transcript:
                "{transcription}"
                
                Please generate a clean, supportive response containing:
                1. **The Objective**: Briefly summarize exactly what needs to be done, stripping out all the user's stress.
                2. **Option A (The Copy-Paste Shield)**: A perfectly crafted text message, email, or WhatsApp message they can send to resolve the issue with no social friction.
                3. **Option B (The Script)**: A step-by-step phone blueprint or dialogue script they can follow if a voice conversation is strictly necessary.
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": master_prompt}]
                )
                
                ai_strategy = completion.choices[0].message.content

            # --- STEP C: Display the Clean Strategy ---
            st.markdown("---")
            st.header("🎯 Your Strategic Plan")
            st.markdown(ai_strategy)
            st.balloons()

# --- STEP D: LIVE AI VOICE PROXY CALLING (MOBILE-FRIENDLY AUDIO HOTLINE) ---
# Direct web voice layout URL string creation
direct_call_url = f"https://vapi.ai/embed?publicKey={VAPI_PUBLIC_KEY}&assistantId={VAPI_AGENT_ID}&mode=voice"

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎙️ Call Your AI Proxy")
    st.write("Mobile browsers often block microphones inside embedded layouts. Click the hotline button below to open an unblocked, dedicated voice portal.")
    
    # Clean mobile action component button
    st.link_button(
        "📞 Start Live Voice Call", 
        direct_call_url, 
        use_container_width=True,
        type="primary"
    )