from transformers import T5Tokenizer, LongformerTokenizer, T5ForConditionalGeneration
from nltk.tokenize import sent_tokenize
## preprocessing 
def preprocessing_input_qa(tokenizer: T5Tokenizer, context: str, device): 

    text_encoding = tokenizer(context, return_tensors="pt") 
    input_ids = text_encoding["input_ids"].to(device)
    return input_ids 


def preprocessing_input_distract(tokenizer: T5Tokenizer, context: str, question: str, answer: str, device, spetoken: str = "<sep>"): 

    input_text = question + ' ' + spetoken + ' ' + answer + ' ' + spetoken + ' ' + context
    text_encoding = tokenizer(input_text, return_tensors="pt")
    input_ids = text_encoding["input_ids"].to(device)
    return input_ids

def sentence_tokenize(context: str): 
    """
    xóa các câu có độ dài nhỏ hơn 20 
    """
    sentences = [sent_tokenize(context)]
    sentences = [y for x in sentences for y in x]
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences



def preprocessing_input_bool(tokenizer: T5Tokenizer, context: str, device, answer: bool): 
    form = "truefalse: %s passage: %s </s>" % (context, answer)

    text_encoding = tokenizer.encode_plus(form, return_tensors="pt")
    input_ids, att_mask = text_encoding["input_ids"].to(device), text_encoding["attention_mask"].to(device)
    return input_ids, att_mask


## decoding method 
def beamsearch_encoding(input_ids, att_mask, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, num_question: int): 
    beam_output = model.generate(
        input_ids=input_ids, 
        attention_mask=att_mask, 
        max_length=256, 
        num_beams=5, 
        num_return_sequences=num_question,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    questions = [tokenizer.encode(output, skip_special_tokens=True,clean_up_tokenization_spaces = True) for output in beam_output]

    return [question.strip().capitalize() for question in questions]

def greedysearch_encoding(input_ids, att_mask, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer):
    greedy_output = model.generate(
        input_ids = input_ids,
        attention_mask = att_mask,
        max_length = 256
    )

    output = tokenizer.decode(greedy_output[0], skip_special_tokens=True, clean_up_tokenization_spaces = True)
    return output.strip().capitalize()
