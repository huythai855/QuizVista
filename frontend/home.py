import time
import streamlit as st

st.set_page_config(layout="centered")

# Custom CSS for centered layout, colors, and grid styling
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
        color: #333333;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 15px;
    }
    .button-container button {
        background-color: #00bfff;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        padding: 20px;
        max-width: 900px;
        margin: auto;
    }
    .card {
        background-color: #e0f7fa;
        margin-bottom: 40px;
        margin-left: 40px;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        color: #00796b;
        text-align: center;
        transition: transform 0.2s;

    }
    .card:hover {
        transform: scale(1.05);
        background-color: #b2ebf2;
    }
    .footer {
        margin-top: 3em;
        color: #888888;
        font-size: 0.9em;
        text-align: center;
    }
    .footer a {
        color: #00bcd4;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Heading and subheading
st.markdown("<h1 class='centered-text'>Welcome to QuizVista</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='centered-text'>The ultimate platform for learning and testing your knowledge</h2>", unsafe_allow_html=True)

# Paragraph
st.markdown("<p class='centered-text'>Start your journey with QuizVista to test and improve your knowledge.</p>", unsafe_allow_html=True)

st.text("")
# Buttons
# col1, col2, col3, col4 = st.columns([2, 3, 3, 1])
# with col2:
#     if st.button("Get Started"):
#         st.write("Redirecting to Get Started...")
#
# with col3:
#     if st.button("Learn More"):
#         st.write("Redirecting to Learn More...")

# Image (if applicable)
st.image("data/1.png", use_column_width=True)

# Feature Cards in a 2x3 grid
features = [
    {"title": "Tự động sinh câu hỏi", "description": "Tạo câu hỏi tự động từ tài liệu."},
    {"title": "Hỗ trợ đa dạng tệp đầu vào", "description": "Tạo bài kiểm tra từ nhiều dạng đầu vào như pdf, docx, ảnh, v.v."},
    {"title": "Đa dạng loại câu hỏi", "description": "Tạo câu hỏi trắc nghiệm, tự luận, điền từ, đúng/sai, v.v."},
    {"title": "Tạo Mindmap, Flashcard, Ghi chú", "description": "Sinh mindmap, flashcard và ghi chú học từ nội dung bài học."},
    {"title": "Quản lý lớp học", "description": "Tổ chức lớp, theo dõi thành viên và bài kiểm tra dễ dàng."},
    {"title": "Thống kê", "description": "Cung cấp biểu đồ và đề xuất học tập phù hợp từng cá nhân."},
]

# Container for grid layout
st.markdown("<div class='grid-container'>", unsafe_allow_html=True)

rows = [features[i:i + 2] for i in range(0, len(features), 2)]  # Splitting into rows of 2 columns

for row in rows:
    cols = st.columns(2)
    for idx, feature in enumerate(row):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="card" style="background-color: #e0f7fa; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); text-align: center;">
                    <h3 style="color: #00796b;">{feature['title']}</h3>
                    <p>{feature['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p>Connect with us on <a href="https://www.linkedin.com/company/quizvista">LinkedIn</a> | Contact: <a href="mailto:support@quizvista.com">support@quizvista.com</a></p>
        <p>© 2024 QuizVista. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)