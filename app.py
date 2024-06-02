import streamlit as st
from openai import OpenAI
import os
# self defined
from whisper_stt import whisper_stt

# Front End
# ***************************************************************

# Set up the page configuration
st.set_page_config(page_title="Chat Interface", layout="wide")


# Sidebar settings
st.sidebar.title("Settings")
st.sidebar.write("Choose your preferences")

user_name = st.sidebar.text_input("Enter your name:", placeholder="Enter your name")
pronouns = st.sidebar.selectbox("Your Pronouns:", ["Select", "She", "He", "They"], index=0)
age_group = st.sidebar.selectbox("Your Age Group:", ["Select", "18-24", "25-34", "35-44", "45-54", "55-64", "65 and over"], index=0)
bot_name = st.sidebar.text_input("Name for the bot:", placeholder="Enter bot name")
character = st.sidebar.selectbox("Customize Character:", ["Select", "Lover", "Friend", "Pet", "Family", "Doctor", "Other"], index=0)
goal = st.sidebar.selectbox("Choose your Goal - Emoease:", ["Select", "Bully", "Depression", "Anxiety", "Breakup", "Failure", "Other"], index=0)
st.session_state["User_Choices"] = {user_name, ...}

if st.sidebar.button("All done, start with your journey"):
	if (user_name == ""):
		user_name = "User not specified"
	if (pronouns == "Select"):
		pronouns = "User not specified"
	if (age_group == "Select"):
		age_group = "User not specified"
	if (bot_name == ""):
		bot_name = "User not specified"
	if (character == "Select"):
		character = "User not specified"
	if (goal == "Select"):
		goal = "User not specified"
	
	st.session_state['user_choices'] = {
		"user_name": user_name,
		"pronouns": pronouns,
		"age_group": age_group,
		"bot_name": bot_name,
		"character": character,
		"goal": goal
	}
	
	# for debug
	st.sidebar.write(f"Name: {user_name}")
	st.sidebar.write(f"Pronouns: {pronouns}")
	st.sidebar.write(f"Age Group: {age_group}")
	st.sidebar.write(f"Bot Name: {bot_name}")
	st.sidebar.write(f"Character: {character}")
	st.sidebar.write(f"Goal: {goal}")


# Define the main chat interface
st.markdown("<h1 style='text-align: center;'>Chat with Your AI Friend</h1>", unsafe_allow_html=True)

# Backend
# ************************************************

# initial Setting
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
max_output_token = 4096
#model = "gpt-4"
#model = "gpt-3.5-turbo"
model = "gpt-4o-2024-05-13"
system_prompt = "You are an AI Application Agent, to provide step-by-step guidance to help users solve their problems. \
	For each query, detail the steps the user should take. \
	The output need to tell user's situation, steps to solve the problem, and future possible advices.\
	Ensure the response is safe and secure. \
	Do not provide any advice that could be unsafe or unethical\
	Additional: use first person's view to response"

# non-changeable setting
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
if "message_GPT" not in st.session_state:
	st.session_state["message_GPT"] = None
if "messages" not in st.session_state:
	st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
for msg in st.session_state.messages:
	st.chat_message(msg["role"]).write(msg["content"])

def get_response(question, pre_message=None, pre_answer=None):
	if pre_message == None:
		message_GPT = [
					{"role": "system", "content": system_prompt},
					{"role": "user", "content": question},
				]
	else:
		message_GPT = pre_message
		message_GPT.append({"role": "assistant", "content": pre_answer})
		message_GPT.append({"role": "user", "content": question})

	try:
		response = client.chat.completions.create(
			model=model,  # Specify the model, adjust if a different version is desired
			messages=message_GPT, max_tokens=max_output_token
		)
		return response.choices[0].message.content, message_GPT
	except Exception as e:
		return f"An error occurred: {str(e)}"

# input = st.chat_input()
# text = whisper_stt(openai_api_key=openai_api_key)  
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"]{
        position:relative;
        right: 10px;
        left: 10px;
        bottom: -300px;
        border: 2px;
        background-color: #EEEEEE;
        padding: 10px;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True
)
with st.container():
	col1, col2 = st.columns([2, 8])
	with col1:
		text = whisper_stt(openai_api_key=openai_api_key)
	with col2:
		input = st.chat_input()


if prompt := input or (prompt := text):
	st.session_state.messages.append({"role": "user", "content": prompt})
	st.chat_message("user").write(prompt)
	#print(st.session_state.messages)
	if st.session_state["message_GPT"] == None:
		msg, message_GPT = get_response(st.session_state.messages[-1]['content'])
	else:
		msg, message_GPT = get_response(st.session_state.messages[-1]['content'], st.session_state["message_GPT"], st.session_state.messages[-2]['content'])
	st.session_state["message_GPT"] = message_GPT
	st.session_state.messages.append({"role": "assistant", "content": msg})
	st.chat_message("assistant").write(msg)
