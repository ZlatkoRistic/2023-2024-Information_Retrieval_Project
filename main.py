from transformers import GPT2LMHeadModel, GPT2Tokenizer
from fact_checking import FactChecker

def main(claim, evidence):
    _claim = claim
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    fact_checker = FactChecker(fact_checking_model, tokenizer)
    is_claim_true = fact_checker.validate(evidence, _claim)

    print(is_claim_true)


if __name__ == '__main__':
    claim = "The earth is flat."
    main(claim, evidence="The earth is round.")