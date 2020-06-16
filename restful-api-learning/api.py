from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

groceries = {
    'groce1': {'item': 'food'},
    'groce2': {'item': 'water'},
    'groce3': {'item': 'fruit'},
}

def abort_item_not_found(item_id):
    if item_id not in groceries:
        abort(404, message="Item {} not found".format(item_id))

parser = reqparse.RequestParser()
parser.add_argument('item')

class Grocery(Resource):
    def get(self, item_id):
        abort_item_not_found(item_id)
        return {item_id: groceries[item_id]}

    def delete(self, item_id):
        abort_item_not_found(item_id)
        del groceries[item_id]
        return '', 204

    def put(self, item_id):
        args = parser.parse_args()
        item = {'item': args['item']}
        groceries[item_id] = item
        return '', 201

class GroceryList(Resource):
    def get(self):
        return(groceries)
    def post(self):
        args = parser.parse_args()
        item_id = int(max(groceries.keys()).lstrip('groce')) + 1
        item_id = 'groce%i' % item_id
        groceries[item_id] = {'item': args['item']}
        return groceries[item_id], 201

api.add_resource(GroceryList, '/grocery')
api.add_resource(Grocery, '/grocery/<item_id>')


if __name__ == '__main__':
    app.run(debug=True)
