from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/blenderbot-400M-distill"  # Changed from the larger model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, use_safetensors=False)  # Disable safetensors to use default format
tokenizer = AutoTokenizer.from_pretrained(model_name)

conversation_history = []
history_string = "\n".join(conversation_history)
input_text = "hello, how are you doing?"
inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")

outputs = model.generate(**inputs)
response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
print(response)

conversation_history.append(input_text)
conversation_history.append(response)

while True:
    # Create conversation history string
    history_string = "\n".join(conversation_history[-4:])  # Keep only last 2 interactions

    # Get the input data from the user
    input_text = input("> ")

    # Tokenize the input text and history
    inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")

    # Generate the response from the model
    outputs = model.generate(**inputs)

    # Decode the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
    print(response)

    # Add interaction to conversation history
    conversation_history.append(input_text)
    conversation_history.append(response)
