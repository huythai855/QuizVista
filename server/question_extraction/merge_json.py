import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Đường dẫn đến tệp JSON
json_path1 = 'all_text/response.json'
json_path2 = 'que_img/response.json'


def similarity_between_sentence(question_all, question_image):
  vectorizer = TfidfVectorizer()
  tfidf_matrix = vectorizer.fit_transform([question_all, question_image])
  similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
  return similarity


# Function to add similarity scores to each question in json_data2
def update_json_with_similarities(json_path1, json_path2, output_path):
    # Read the JSON files
    with open(json_path1, 'r', encoding='utf-8') as f:
        json_data1 = json.load(f)

    with open(json_path2, 'r', encoding='utf-8') as f:
        json_data2 = json.load(f)

    # Extract questions
    question_text1 = [(question_key, question_content.get("Câu hỏi")) for question_key, question_content in json_data1.items()]
    question_text2 = [(question_key, question_content.get("Câu hỏi")) for question_key, question_content in json_data2.items()]

    # Initialize similarity values
    for k1, q1 in question_text1:
        max_value = -10000
        for k2, q2 in question_text2:
            b1 = similarity_between_sentence(q1, q2)
            b1_value = b1[0][0]
            if b1_value > max_value:
                max_value = b1_value
                best_key2 = k2
                best_key1 = k1

        # Update the best similarity value in json_data2
        if best_key1 is not None:
            link = json_data1[best_key1].get("link_image")
            json_data2[best_key2]['link_image'] = {}
            json_data2[best_key2]['link_image'] = link

    # Write the updated JSON data to a new file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data2, f, ensure_ascii=False, indent=4)
