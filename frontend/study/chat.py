import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")


def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


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
    ['Hello, I\'m Thai',
     'How is my learning progress recently?',
     'Show me questions that I got wrong',
     'Yes, please!',
     'show me some markdown sample',
     'table in markdown']
)
st.session_state.setdefault(
    'generated',
    [{'type': 'normal', 'data': "Hi! I'm BotVista. I'm here to help you with your study."},
     {'type': 'normal', 'data': f'Well, I think you are doing great!\n You have completed 3 out of 5 lessons with an average score of 95%'},
     {'type': 'normal', 'data': "Here are the questions that you got wrong:\n 1. Question 1: Who is the first President of America? \n2. Question 2: What is the capital of France? \n3. Question 3: What is the largest desert in the world? \n \n Do you want to see the explanation of the questions?"},
     {'type': 'normal', 'data': f'{youtube_embed}'},
     {'type': 'normal', 'data': f'{markdown}'},
     {'type': 'table', 'data': f'{table_markdown}'}]
)

st.title("Learn with AI Mentor - BotVista")

chat_placeholder = st.empty()

with chat_placeholder.container():
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'],
            key=f"{i}",
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type'] == 'table' else False
        )

    st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")