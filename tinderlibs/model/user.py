from sqlalchemy import Column, String, Date, Integer
from tinderlibs.model import Base

class User(Base):
	__tablename__ = "users"
	id = Column(String, primary_key=True, nullable=False)
	birth_date = Column(Date)
	genre = Column(String)

	prefered_genre = Column(String)
	prefered_age_range_min = Column(Integer)
	prefered_age_range_max = Column(Integer)
	

	def __repr__(self):
		return f"User({self.id})"
	def __str__(self):
		return f"User({self.id})"