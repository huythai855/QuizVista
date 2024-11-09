import clip
from PIL import Image
import torch
import json
import os

# Set up device and load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        questions = {key: item["Question"] for key, item in data.items() if "Question" in item}
    return data, questions

# Function to truncate text to fit within CLIP's context length
def truncate_text(text, max_length):
    # Split the text into words
    words = text.split()
    # Truncate the words list to fit the max_length
    if len(words) > max_length:
        words = words[:max_length]
    # Join the words back into a single string
    return ' '.join(words)

# Function to compute similarity scores and update JSON
def image_text_matching(text_path, image_folder, context_length = 30):
    # Load JSON data and get questions
    data, questions = get_questions(text_path)
    
    # Iterate over each image in the folder first
    for filename in os.listdir(image_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            print(f"Processing image: {filename}")
            
            # Preprocess and encode the image
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image)

            best_prob = 0
            best_question_id = None
            
            # Iterate over each question and compare with the current image
            for question_id, question_text in questions.items():
                # Truncate the question text if it's too long
                truncated_text = truncate_text(question_text, max_length=context_length)
                
                # Tokenize the truncated question text
                text_tokens = clip.tokenize([truncated_text]).to(device)
                
                # Compute similarity between the image and the question
                logits_per_image, _ = model(image, text_tokens)
                probs = logits_per_image.detach().cpu().numpy()[0, 0]

                # Update best match if this question has a higher probability for the current image
                if probs > best_prob:
                    best_prob = probs
                    best_question_id = question_id

            # Add the best matching question for the current image
            if best_question_id:
                print(f"Best matching question for {filename}: {questions[best_question_id]}")
                if "image_link" not in data[best_question_id]:
                    data[best_question_id]["image_link"] = []
                data[best_question_id]["image_link"].append(filename)
    
    # Write the updated data back to JSON
    with open(text_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Call the function
