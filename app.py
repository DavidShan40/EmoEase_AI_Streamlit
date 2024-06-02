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
character = st.sidebar.selectbox("Customize Character:", ["Select", "Lover", "Friend", "Pet", "Family Member", "Doctor"], index=0)
goal = st.sidebar.selectbox("Choose your Goal - Emoease:", ["Select", "Bully", "Depression", "Anxiety", "Breakup", "Failure"], index=0)
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

	if user_name != "User not specified":
		st.session_state["messages"] = [{"role": "assistant", "content": f"Hi {user_name}, nice to meet you!"}]
	else:
		st.session_state["messages"] = [{"role": "assistant", "content": f"Hi, nice to meet you!"}]
	if (bot_name != '') and character != "User not specified":
		st.session_state["messages"]+=[{"role": "assistant", "content": f"My name is {bot_name} and I'm your {character}"}]
	st.session_state["messages"]+=[{"role": "assistant", "content": "I'm here to relieve your stress and boost your mood Today. Feel free to talk about anything you met."}]		
	st.session_state["messages"]+=[{"role": "assistant", "content": "How can I help you?"}]


# Define the main chat interface
st.markdown("<h1 style='text-align: center;'>EmoEase AI - Chat with AI </h1>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .large-arrow {
        font-size: 48px;
        margin-right: 10px;
    }
    </style>
    <div class="container">
        <p class="large-arrow">&#10229;</p>
        <h5 style='text-align: center;'>Choose your preferences</h5>
    </div>
""", unsafe_allow_html=True)

# Backend
# ************************************************

# initial Setting
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
max_output_token = 4096
#model = "gpt-4"
#model = "gpt-3.5-turbo"
model = "gpt-4o-2024-05-13"
# system_prompt = "You are an AI Application Agent, to provide step-by-step guidance to help users solve their problems. \
# 	For each query, detail the steps the user should take. \
# 	The output need to tell user's situation, steps to solve the problem, and future possible advices.\
# 	Ensure the response is safe and secure. \
# 	Do not provide any advice that could be unsafe or unethical\
# 	Additional: use first person's view to response"
with open('system_prompt.txt', 'r') as file:
    # Read the contents of the file
    system_prompt = file.read()

user_prompt = f"\
User's name is {user_name} \
User's Pronoun is {pronouns} \
User's Age Group is {age_group} \
Your name is {bot_name} \
You should act as {character} \
User's Goal: {goal} \
"
system_prompt += user_prompt

# non-changeable setting
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
if "message_GPT" not in st.session_state:
	st.session_state["message_GPT"] = None
if "messages" not in st.session_state:
	if user_name != "User not specified":
		st.session_state["messages"] = [{"role": "assistant", "content": f"Hi {user_name}, nice to meet you!"}]
	else:
		st.session_state["messages"] = [{"role": "assistant", "content": f"Hi, nice to meet you!"}]
	if (bot_name != '') and character != "User not specified":
		st.session_state["messages"]+=[{"role": "assistant", "content": f"My name is {bot_name} and I'm your {character}"}]
	st.session_state["messages"]+=[{"role": "assistant", "content": "I'm here to relieve your stress and boost your mood Today. Feel free to talk about anything you met."}]		
	st.session_state["messages"]+=[{"role": "assistant", "content": "How can I help you?"}]

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
	print(message_GPT)

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
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;

        padding: 10px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
	col1, col2 = st.columns([2, 8])
	with col1:
		text = whisper_stt(openai_api_key=openai_api_key)
	with col2:
		input = st.chat_input()

with st.container():
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

# # Define the scroll operation as a function and pass in something unique for each
# # page load that it needs to re-evaluate where "bottom" is
# js = f"""
# <script>
#     function scroll(dummy_var_to_force_repeat_execution){{
#         var textAreas = parent.document.querySelectorAll('section.main');
#         for (let index = 0; index < textAreas.length; index++) {{
#             textAreas[index].style.color = 'red';
#             if (textAreas[index].scrollTop !== textAreas[index].scrollHeight) {{
#                 textAreas[index].scrollTop = textAreas[index].scrollHeight;
#             }}
#         }}
#     }}
#     scroll({0.1})
# </script>
# """

# st.components.v1.html(js)
