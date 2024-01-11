import pathlib

from flask import Blueprint, render_template, request
from utils import verification, precision
from src.vsm.vsm import VSM

from transformers import GPT2Tokenizer, GPT2LMHeadModel
from fact_checking import fact_checker
views = Blueprint(__name__, "views")

# Initialize fact checking and models.
FACT_CHECK_TOKEN_COUNT_MAX: int = 1024
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
fact = fact_checker(fact_checking_model, tokenizer)

this_file_path: str = pathlib.Path(__file__).parent.resolve().as_posix()
VSM_INDEX_DUMP_PATH: str = this_file_path + "/src/wikipedia/corpus/index.dump"
vsm = VSM()
with open(VSM_INDEX_DUMP_PATH, "r", encoding="utf8") as index_file:
    vsm.loads(index_file.read())


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/submit", methods=["GET"])
def submit():
    args = request.args
    claim = args.get('claim')
    k: int = 3
    evidence = []

    top_k = vsm.get_top_k(claim, k)
    has_results: bool = len(top_k) > 0

    best_id: int = top_k[0][0]
    fact_check_evidence: str = ""

    if has_results:
        verification_evidence_path: str = this_file_path + f"/src/wikipedia/corpus/processed-articles/{best_id}.txt"
        with open(verification_evidence_path, "r", encoding="utf8") as processed_file:
            fact_check_evidence = vsm._tokenizer.tokenize(processed_file.read(), do_stemming=False)[:FACT_CHECK_TOKEN_COUNT_MAX]

        evidence = [ str(top_id) for top_id, score in top_k ]

    result: bool = fact.validate(' '.join(fact_check_evidence), claim)

    return render_template("evidence.html", claim=claim, result=result, evidence=evidence)


@views.route("/show_document", methods=["GET"])
def show_document():
    args = request.args
    page = args.get('pagenr')

    page_name = "./raw-articles/" + str(page) + ".html"

    return render_template(page_name)


@views.route("/evaluate", methods=["GET"])
def evaluate():
    args = request.args
    eval_input = args.get("input")
    eval_output = args.get("output")

    correct, incorrect, total = verification(eval_input, eval_output)
    precis = precision(correct, total)

    return render_template("evaluation.html", precis=precis)

