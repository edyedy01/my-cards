from flask import Flask, request, jsonify
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mtg-cards.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
engine = create_engine("sqlite:///mtg-cards.db")
Base.metadata.create_all(engine, checkfirst=True)

class Card(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    scryfall_link: Mapped[str] = mapped_column(String(250), unique=True, nullable=True)

with app.app_context():
    db.create_all()

def save_card(card):
    with app.app_context():
        db.session.add(card)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Exception:  {e}")
            return 0
    return 1

def get_all_card():
    with app.app_context():
        result = db.session.execute(db.select(Card).order_by(Card.title))
        return result.scalars().all()

def delete_card_by_id(card_id: int):
    """Deletes a card record directly by ID without loading the object first."""
    # 1. Define the Delete Statement
    # The delete() function specifies the table (Card) and the filter (id=card_id).
    statement = db.delete(Card).where(Card.id == card_id)
    # 2. Execute the Statement
    # The statement is executed directly against the database.
    try:
        db.session.execute(statement)
        # 3. Commit the Transaction
        db.session.commit()
        print(f"Successfully deleted movie with ID: {card_id}.")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting movie: {e}")
        return False

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
    card = Card(name=name, quantity=quantity, scryfall_link=None)
    # save card
    updated_row_count = save_card(card)
    # return message
    return jsonify({'added': updated_row_count}), 200

if __name__ == '__main__':
    app.run(debug=True)
