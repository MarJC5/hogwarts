"""
Script to initialize the database with sample data.
"""
from sqlalchemy.orm import Session
from app.models.models import Wizard, Teacher, HousePoints, House
from app.database.db import engine, Base, get_db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def init_test_data(db: Session):
    """Initialize database with test data if tables are empty."""
    # Check if we already have data
    if db.query(Teacher).count() > 0:
        logger.info("Database already has data, skipping initialization.")
        return
    
    logger.info("Initializing database with test data...")
    
    # Add wizards (students)
    wizards = [
        # Gryffindor students
        Wizard(name="Harry Potter", house=House.GRYFFINDOR, wand="Holly and Phoenix feather, 11 inches", patronus="Stag"),
        Wizard(name="Hermione Granger", house=House.GRYFFINDOR, wand="Vine wood and Dragon heartstring, 10¾ inches", patronus="Otter"),
        Wizard(name="Ron Weasley", house=House.GRYFFINDOR, wand="Willow and Unicorn hair, 14 inches", patronus="Jack Russell Terrier"),
        Wizard(name="Neville Longbottom", house=House.GRYFFINDOR, wand="Cherry and Unicorn hair, 13 inches", patronus="Non-corporeal"),
        Wizard(name="Ginny Weasley", house=House.GRYFFINDOR, wand="Yew, unknown core", patronus="Horse"),
        
        # Slytherin students
        Wizard(name="Draco Malfoy", house=House.SLYTHERIN, wand="Hawthorn and Unicorn hair, 10 inches"),
        Wizard(name="Pansy Parkinson", house=House.SLYTHERIN, wand="Unknown"),
        Wizard(name="Blaise Zabini", house=House.SLYTHERIN, wand="Unknown"),
        Wizard(name="Gregory Goyle", house=House.SLYTHERIN, wand="Unknown"),
        Wizard(name="Vincent Crabbe", house=House.SLYTHERIN, wand="Unknown"),
        
        # Ravenclaw students
        Wizard(name="Luna Lovegood", house=House.RAVENCLAW, wand="Unknown", patronus="Hare"),
        Wizard(name="Cho Chang", house=House.RAVENCLAW, wand="Unknown", patronus="Swan"),
        Wizard(name="Padma Patil", house=House.RAVENCLAW, wand="Unknown"),
        Wizard(name="Terry Boot", house=House.RAVENCLAW, wand="Unknown"),
        Wizard(name="Michael Corner", house=House.RAVENCLAW, wand="Unknown"),
        
        # Hufflepuff students
        Wizard(name="Cedric Diggory", house=House.HUFFLEPUFF, wand="Ash, 12¼ inches, unicorn hair"),
        Wizard(name="Hannah Abbott", house=House.HUFFLEPUFF, wand="Unknown"),
        Wizard(name="Susan Bones", house=House.HUFFLEPUFF, wand="Unknown"),
        Wizard(name="Justin Finch-Fletchley", house=House.HUFFLEPUFF, wand="Unknown"),
        Wizard(name="Ernie Macmillan", house=House.HUFFLEPUFF, wand="Unknown"),
    ]
    db.add_all(wizards)
    db.commit()
    logger.info(f"Added {len(wizards)} wizards")
    
    # Refresh to get IDs
    for wizard in wizards:
        db.refresh(wizard)
    
    # Add teachers
    teachers = [
        Teacher(name="Albus Dumbledore", subject="Headmaster"),
        Teacher(name="Minerva McGonagall", subject="Transfiguration", house=House.GRYFFINDOR),
        Teacher(name="Severus Snape", subject="Potions", house=House.SLYTHERIN),
        Teacher(name="Filius Flitwick", subject="Charms", house=House.RAVENCLAW),
        Teacher(name="Pomona Sprout", subject="Herbology", house=House.HUFFLEPUFF),
        Teacher(name="Rubeus Hagrid", subject="Care of Magical Creatures"),
        Teacher(name="Horace Slughorn", subject="Potions", house=House.SLYTHERIN),
        Teacher(name="Remus Lupin", subject="Defense Against the Dark Arts"),
        Teacher(name="Sybill Trelawney", subject="Divination"),
        Teacher(name="Gilderoy Lockhart", subject="Defense Against the Dark Arts"),
    ]
    db.add_all(teachers)
    db.commit()
    logger.info(f"Added {len(teachers)} teachers")
    
    # Refresh to get IDs
    for teacher in teachers:
        db.refresh(teacher)
    
    # Map names to objects for easier reference
    wizard_map = {wizard.name: wizard for wizard in wizards}
    teacher_map = {teacher.name: teacher for teacher in teachers}
    
    # Add house points
    house_points = [
        # Gryffindor points
        HousePoints(house=House.GRYFFINDOR, points=50, reason="Saving the Philosophers Stone", 
                   teacher=teacher_map["Albus Dumbledore"], wizard=wizard_map["Harry Potter"]),
        HousePoints(house=House.GRYFFINDOR, points=10, reason="Answering correctly in Transfiguration class", 
                   teacher=teacher_map["Minerva McGonagall"], wizard=wizard_map["Hermione Granger"]),
        HousePoints(house=House.GRYFFINDOR, points=5, reason="Bravery in Herbology class", 
                   teacher=teacher_map["Pomona Sprout"], wizard=wizard_map["Neville Longbottom"]),
        HousePoints(house=House.GRYFFINDOR, points=-10, reason="Out after curfew", 
                   teacher=teacher_map["Severus Snape"], wizard=wizard_map["Ron Weasley"]),
        HousePoints(house=House.GRYFFINDOR, points=20, reason="Excellence in Charms", 
                   teacher=teacher_map["Filius Flitwick"], wizard=wizard_map["Hermione Granger"]),
                   
        # Slytherin points
        HousePoints(house=House.SLYTHERIN, points=15, reason="Perfect potion brewing", 
                   teacher=teacher_map["Severus Snape"], wizard=wizard_map["Draco Malfoy"]),
        HousePoints(house=House.SLYTHERIN, points=10, reason="Helping in classroom setup", 
                   teacher=teacher_map["Severus Snape"], wizard=wizard_map["Pansy Parkinson"]),
        HousePoints(house=House.SLYTHERIN, points=5, reason="Correct answer in Potions", 
                   teacher=teacher_map["Horace Slughorn"], wizard=wizard_map["Blaise Zabini"]),
        HousePoints(house=House.SLYTHERIN, points=-5, reason="Disruptive behavior", 
                   teacher=teacher_map["Minerva McGonagall"], wizard=wizard_map["Gregory Goyle"]),
        HousePoints(house=House.SLYTHERIN, points=20, reason="Prefect duties", 
                   teacher=teacher_map["Severus Snape"], wizard=wizard_map["Draco Malfoy"]),
                   
        # Ravenclaw points
        HousePoints(house=House.RAVENCLAW, points=25, reason="Outstanding Charms essay", 
                   teacher=teacher_map["Filius Flitwick"], wizard=wizard_map["Luna Lovegood"]),
        HousePoints(house=House.RAVENCLAW, points=15, reason="Creative spell application", 
                   teacher=teacher_map["Filius Flitwick"], wizard=wizard_map["Cho Chang"]),
        HousePoints(house=House.RAVENCLAW, points=10, reason="Excellence in Transfiguration", 
                   teacher=teacher_map["Minerva McGonagall"], wizard=wizard_map["Padma Patil"]),
        HousePoints(house=House.RAVENCLAW, points=-5, reason="Late to class", 
                   teacher=teacher_map["Severus Snape"], wizard=wizard_map["Terry Boot"]),
        HousePoints(house=House.RAVENCLAW, points=20, reason="Helping younger students", 
                   teacher=teacher_map["Filius Flitwick"], wizard=wizard_map["Michael Corner"]),
                   
        # Hufflepuff points
        HousePoints(house=House.HUFFLEPUFF, points=30, reason="Exceptional teamwork", 
                   teacher=teacher_map["Pomona Sprout"], wizard=wizard_map["Cedric Diggory"]),
        HousePoints(house=House.HUFFLEPUFF, points=15, reason="Helping in the greenhouses", 
                   teacher=teacher_map["Pomona Sprout"], wizard=wizard_map["Hannah Abbott"]),
        HousePoints(house=House.HUFFLEPUFF, points=10, reason="Kindness to first years", 
                   teacher=teacher_map["Albus Dumbledore"], wizard=wizard_map["Susan Bones"]),
        HousePoints(house=House.HUFFLEPUFF, points=5, reason="Good participation in class", 
                   teacher=teacher_map["Rubeus Hagrid"], wizard=wizard_map["Justin Finch-Fletchley"]),
        HousePoints(house=House.HUFFLEPUFF, points=-5, reason="Forgotten homework", 
                   teacher=teacher_map["Severus Snape"], wizard=wizard_map["Ernie Macmillan"]),
                   
        # House-wide points (with no specific student)
        HousePoints(house=House.GRYFFINDOR, points=100, reason="Winning the Quidditch match", 
                   teacher=teacher_map["Minerva McGonagall"]),
        HousePoints(house=House.SLYTHERIN, points=50, reason="Best decorated common room", 
                   teacher=teacher_map["Severus Snape"]),
        HousePoints(house=House.RAVENCLAW, points=75, reason="Highest average in examinations", 
                   teacher=teacher_map["Filius Flitwick"]),
        HousePoints(house=House.HUFFLEPUFF, points=60, reason="Community service project", 
                   teacher=teacher_map["Pomona Sprout"]),
    ]
    db.add_all(house_points)
    db.commit()
    logger.info(f"Added {len(house_points)} house point transactions")
    
    logger.info("Database initialization complete!")

def init_db():
    """Create tables and initialize with test data."""
    Base.metadata.create_all(bind=engine)
    
    # Get a DB session
    db = next(get_db())
    try:
        init_test_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    # Can be run directly with: python -m app.database.init_db
    logging.basicConfig(level=logging.INFO)
    init_db()
    logger.info("Database initialized successfully!") 