import config
import torch
import flask
import time
from flask import Flask
from flask import request
from flask import render_template
from model import BERTBaseUncased
import functools
import torch.nn as nn
from wtforms import Form, TextAreaField, validators
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

MODEL = None
DEVICE = config.DEVICE
PREDICTION_DICT = dict()


def sentence_prediction(sentence):
    tokenizer = config.TOKENIZER
    max_len = config.MAX_LEN
    review = str(sentence)
    review = " ".join(review.split())
    
    
    inputs = tokenizer.encode_plus(
        review, None, add_special_tokens=True, max_length=max_len
    )

    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]
    token_type_ids = inputs["token_type_ids"]

    padding_length = max_len - len(ids)
    ids = ids + ([0] * padding_length)
    mask = mask + ([0] * padding_length)
    token_type_ids = token_type_ids + ([0] * padding_length)

    ids = torch.tensor(ids, dtype=torch.long).unsqueeze(0)
    mask = torch.tensor(mask, dtype=torch.long).unsqueeze(0)
    token_type_ids = torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0)

    ids = ids.to(DEVICE, dtype=torch.long)
    token_type_ids = token_type_ids.to(DEVICE, dtype=torch.long)
    mask = mask.to(DEVICE, dtype=torch.long)

    outputs = MODEL(ids=ids, mask=mask, token_type_ids=token_type_ids)

    outputs = torch.sigmoid(outputs).cpu().detach().numpy()
    return outputs[0][0]

class InputForm(Form):
    comment = TextAreaField(u'Please input comment in this box', render_kw={"rows": 4, "cols": 11},validators=[validators.InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        comment = form.comment.data
        prediction = sentence_prediction(comment)

        if prediction >= 0.75:
            processed_text = "The comment is positive"
            link_to_pic = "https://cdn-icons-png.flaticon.com/512/742/742751.png"     

        elif prediction >=0.45:
            processed_text = "The comment is neutral"
            link_to_pic = "https://cdn-icons-png.flaticon.com/512/1933/1933511.png" 

        else:
            processed_text = "The comment is negative"
            link_to_pic = "https://cdn-icons-png.flaticon.com/512/725/725099.png"
        
    else:
        processed_text = None
        link_to_pic = ""
    s = processed_text

    return render_template("index.html", form=form, s=s, link_to_pic = link_to_pic)


@app.route("/predict")
def predict():
    sentence = request.args.get("sentence")
    start_time = time.time()
    positive_prediction = sentence_prediction(sentence)
    negative_prediction = 1 - positive_prediction
    response = {}
    response["response"] = {
        "positive": str(positive_prediction),
        "negative": str(negative_prediction),
        "sentence": str(sentence),
        "time_taken": str(time.time() - start_time),
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    MODEL = BERTBaseUncased()
    MODEL.load_state_dict(torch.load(config.MODEL_PATH, map_location=torch.device('cpu')))
    MODEL.to(DEVICE)
    MODEL.eval()
    app.run(debug=True, host="0.0.0.0", port="5000")


