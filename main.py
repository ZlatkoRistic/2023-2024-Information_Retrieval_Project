from transformers import GPT2LMHeadModel, GPT2Tokenizer


def main(ev):
    _evidence = ev
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    inputs = tokenizer.encode(_evidence, return_tensors='pt')
    outputs = model.generate(inputs, max_length=1000, do_sample=True, top_k=50)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(text)


if __name__ == '__main__':
    evidence = "The earth is flat."
    main(evidence)

