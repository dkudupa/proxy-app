import streamlit as st
from groq import Groq
from gtts import gTTS
import requests
import io

# 1. Page Configuration
st.set_page_config(page_title="Proxy Alpha", page_icon="🛡️")
st.title("🛡️ Proxy")
st.subheader("The Shadow-Self Agent")
st.write("Voice your chaotic thoughts. Proxy will structure the path forward and speak right back to you.")

# 2. Sidebar Configuration
st.sidebar.header("Setup Configuration")
user_key = st.sidebar.text_input("Paste your free Groq API Key:", type="password")

# Secure Account Credentials for Vapi's Outbound Engine
# NOTE: Replace with your copied Private Secret Key from Vapi Dashboard -> API Keys
VAPI_PRIVATE_KEY = "9e86d08a-bb8b-498f-98df-7df2dab89304"
VAPI_AGENT_ID = "7cb60ce4-684d-4f58-af4e-f156d89f2e60"

if not user_key:
    st.info("💡 To start, paste your free Groq API key in the sidebar.")
else:
    client = Groq(api_key=user_key)
    
    # 3. Native Python Audio Recorder
    audio_data = st.audio_input("Record your thoughts:")

    if audio_data is not None:
        # We use session state to preserve data across button reruns
        if 'ai_strategy' not in st.session_state:
            if st.button("🚀 Consult Proxy Agent", type="primary", use_container_width=True):
                
                # --- STEP A: Audio Transcribe ---
                with st.spinner("Proxy is listening..."):
                    transcription = client.audio.transcriptions.create(
                        file=("voice_dump.wav", audio_data.read()),
                        model="whisper-large-v3",
                        response_format="text"
                    )
                
                # --- STEP B: AI Strategy Generation ---
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
                    st.session_state.ai_strategy = completion.choices[0].message.content

                # --- STEP C: Text-to-Speech Generation ---
                with st.spinner("Synthesizing audio output..."):
                    speech_text = f"Here is your strategic plan. {st.session_state.ai_strategy}"
                    tts = gTTS(text=speech_text, lang='en', tld='com')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.session_state.speech_bytes = fp.read()

        # Display Outputs if they exist
        if 'ai_strategy' in st.session_state:
            st.markdown("---")
            st.header("🎯 Proxy's Verdict")
            st.audio(st.session_state.speech_bytes, format="audio/mp3")
            st.markdown(st.session_state.ai_strategy)
            
            # --- STEP D: OUTBOUND TELEPHONY TASK AUTOMATION ---
            st.markdown("---")
            st.subheader("🤖 Delegate to Proxy Outbound")
            st.write("Ready to hand off the task entirely? Enter the target company phone number below and Proxy will call them to execute the strategy.")
            
            target_business_number = st.text_input("Enter destination number (e.g., +15551234567 or standard local format):", placeholder="+1...")
            
            if st.button("☎️ Deploy Proxy (Place Call)", type="secondary", use_container_width=True):
                if not target_business_number:
                    st.error("Please provide a valid destination phone number.")
                elif VAPI_PRIVATE_KEY == "YOUR_VAPI_PRIVATE_KEY_HERE":
                    st.error("Developer Alert: Please insert your actual Vapi Private API Key on line 18!")
                else:
                    with st.spinner("Injecting strategy parameters into phone system trunk..."):
                        # Endpoint to trigger an automated backend call
                        vapi_url = "https://api.vapi.ai/call"
                        headers = {
                            "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        # We pass the custom strategy into the assistant's instruction block dynamically!
                        payload = {
                            "assistantId": VAPI_AGENT_ID,
                            "assistantOverrides": {
                                "instructions": f"You are Proxy. Your job is to call a business and execute this administrative strategy flawlessly on behalf of your client. Act professional, clear, and direct. Strategy to execute:\n{st.session_state.ai_strategy}"
                            },
                            "customer": {
                                "number": target_business_number
                            }
                        }
                        
                        try:
                            response = requests.post(vapi_url, json=payload, headers=headers)
                            if response.status_code in [200, 201]:
                                st.success(f"🚀 Proxy has deployed! Outbound line connected to {target_business_number}. Checking dashboard call logs.")
                            else:
                                st.error(f"Telephony error: {response.text}")
                        except Exception as e:
                            st.error(f"Uplink Connection Failed: {str(e)}")