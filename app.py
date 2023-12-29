#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask
from flask import request, send_file

import render

app = Flask(__name__)

PORT = 5997

@app.route('/make/<tpl>', methods=['POST'])
def make(tpl="sorry"):
    a = request.get_data()
    idx_sentence = json.loads(a)
    sentences = list(idx_sentence.keys())
    for idx, sentence in idx_sentence.items():
        sentences[int(idx)] = sentence
    gif_path = render.make(tpl, sentences)
    return send_file(gif_path, mimetype='image/gif')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=False)
