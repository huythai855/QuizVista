import json
import requests
import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

st.set_page_config(layout="wide")



audio_path = "https://docs.google.com/uc?export=open&id=16QSvoLWNxeqco_Wb2JvzaReSAw5ow6Cl"
img_path = "https://www.groundzeroweb.com/wp-content/uploads/2017/05/Funny-Cat-Memes-11.jpg"
youtube_embed = '''
<iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
'''

markdown = """
### HTML in markdown is ~quite~ **unsafe**
<blockquote>
  However, if you are in a trusted environment (you trust the markdown). You can use allow_html props to enable support for html.
</blockquote>

* Lists
* [ ] todo
* [x] done

Math:

Lift($L$) can be determined by Lift Coefficient ($C_L$) like the following
equation.

$$
L = \\frac{1}{2} \\rho v^2 S C_L
$$

~~~py
import streamlit as st

st.write("Python code block")
~~~

~~~js
console.log("Here is some JavaScript code")
~~~

"""

table_markdown = '''
A Table:

| Feature     | Support              |
| ----------: | :------------------- |
| CommonMark  | 100%                 |
| GFM         | 100% w/ `remark-gfm` |
'''

st.session_state.setdefault(
    'past',
    ['Good morning!',
     ]
)
st.session_state.setdefault(
    'generated',
    [{'type': 'normal', 'data': "Hi! How do you do?"},
    ]
)



GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Initialize session state if needed
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'generated' not in st.session_state:
    st.session_state['generated'] = []


def get_gemini_response(user_input):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_input  # User's input goes here
                    }
                ]
            }
        ]
    }

    # Send POST request to the Gemini API
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        data=json.dumps(data)
    )

    # Check for a successful response and retrieve text
    if response.status_code == 200:
        response_data = response.json()

        # Debug: Print parsed response to check for the structure
        print("Parsed Response Data:", response_data)

        # Extract the response text
        # Adjust this part based on the exact structure you observe in the API response
        try:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        except (IndexError, KeyError) as e:
            print("Error parsing response:", e)
            return "Error in parsing the response from Gemini."
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return "Error in fetching response from Gemini."

def get_function_calling_response(user_input):
    response = requests.post(
        "http://localhost:1513/chat",
        json={"message": user_input,
              "user_id": 1
            }
    ).json()

    return response['message']



def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)  # Append user input to past messages

    # Get response from Gemini API
    # gemini_response = get_gemini_response(user_input)
    function_calling_response = get_function_calling_response(user_input)
    # print("User Input:", function_calling_response)
    print("Function calling Response:", function_calling_response)

    # Append Gemini's response to the generated messages
    st.session_state.generated.append({"data": function_calling_response, "type": "text"})


def on_btn_click():
    # Clear conversation history
    st.session_state.past.clear()
    st.session_state.generated.clear()

st.title("Learn with AI Mentor")
st.write("Improve your study experience with BotVista, your personalized AI mentor!")
st.text("")

st.button("➕ New chat", on_click=on_btn_click)

# Display the chat UI in Streamlit

col1, col2, col3 = st.columns([0.05, 0.9, 0.05])
with col2:
    chat_placeholder = st.empty()

    with chat_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")

            # Display Bot's message with support for different types (text, table)
            message(
                st.session_state['generated'][i]['data'],
                allow_html=True,
                is_table=True if st.session_state['generated'][i]['type'] == 'table' else False,
                key=f"{i}_bot"
            )

    st.text("")
    st.text_input("Your turn:", on_change=on_input_change, key="user_input")


