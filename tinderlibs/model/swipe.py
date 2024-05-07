from sqlalchemy import Column, String, Date, ForeignKey
from model import Base
from model.user import User

class Swipe(Base):
	__tablename__ = "swipes"
	id_from = Column(String,
			  ForeignKey(User.id),
			  primary_key=True,
			  nullable=False)
	id_to = Column(String,
			  ForeignKey(User.id),
			  primary_key=True,
			  nullable=False)
	r = Column(String, nullable=False)
	timestamp = Column(Date, nullable=False)

	def __repr__(self):
		return f"Swipe({self.r} | from: {self.id_from}, to:{self.id_to})"
	def __str__(self):
		return f"Swipe({self.r} | rom: {self.id_from}, to:{self.id_to})"
