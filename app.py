import json
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from summarize import summarize

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')


def parse_attr(data, attr, default = None):
	if attr not in data or not data[attr]:
		return default
	return data[attr]

@app.route("/api/textsum", methods=['POST'])
def textsum():
	data = request.json
	if 'text' not in data or not ['text']:
		result = 'Something wrong!'

	text = parse_attr(data, 'text', '')
	phrase_limit = int(parse_attr(data, 'phrase_limit', 12))
	word_limit = int(parse_attr(data, 'phrase_limit', 150))

	print(phrase_limit, word_limit)

	result, phrases = summarize(text, phrase_limit, word_limit)

	return jsonify({'message': result, 'keywords': phrases})

if __name__ == "__main__":
	app.run(debug=1, host="0.0.0.0", port=8080)