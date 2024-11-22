import base64
import json

import streamlit as st
import streamlit.components.v1 as components
from streamlit import button, container

from sympy import false
import requests



this_page = "create_new_test"

st.set_page_config(layout="wide")

st.markdown("# Study Notes")
st.write("Read the summary, then explore the mind map to learn more about the topic.")
st.write("")
st.write("")


# Function to generate the mindmap as a string
def generate_mindmap(data, level=0):
    mindmap = ""
    indent = "    " * level  # Adjust indentation for tree structure

    # Root level
    if level == 0:
        mindmap += "(root)\n"

    # Process each topic
    count = 0
    for topic in data["topics"]:
        count += 1


        # Process each subtopic under a topic
        if count != len(data["topics"]):
            mindmap += f"{indent}├── {topic['name']}\n"
            for subtopic in topic.get("subtopics", []):
                mindmap += f"{indent}│   ├── {subtopic['name']}\n"
            mindmap += "│ \n"
        else:
            mindmap += f"{indent}└── {topic['name']}\n"
            for subtopic in topic.get("subtopics", []):
                mindmap += f"{indent}    ├── {subtopic['name']}\n"




    return mindmap



test_id = st.query_params["test_id"]
response = requests.get(f"http://127.0.0.1:1510/api/tests/detail?test_id={test_id}")
test_data = response.json()

encoded_study_note = response.json()["study_note"]
print(encoded_study_note)

# Giải mã từ base64 sang chuỗi JSON
decoded_question_set = base64.b64decode(encoded_study_note).decode("utf-8")

# Parse chuỗi JSON thành Python dictionary
study_note = json.loads(decoded_question_set)

print(study_note)


notes = ""
for topic in study_note["topics"]:
    notes += f"## {topic['name']}\n\n"
    notes += f"{topic['details']}\n\n"
    for subtopic in topic.get("subtopics", []):
        notes += f"#### {subtopic['name']}\n"
        notes += f"{subtopic['details']}\n\n"
    notes += "\n\n\n\n\n"


print(notes)


# notes = """
#     FPT Smart Cloud là một công ty con của FPT, chuyên cung cấp các giải pháp và dịch vụ liên quan đến điện toán đám mây (cloud computing) và trí tuệ nhân tạo (AI). FPT Smart Cloud được thành lập với mục tiêu giúp các doanh nghiệp tại Việt Nam và quốc tế tăng cường khả năng số hóa, tối ưu hóa hệ thống và nâng cao năng lực cạnh tranh trong thời đại chuyển đổi số.
#     ##### FPT Cloud
#     Nền tảng điện toán đám mây toàn diện, cung cấp hạ tầng và các dịch vụ đám mây cho doanh nghiệp. FPT Cloud cho phép các tổ chức triển khai, vận hành, và quản lý hạ tầng IT của mình trên nền tảng đám mây một cách linh hoạt và bảo mật.
#     ##### FPT AI
#     Cung cấp các giải pháp trí tuệ nhân tạo như chatbot, xử lý ngôn ngữ tự nhiên, nhận dạng giọng nói, và học máy (machine learning). Các dịch vụ này hỗ trợ tự động hóa quy trình và nâng cao trải nghiệm khách hàng thông qua AI.
#     ##### Giải pháp đa đám mây (Multi-cloud Solutions)
#     Hỗ trợ doanh nghiệp quản lý các hệ thống đám mây khác nhau, chẳng hạn như AWS, Google Cloud, và Microsoft Azure, trên một nền tảng duy nhất.
#     ##### Giải pháp an ninh mạng
#     Bảo vệ hệ thống thông tin của doanh nghiệp bằng các dịch vụ bảo mật và giám sát mạng tiên tiến, giúp giảm thiểu rủi ro về bảo mật.
#     FPT Smart Cloud hướng đến việc cung cấp các giải pháp linh hoạt và toàn diện, giúp doanh nghiệp dễ dàng chuyển đổi và tận dụng các lợi ích từ điện toán đám mây và trí tuệ nhân tạo trong thời đại số hóa.
# """



box = st.container(border=True)
box.markdown(notes, unsafe_allow_html=True)


# Mind map data
mindmap = generate_mindmap(study_note)

# Display the mind map
st.text("")
st.text("")

