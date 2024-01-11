from flask import Blueprint, render_template, request
from utils import verification, precision
from src.vsm.vsm import VSM

from transformers import GPT2Tokenizer, GPT2LMHeadModel
from src.pfc.OurFactChecker import OurFactChecker

views = Blueprint(__name__, "views")

# Initizalize fact checking and models.
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
fact = OurFactChecker(fact_checking_model, tokenizer)

vsm = VSM()
if False:
    with open("index.dump", "r") as index_file:
        vsm.loads(index_file.read())


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/submit", methods=["GET"])
def submit():
    args = request.args
    claim = args.get('claim')

        evidence = [ str(top_id) for top_id, score in top_k ]

    result: bool = fact.validate(' '.join(fact_check_evidence), claim)

    return render_template("evidence.html", claim=claim, result=result, evidence=["6678"])


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

