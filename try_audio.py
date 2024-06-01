from streamlit_mic_recorder import mic_recorder
import streamlit as st

# def callback():
#     if st.session_state.my_recorder_output:
#         audio_bytes = st.session_state.my_recorder_output['bytes']
#         st.audio(audio_bytes)


# mic_recorder(key='my_recorder', callback=callback)

import streamlit as st
from whisper_stt import whisper_stt
import os
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
openai_api_key = os.environ.get("OPENAI_API_KEY")
text = whisper_stt(openai_api_key=openai_api_key)  
# If you don't pass an API key, the function will attempt to retrieve it as an environment variable : 'OPENAI_API_KEY'.
if text:
    st.write(text)