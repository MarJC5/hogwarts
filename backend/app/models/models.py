from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from app.database.db import Base
import enum
from sqlalchemy.orm import relationship
from datetime import datetime

class House(str, enum.Enum):
    GRYFFINDOR = "Gryffindor"
    HUFFLEPUFF = "Hufflepuff"
    RAVENCLAW = "Ravenclaw"
    SLYTHERIN = "Slytherin"

class Wizard(Base):
    __tablename__ = "wizards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    house = Column(Enum(House))
    wand = Column(String)
    patronus = Column(String, nullable=True)
    
    # Relationship to house points earned by this wizard
    points_earned = relationship("HousePoints", back_populates="wizard")

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    house = Column(Enum(House), nullable=True)  # Head of house (can be null if not a head)
    
    # Relationship to house points awarded by this teacher
    points_awarded = relationship("HousePoints", back_populates="teacher")

class HousePoints(Base):
    __tablename__ = "house_points"
    
    id = Column(Integer, primary_key=True, index=True)
    house = Column(Enum(House), nullable=False)
    points = Column(Integer, nullable=False)
    reason = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Teacher who awarded the points
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    teacher = relationship("Teacher", back_populates="points_awarded")
    
    # Student who earned the points (optional - can be null for house-wide awards)
    wizard_id = Column(Integer, ForeignKey("wizards.id"), nullable=True)
    wizard = relationship("Wizard", back_populates="points_earned") 