st.markdown("# Mind Map")
box2 = st.container(border=True)
with box2:
    st.code(mindmap, language="text")


flashcard_data = {
    "topic1": {
        "name": "Word Vectors",
        "details": "Representing words as numerical vectors that capture semantic relationships.",
        "subtopics": [
            {
                "name": "Word2Vec",
                "details": "Predictive model learning word embeddings by maximizing the likelihood of predicting a target word given its context (CBOW) or vice versa (Skip-gram)."
            },
            {
                "name": "GloVe (Global Vectors for Word Representation)",
                "details": "Leverages global word co-occurrence statistics to learn word embeddings that capture both local and global context."
            },
            {
                "name": "Word Similarity and Analogy Tasks",
                "details": "Evaluating word vectors by their ability to capture semantic relationships through cosine similarity and solving analogies (e.g., king - man + woman = queen)."
            }
        ]
    },
    "topic2": {
        "name": "Backpropagation",
        "details": "Core algorithm for training neural networks by computing gradients of the loss function with respect to model parameters.",
        "subtopics": [
            {
                "name": "Chain Rule",
                "details": "Fundamental rule in calculus used to compute derivatives of composite functions, crucial for backpropagating gradients through layers of a network."
            },
            {
                "name": "Computational Graph",
                "details": "Visual representation of a mathematical expression, useful for understanding the flow of computation and backpropagation of gradients."
            },
            {
                "name": "Gradient Descent",
                "details": "Iterative optimization algorithm used to minimize the loss function by updating parameters in the direction opposite to the gradient."
            }
        ]
    },
    "topic3": {
        "name": "Recurrent Neural Networks (RNNs)",
        "details": "Neural network architecture designed for processing sequential data by maintaining a hidden state that captures information from previous time steps.",
        "subtopics": [
            {
                "name": "Vanishing and Exploding Gradients",
                "details": "Challenges in training RNNs due to the accumulation of gradients over long sequences, leading to vanishing or exploding values."
            },
            {
                "name": "Long Short-Term Memory (LSTM)",
                "details": "Specialized RNN cell with gating mechanisms (input, forget, output gates) to address the vanishing gradient problem and capture long-range dependencies."
            },
            {
                "name": "Gated Recurrent Unit (GRU)",
                "details": "Simplified RNN cell similar to LSTM but with fewer parameters, often achieving comparable performance."
            },
            {
                "name": "Applications of RNNs",
                "details": "Widely used in NLP tasks such as language modeling, machine translation, sentiment analysis, text generation, and speech recognition."
            }
        ]
    },
    "topic4": {
        "name": "Multiple Choice Questions",
        "details": "Focus on foundational concepts from the covered topics. Review definitions, key differences, and common applications of methods.",
        "subtopics": []
    },
    "topic5": {
        "name": "Short Answer Questions",
        "details": "Likely to test your understanding of core concepts and ability to apply them. Practice explaining concepts concisely and providing illustrative examples.",
        "subtopics": []
    }
}


# Hàm tạo mindmap bằng HTML
def create_mindmap(data):
    mindmap_html = """
    <style>
        .mindmap {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-family: Arial, sans-serif;
        }
        .topic {
            background-color: #ffeb3b;
            padding: 10px;
            border-radius: 10px;
            margin: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
            width: 250px;
        }
        .subtopic {
            background-color: #fff59d;
            padding: 5px;
            margin: 5px;
            border-radius: 8px;
            width: 200px;
        }
        .connector {
            width: 2px;
            height: 20px;
            background-color: #333;
            margin: 5px 0;
        }
    </style>
    <div class="mindmap">
    """
    for key, topic in data.items():
        mindmap_html += f"""
        <div class="topic">
            <strong>{topic['name']}</strong><br>
            <small>{topic['details']}</small>
        </div>
        """
        if topic['subtopics']:
            for subtopic in topic['subtopics']:
                mindmap_html += f"""
                <div class="connector"></div>
                <div class="subtopic">
                    <strong>{subtopic['name']}</strong><br>
                    <small>{subtopic['details']}</small>
                </div>
                """

    mindmap_html += "</div>"

    # Hiển thị mindmap
    components.html(mindmap_html, height=600)


# create_mindmap(flashcard_data)