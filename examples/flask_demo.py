from flask import Flask, request, jsonify, abort
from pydantic import BaseModel, Schema
from random import random

from spectree import SpecTree, Response


app = Flask(__name__)
api = SpecTree('flask')


class Query(BaseModel):
    text: str


class Resp(BaseModel):
    label: int
    score: float = Schema(
        ...,
        gt=0,
        lt=1,
    )


class Data(BaseModel):
    uid: str
    limit: int
    vip: bool


@app.route('/api/predict/<string(length=2):source>/<string(length=2):target>', methods=['POST'])
@api.validate(query=Query, json=Data, resp=Response('HTTP_403', HTTP_200=Resp), tags=['model'])
def predict(source, target):
    """
    predict demo

    demo for `query`, `data`, `resp`, `x`
    """
    print(f'=> from {source} to {target}')  # path
    print(f'JSON: {request.context.json}')  # Data
    print(f'Query: {request.context.query}')  # Query
    if random() < 0.5:
        abort(403)
    return Resp(label=int(10 * random()), score=random())


@app.route('/api/header', methods=['POST'])
@api.validate(resp=Response('HTTP_203'), tags=['test', 'demo'])
def with_code_header():
    """
    demo for JSON with status code and header
    """
    return jsonify('header'), 203, {'X': 233}


if __name__ == '__main__':
    api.register(app)
    app.run()
