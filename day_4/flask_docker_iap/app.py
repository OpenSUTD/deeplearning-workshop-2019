print(" * [i] Loading Python modules...")
import time
import flask
import functools

print(" * [i] Loading NLP models...")
from model_nlp import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

app = flask.Flask(__name__)

sentiment_model = sentiment_classifier()
sia = SIA()

@functools.lru_cache(maxsize=128, typed=False)
def pred_sentiment(input_):
    global sentiment_model, data
    data["sentiment"] = sentiment_model.predict(input_)

data = {"success": False}

@app.route("/predict", methods=["POST"])
def predict():
    global sentiment_model, data

    # get the respective args from the post request

    if flask.request.method == "POST":
        start_time = time.time()

        data = {"success": False}
        start_time = time.time()
        test_text = flask.request.args.get("test")
        test_text = test_text.replace("%20", " ")

        pred_sentiment(test_text)

        nltk_sentiment = sia.polarity_scores(test_text)
        data["nltk"] = nltk_sentiment

        data["success"] = True

        print(" * [i] Request took", round(time.time()-start_time, 3), "seconds")

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if file was executed by itself, start the server process
if __name__ == "__main__":
    print(" * [i] Starting Flask server")
    app.run(host='0.0.0.0', port=5000)