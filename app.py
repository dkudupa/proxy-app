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

# Shared verified account constants
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

# --- STEP D: UNBLOCKED WEB TALK LINK FOR MOBILE & DESKTOP ---
# Secure web client link structure generated to launch out of sandboxes cleanly
clean_vapi_web_link = f"https://vapi.ai/?assistantId={VAPI_AGENT_ID}&publicKey={VAPI_PUBLIC_KEY}"

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎙️ Talk Live with Proxy")
    st.write("Launch a full-screen, unblocked direct voice link to speak seamlessly with your custom agent.")
    
    # Native Streamlit Link Button out of iframes
    st.link_button(
        "⚡ Launch Secure Voice Link",
        clean_vapi_web_link,
        use_container_width=True,
        type="primary"
    )
    
    # QR code generator interface for rapid mobile scanning
    qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={clean_vapi_web_link}"
    st.markdown("<br><p style='text-align: center; color: gray; font-size: 13px;'>Or scan this on your phone to open instantly:</p>", unsafe_allow_html=True)
    st.image(qr_api_url, use_container_width=False)