from flask import Flask, request, jsonify

from Card import Card
from MyCardsDatabaseManager import MyCardsDatabaseManager

app = Flask(__name__)

db = MyCardsDatabaseManager()
db.connect() #tested and works
db.setup_tables() #tested and works

@app.route("/api/mtg/add-card", methods=['POST'])
def add_card():
    # error check
    if not request.is_json:
        return jsonify({'error': 'Request must be in JSON format only'}), 400
    # collect data
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    # init card
    card = Card(name=name, quantity=quantity)
    # save card
    updated_row_count = db.save_card(card)
    # return message
    return jsonify({'added': updated_row_count}), 200

if __name__ == '__main__':
    app.run(debug=True)
