import pathlib

from flask import Blueprint, render_template, request
from utils import verification, precision
from src.vsm.vsm import VSM

from transformers import GPT2Tokenizer, GPT2LMHeadModel
from src.pfc.OurFactChecker import OurFactChecker
views = Blueprint(__name__, "views")

# Initialize fact checking and models.
FACT_CHECK_TOKEN_COUNT_MAX: int = 950
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
fact = OurFactChecker(fact_checking_model, tokenizer)

this_file_path: str = pathlib.Path(__file__).parent.resolve().as_posix()
VSM_INDEX_DUMP_PATH: str = this_file_path + "/src/wikipedia/corpus/index.dump"
vsm = VSM()
with open(VSM_INDEX_DUMP_PATH, "r", encoding="utf8") as index_file:
    vsm.loads(index_file.read())


@views.route("/")
def home():
    """The route to the home page.
    This is the main page we see when starting the application and offers us access to all functionalities we would want to have available.

    :return: render_template of the index.html home page
    """
    return render_template("index.html")


@views.route("/submit", methods=["GET"])
def submit():
    """Route to submitting a claim to be checked.
    This route shall check the claim against evidence and display the result.

    Using the claim, this will retrieve the most relevant pages using a VSM.
    Then use the one most relevant page to check if the claim is supported by reading the content and passing it to GPT.
    Using the GPT model the claim is validated using the evidence(list of strings that are the names of evidence file)

    arguments:
    - claim: a statement which has to be verified by the evidence available using a GPT model

    The rendered template contains the claim, the result and a list of buttons that show evidence in new pages.

    :return: rendered template of evidence.html containing the claim, result and list of evidence buttons
    """
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
            # Read "natural language" version of evidence
            fact_check_evidence = processed_file.read()
            fact_check_evidence = ' '.join(fact_check_evidence.split(' ')[:FACT_CHECK_TOKEN_COUNT_MAX])

            # Convert "natural language" to tokens
            # fact_check_evidence = vsm._tokenizer.tokenize(processed_file.read(), do_stemming=False)[:FACT_CHECK_TOKEN_COUNT_MAX]
            # fact_check_evidence = ' '.join(fact_check_evidence)

        evidence = [ str(top_id) for top_id, score in top_k ]

    # result: bool = False

    result: bool = fact.validate(fact_check_evidence, claim)

    return render_template("evidence.html", claim=claim, result=result, evidence=evidence)


@views.route("/show_document", methods=["GET"])
def show_document():
    """Route to the evidence documents.
    This route takes an argument which should be the name of a document in the provided evidence and return it rendered.

    This document should be a html file with name 'x.html' where x is the argument passed in this function.
    The document will be rendered from the folder 'raw-articles' and the html extension should NEVER be in the argument.

    arguments:
    - pagenr: the name of the file, which must be a html file. Ex.: 'example.html', pagenr should be 'example'

    :return: rendered html file from render_template
    """
    args = request.args
    page = args.get('pagenr')

    page_name = "./raw-articles/" + str(page) + ".html"

    return render_template(page_name)


@views.route("/evaluate", methods=["GET"])
def evaluate():
    """Route for the evaluation extension of index.html.
    This route inserts the evaluation.html blocks into the blocks of index.html.

    Using the input and output arguments this route calls the verification from utils and checks the precision.
    The precision, also from utils, uses the correct and total outputs from verification to return the precision.
    This returned precision is fed into evaluation.html, which is then rendered and returned

    arguments:
    - input: relative path from the working directory to the input file to be used in the verification
    - output: relative path from the working directory to the output file to be used in the verification

    :return: rendered template with evaluation.html with a calculated precis value given
    """
    args = request.args
    eval_input = args.get("input")
    eval_output = args.get("output")

    correct, incorrect, total = verification(eval_input, eval_output)
    precis = precision(correct, total)

    return render_template("evaluation.html", precis=precis)

