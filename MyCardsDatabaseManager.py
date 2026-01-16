import sys
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Card import Card

# Define the Base class for ORM models
Base = declarative_base()

class MyCardsDatabaseManager:
    """
    Data Access Object (DAO) using SQLAlchemy ORM.
    No manual SQL scripts or strings are used here.
    """

    def __init__(self):
        # Database URL format: mariadb+mariadbconnector://user:password@host:port/dbname
        self.user = "my_cards_user"
        self.password = "my_cards_user"
        self.host = "127.0.0.1"
        self.port = 3307
        self.db_name = "my_cards"

        self.url = f"mariadb+mariadbconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.engine = None
        self.Session = None

    def connect(self):
        """Initializes the engine and session factory."""
        try:
            self.engine = create_engine(self.url, pool_recycle=3600)
            self.Session = sessionmaker(bind=self.engine)
            print("Successfully connected to MariaDB via SQLAlchemy")
        except Exception as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)

    def setup_tables(self):
        """Creates all tables defined in the ORM models automatically."""
        try:
            Base.metadata.create_all(self.engine)
            print("Database schema synchronized successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")


    def save_card(self, card_instance):
        """Saves a Card instance to the database."""
        session = self.Session()
        try:
            session.add(card_instance)
            session.commit()
            session.refresh(card_instance)  # Get the newly generated ID
            return card_instance.id
        except Exception as e:
            print(f"Error saving card: {e}")
            session.rollback()
            return None
        finally:
            session.close()

    def update_card(self, card_id, **kwargs):
        """Updates a card using dynamic keyword arguments."""
        session = self.Session()
        try:
            card = session.query(Card).filter(Card.id == card_id).first()
            if not card:
                return False
            for key, value in kwargs.items():
                if hasattr(card, key) and value is not None:
                    setattr(card, key, value)
            session.commit()
            return True
        except Exception as e:
            print(f"Error updating card: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def delete_card(self, card_id):
        """Deletes a card record using the ORM."""
        session = self.Session()
        try:
            card = session.query(Card).filter(Card.id == card_id).first()
            if card:
                session.delete(card)
                session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting card: {e}")
            session.rollback()
            return False
        finally:
            session.close()