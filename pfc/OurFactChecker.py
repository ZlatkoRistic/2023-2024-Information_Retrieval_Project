import torch
_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class OurFactChecker:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def validate(self, evidence, claim):
        # Make a prompt to feed to the model.
        prompt = f"Evidence:\n{evidence}\n\nClaim:\n{claim}\n\nDoes the evidence support the claim?:\n"
        # Generate the response of the model.
        text = self.__val(prompt)
        # Check if Yes is in the text on the end.
        if "Yes" in text[-10:]:
            return True
        return False

    def __val(self,prompt):
        # We evaluate the model
        self.model.eval()
        # Connect to the device
        self.model.to(_device)
        # We encode our tokens
        # Prompt is how we want to ask it
        tokens = self.tokenizer.encode(prompt, return_tensors='pt')
        # We get the output
        output = self.model.generate(tokens.to(_device), max_length=1024, pad_token_id=50256)
        # Let it decode back in text.
        text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return text