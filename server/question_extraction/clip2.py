import clip
from PIL import Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
image_path = "images/tamgiac.png"
content = ["Triangle ABC is a right triangle with the right angle at A.", "Triangle ABC", "Rectangle ABCD"]

def process(content, path):
    image = preprocess(Image.open(path)).unsqueeze(0).to(device)
    text = clip.tokenize(content).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
    return probs

probs = process(content, image_path)
print(probs)