from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Card(Base):
    """
    ORM Model for the 'Card' table.
    Maps to the MariaDB schema defined in create_card_table.sql.
    """
    __tablename__ = 'Card'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    scryfall_id = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    # func.now() ensures the DB handles the timestamp generation
    created_date = Column(TIMESTAMP, server_default=func.now())

    def to_dict(self):
        """
        Helper method to convert the ORM object to a dictionary.
        Useful for returning JSON responses in a REST API.
        """
        return {
            "id": self.id,
            "name": self.name,
            "scryfall_id": self.scryfall_id,
            "location": self.location,
            "quantity": self.quantity,
            "created_date": self.created_date.isoformat() if self.created_date else None
        }

    def __repr__(self):
        return f"<Card(name='{self.name}', quantity={self.quantity}, location='{self.location}')>"