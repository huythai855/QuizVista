from transformers import T5Tokenizer, LongformerTokenizer

def preprocessing_input_qa(tokenizer: T5Tokenizer, context: str, device): 

    text_encoding = tokenizer(context, return_tensors="pt") 
    input_ids = text_encoding["input_ids"].to(device)
    return input_ids 


def preprocessing_input_distract(tokenizer: T5Tokenizer, context: str, question: str, answer: str, device, spetoken: str = "<sep>"): 

    input_text = question + ' ' + spetoken + ' ' + answer + ' ' + spetoken + ' ' + context
    text_encoding = tokenizer(input_text, return_tensors="pt")
    input_ids = text_encoding["input_ids"].to(device)
    return input_ids


def preprocessing_input_ans(tokenizer:LongformerTokenizer, question: str, optiton: list, context: str, device, max_seq: int = 4096): 
    pass 
