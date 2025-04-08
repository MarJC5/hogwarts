import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.models import Wizard, House, Teacher, HousePoints
from app.database.db import get_db
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from enum import Enum

@strawberry.enum
class HouseEnum(Enum):
    """GraphQL enum for Hogwarts houses, maps to House model enum"""
    GRYFFINDOR = "Gryffindor"
    HUFFLEPUFF = "Hufflepuff"
    RAVENCLAW = "Ravenclaw"
    SLYTHERIN = "Slytherin"

@strawberry.enum
class GroupByEnum(Enum):
    """Enum for grouping history data in different ways"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    TEACHER = "teacher"
    HOUSE = "house"

@strawberry.type
class WizardType:
    """GraphQL type that represents a wizard, maps to Wizard model"""
    id: int
    name: str
    house: HouseEnum
    wand: str
    patronus: Optional[str] = None

@strawberry.input
class WizardInput:
    """Input type for creating a new wizard"""
    name: str
    house: HouseEnum
    wand: str
    patronus: Optional[str] = None

@strawberry.type
class TeacherType:
    """GraphQL type that represents a teacher, maps to Teacher model"""
    id: int
    name: str
    subject: str
    house: Optional[HouseEnum] = None
    
@strawberry.input
class TeacherInput:
    """Input type for creating a new teacher"""
    name: str
    subject: str
    house: Optional[HouseEnum] = None

@strawberry.type
class HousePointsType:
    """GraphQL type for house points, maps to HousePoints model"""
    id: int
    house: HouseEnum
    points: int
    reason: Optional[str] = None
    timestamp: datetime
    teacher: TeacherType
    is_deduction: bool

@strawberry.input
class HousePointsInput:
    """Input type for awarding or deducting house points"""
    house: HouseEnum
    points: int  # Can be positive (award) or negative (deduct)
    reason: Optional[str] = None
    teacher_id: int

@strawberry.type
class PointHistoryEntry:
    """GraphQL type for a single entry in the points history"""
    timestamp: datetime
    house: HouseEnum
    points: int
    cumulative_points: int
    is_deduction: bool
    reason: Optional[str] = None
    teacher: TeacherType

@strawberry.type
class PointHistoryGroupedEntry:
    """GraphQL type for grouped history data, used for analytics"""
    group_key: str  # Could be a date string, teacher name, house name, etc.
    total_points: int
    awards_count: int
    deductions_count: int

# ====== WIZARD DATABASE OPERATIONS ======

def get_all_wizards(db: Session) -> List[Wizard]:
    """
    Retrieves all wizards from the database.
    
    Args:
        db: SQLAlchemy database session
        
    Returns:
        List of Wizard database models
    """
    return db.query(Wizard).all()

def get_wizard_by_id(id: int, db: Session) -> Optional[Wizard]:
    """
    Retrieves a specific wizard by ID.
    
    Args:
        id: The ID of the wizard to find
        db: SQLAlchemy database session
        
    Returns:
        Wizard model if found, None otherwise
    """
    return db.query(Wizard).filter(Wizard.id == id).first()

def create_wizard(wizard_data: WizardInput, db: Session) -> Wizard:
    """
    Creates a new wizard in the database.
    
    Args:
        wizard_data: Input data with wizard details
        db: SQLAlchemy database session
        
    Returns:
        The newly created Wizard model instance
    """
    db_wizard = Wizard(
        name=wizard_data.name,
        house=wizard_data.house.value,
        wand=wizard_data.wand,
        patronus=wizard_data.patronus
    )
    db.add(db_wizard)
    db.commit()
    db.refresh(db_wizard)
    return db_wizard

# ====== TEACHER DATABASE OPERATIONS ======

def get_all_teachers(db: Session) -> List[Teacher]:
    """
    Retrieves all teachers from the database.
    
    Args:
        db: SQLAlchemy database session
        
    Returns:
        List of Teacher database models
    """
    return db.query(Teacher).all()

def get_teacher_by_id(id: int, db: Session) -> Optional[Teacher]:
    """
    Retrieves a specific teacher by ID.
    
    Args:
        id: The ID of the teacher to find
        db: SQLAlchemy database session
        
    Returns:
        Teacher model if found, None otherwise
    """
    return db.query(Teacher).filter(Teacher.id == id).first()

def create_teacher(teacher_data: TeacherInput, db: Session) -> Teacher:
    """
    Creates a new teacher in the database.
    
    Args:
        teacher_data: Input data with teacher details
        db: SQLAlchemy database session
        
    Returns:
        The newly created Teacher model instance
    """
    db_teacher = Teacher(
        name=teacher_data.name,
        subject=teacher_data.subject,
        house=teacher_data.house.value if teacher_data.house else None
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# ====== HOUSE POINTS DATABASE OPERATIONS ======

def get_all_house_points(db: Session) -> List[HousePoints]:
    """
    Retrieves all house points records from the database.
    
    Args:
        db: SQLAlchemy database session
        
    Returns:
        List of HousePoints database models
    """
    return db.query(HousePoints).all()

def get_house_points_by_house(house: House, db: Session) -> List[HousePoints]:
    """
    Retrieves house points for a specific house.
    
    Args:
        house: The house to filter by
        db: SQLAlchemy database session
        
    Returns:
        List of HousePoints database models for the specified house
    """
    return db.query(HousePoints).filter(HousePoints.house == house).all()

def get_house_points_sum(house: House, db: Session) -> int:
    """
    Calculates the total points for a specific house.
    
    Args:
        house: The house to calculate points for
        db: SQLAlchemy database session
        
    Returns:
        Integer representing total points (can be negative)
    """
    result = db.query(
        HousePoints.house, 
        func.sum(HousePoints.points).label('total')
    ).filter(HousePoints.house == house).group_by(HousePoints.house).first()
    
    return result.total if result else 0

def modify_house_points(points_data: HousePointsInput, db: Session) -> HousePoints:
    """
    Adds a new house points record (positive for awards, negative for deductions).
    
    Args:
        points_data: Input data with points details
        db: SQLAlchemy database session
        
    Returns:
        The newly created HousePoints model instance
    """
    # Store the points value as is (positive for award, negative for deduction)
    db_points = HousePoints(
        house=points_data.house.value,
        points=points_data.points,
        reason=points_data.reason,
        teacher_id=points_data.teacher_id
    )
    db.add(db_points)
    db.commit()
    db.refresh(db_points)
    return db_points

# ====== POINT HISTORY OPERATIONS ======

def get_points_history(
    db: Session, 
    house: Optional[House] = None,
    teacher_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 50
) -> List[HousePoints]:
    """
    Retrieves house points history with optional filtering.
    
    Args:
        db: SQLAlchemy database session
        house: Optional house to filter by
        teacher_id: Optional teacher ID to filter by
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering
        limit: Maximum number of records to return
        
    Returns:
        List of HousePoints database models matching the filters
    """
    query = db.query(HousePoints)
    
    if house:
        query = query.filter(HousePoints.house == house)
    
    if teacher_id:
        query = query.filter(HousePoints.teacher_id == teacher_id)
    
    if start_date:
        query = query.filter(HousePoints.timestamp >= start_date)
    
    if end_date:
        query = query.filter(HousePoints.timestamp <= end_date)
    
    return query.order_by(desc(HousePoints.timestamp)).limit(limit).all()

def calculate_cumulative_points(
    db: Session,
    house: House,
    up_to_timestamp: datetime
) -> int:
    """
    Calculates the total points for a house up to a specific point in time.
    
    Args:
        db: SQLAlchemy database session
        house: The house to calculate points for
        up_to_timestamp: Datetime up to which to calculate points
        
    Returns:
        Integer representing cumulative points
    """
    result = db.query(
        func.sum(HousePoints.points).label('total')
    ).filter(
        HousePoints.house == house,
        HousePoints.timestamp <= up_to_timestamp
    ).first()
    
    return result.total if result and result.total else 0

def get_points_grouped(
    db: Session,
    group_by: str,
    house: Optional[House] = None,
    teacher_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[dict]:
    """
    Groups house points by various criteria for analytics.
    
    Args:
        db: SQLAlchemy database session
        group_by: Criteria to group by (day, week, month, teacher, house)
        house: Optional house to filter by
        teacher_id: Optional teacher ID to filter by
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering
        
    Returns:
        List of dictionaries with grouped data
    """
    
    if group_by == "day":
        # PostgreSQL date_trunc for grouping by day
        group_expr = func.date_trunc('day', HousePoints.timestamp).label('group_key')
    elif group_by == "week":
        group_expr = func.date_trunc('week', HousePoints.timestamp).label('group_key')
    elif group_by == "month":
        group_expr = func.date_trunc('month', HousePoints.timestamp).label('group_key')
    elif group_by == "teacher":
        group_expr = Teacher.name.label('group_key')
    elif group_by == "house":
        group_expr = HousePoints.house.label('group_key')
    else:
        raise ValueError(f"Invalid group_by parameter: {group_by}")
    
    query = db.query(
        group_expr,
        func.sum(HousePoints.points).label('total_points'),
        func.count(func.case([(HousePoints.points > 0, 1)])).label('awards_count'),
        func.count(func.case([(HousePoints.points < 0, 1)])).label('deductions_count')
    ).join(Teacher, HousePoints.teacher_id == Teacher.id)
    
    if house:
        query = query.filter(HousePoints.house == house)
    
    if teacher_id:
        query = query.filter(HousePoints.teacher_id == teacher_id)
    
    if start_date:
        query = query.filter(HousePoints.timestamp >= start_date)
    
    if end_date:
        query = query.filter(HousePoints.timestamp <= end_date)
    
    return query.group_by(group_expr).all()

@strawberry.type
class HouseTotalType:
    """GraphQL type for house total points, used for house cup standings"""
    house: HouseEnum
    total_points: int

@strawberry.type
class Query:
    """
    GraphQL Query type that defines all available queries.
    Each field resolver handles a specific type of query.
    """
    
    @strawberry.field
    def wizards(self, info) -> List[WizardType]:
        """
        GraphQL resolver that returns all wizards.
        
        Args:
            info: GraphQL resolver info (context, etc.)
            
        Returns:
            List of WizardType objects
        """
        db = next(get_db())
        wizards = get_all_wizards(db)
        return [
            WizardType(
                id=w.id,
                name=w.name,
                house=HouseEnum(w.house),
                wand=w.wand,
                patronus=w.patronus
            )
            for w in wizards
        ]
    
    @strawberry.field
    def wizard(self, info, id: int) -> Optional[WizardType]:
        """
        GraphQL resolver that returns a specific wizard by ID.
        
        Args:
            info: GraphQL resolver info
            id: ID of the wizard to retrieve
            
        Returns:
            WizardType if found, None otherwise
        """
        db = next(get_db())
        wizard = get_wizard_by_id(id, db)
        if wizard:
            return WizardType(
                id=wizard.id,
                name=wizard.name,
                house=HouseEnum(wizard.house),
                wand=wizard.wand,
                patronus=wizard.patronus
            )
        return None
    
    @strawberry.field
    def teachers(self, info) -> List[TeacherType]:
        """
        GraphQL resolver that returns all teachers.
        
        Args:
            info: GraphQL resolver info
            
        Returns:
            List of TeacherType objects
        """
        db = next(get_db())
        teachers = get_all_teachers(db)
        return [
            TeacherType(
                id=t.id,
                name=t.name,
                subject=t.subject,
                house=HouseEnum(t.house) if t.house else None
            )
            for t in teachers
        ]
    
    @strawberry.field
    def teacher(self, info, id: int) -> Optional[TeacherType]:
        """
        GraphQL resolver that returns a specific teacher by ID.
        
        Args:
            info: GraphQL resolver info
            id: ID of the teacher to retrieve
            
        Returns:
            TeacherType if found, None otherwise
        """
        db = next(get_db())
        teacher = get_teacher_by_id(id, db)
        if teacher:
            return TeacherType(
                id=teacher.id,
                name=teacher.name,
                subject=teacher.subject,
                house=HouseEnum(teacher.house) if teacher.house else None
            )
        return None
    
    @strawberry.field
    def house_points(self, info, house: Optional[HouseEnum] = None) -> List[HousePointsType]:
        """
        GraphQL resolver that returns house points records, optionally filtered by house.
        
        Args:
            info: GraphQL resolver info
            house: Optional house to filter by
            
        Returns:
            List of HousePointsType objects
        """
        db = next(get_db())
        if house:
            points = get_house_points_by_house(house.value, db)
        else:
            points = get_all_house_points(db)
            
        return [
            HousePointsType(
                id=p.id,
                house=HouseEnum(p.house),
                points=abs(p.points),  # Always return absolute value
                reason=p.reason,
                timestamp=p.timestamp,
                is_deduction=p.points < 0,  # Determine if this was a deduction
                teacher=TeacherType(
                    id=p.teacher.id,
                    name=p.teacher.name,
                    subject=p.teacher.subject,
                    house=HouseEnum(p.teacher.house) if p.teacher.house else None
                )
            )
            for p in points
        ]
    
    @strawberry.field
    def house_totals(self, info) -> List[HouseTotalType]:
        """
        GraphQL resolver that returns total points for all houses (house cup standings).
        
        Args:
            info: GraphQL resolver info
            
        Returns:
            List of HouseTotalType objects with current standings
        """
        db = next(get_db())
        houses = [h.value for h in House]
        return [
            HouseTotalType(
                house=HouseEnum(house),
                total_points=get_house_points_sum(house, db)
            )
            for house in houses
        ]
    
    @strawberry.field
    def points_history(
        self, 
        info, 
        house: Optional[HouseEnum] = None,
        teacher_id: Optional[int] = None,
        days_ago: Optional[int] = None,
        limit: int = 50
    ) -> List[PointHistoryEntry]:
        """
        GraphQL resolver that returns detailed points history with filtering options.
        
        Args:
            info: GraphQL resolver info
            house: Optional house to filter by
            teacher_id: Optional teacher ID to filter by
            days_ago: Optional number of days to look back
            limit: Maximum number of records to return
            
        Returns:
            List of PointHistoryEntry objects
        """
        db = next(get_db())
        
        # Calculate start date if days_ago is provided
        start_date = None
        if days_ago:
            start_date = datetime.utcnow() - timedelta(days=days_ago)
        
        points = get_points_history(
            db, 
            house=house.value if house else None,
            teacher_id=teacher_id,
            start_date=start_date,
            limit=limit
        )
        
        result = []
        for p in points:
            # Calculate cumulative points up to this point for the house
            cumulative = calculate_cumulative_points(db, p.house, p.timestamp)
            
            result.append(PointHistoryEntry(
                timestamp=p.timestamp,
                house=HouseEnum(p.house),
                points=abs(p.points),
                cumulative_points=cumulative,
                is_deduction=p.points < 0,
                reason=p.reason,
                teacher=TeacherType(
                    id=p.teacher.id,
                    name=p.teacher.name,
                    subject=p.teacher.subject,
                    house=HouseEnum(p.teacher.house) if p.teacher.house else None
                )
            ))
        
        return result
    
    @strawberry.field
    def points_history_grouped(
        self,
        info,
        group_by: GroupByEnum,
        house: Optional[HouseEnum] = None,
        teacher_id: Optional[int] = None,
        days_ago: Optional[int] = None
    ) -> List[PointHistoryGroupedEntry]:
        """
        GraphQL resolver that returns aggregated points history for analytics.
        
        Args:
            info: GraphQL resolver info
            group_by: Criteria to group results by (day, week, month, teacher, house)
            house: Optional house to filter by
            teacher_id: Optional teacher ID to filter by
            days_ago: Optional number of days to look back
            
        Returns:
            List of PointHistoryGroupedEntry objects with analytics data
        """
        db = next(get_db())
        
        # Calculate start date if days_ago is provided
        start_date = None
        if days_ago:
            start_date = datetime.utcnow() - timedelta(days=days_ago)
        
        groups = get_points_grouped(
            db,
            group_by=group_by.value,
            house=house.value if house else None,
            teacher_id=teacher_id,
            start_date=start_date
        )
        
        result = []
        for g in groups:
            # Convert date objects to strings for consistent return type
            group_key = g.group_key
            if group_by.value in ["day", "week", "month"]:
                group_key = g.group_key.strftime("%Y-%m-%d")
            
            result.append(PointHistoryGroupedEntry(
                group_key=str(group_key),
                total_points=g.total_points,
                awards_count=g.awards_count,
                deductions_count=g.deductions_count
            ))
        
        return result

@strawberry.type
class Mutation:
    """
    GraphQL Mutation type that defines all available mutations.
    Each field resolver handles a specific type of data modification.
    """
    
    @strawberry.mutation
    def create_wizard(self, info, wizard_data: WizardInput) -> WizardType:
        """
        GraphQL mutation that creates a new wizard.
        
        Args:
            info: GraphQL resolver info
            wizard_data: Input data for creating the wizard
            
        Returns:
            The newly created WizardType
        """
        db = next(get_db())
        wizard = create_wizard(wizard_data, db)
        return WizardType(
            id=wizard.id,
            name=wizard.name,
            house=HouseEnum(wizard.house),
            wand=wizard.wand,
            patronus=wizard.patronus
        )
    
    @strawberry.mutation
    def create_teacher(self, info, teacher_data: TeacherInput) -> TeacherType:
        """
        GraphQL mutation that creates a new teacher.
        
        Args:
            info: GraphQL resolver info
            teacher_data: Input data for creating the teacher
            
        Returns:
            The newly created TeacherType
        """
        db = next(get_db())
        teacher = create_teacher(teacher_data, db)
        return TeacherType(
            id=teacher.id,
            name=teacher.name,
            subject=teacher.subject,
            house=HouseEnum(teacher.house) if teacher.house else None
        )
    
    @strawberry.mutation
    def award_house_points(self, info, points_data: HousePointsInput) -> HousePointsType:
        """
        GraphQL mutation that awards points to a house.
        
        Args:
            info: GraphQL resolver info
            points_data: Input data with points details
            
        Returns:
            The newly created HousePointsType
        """
        if points_data.points <= 0:
            raise ValueError("Points must be positive when awarding")
            
        db = next(get_db())
        points = modify_house_points(points_data, db)
        teacher = get_teacher_by_id(points.teacher_id, db)
        
        return HousePointsType(
            id=points.id,
            house=HouseEnum(points.house),
            points=points.points,
            reason=points.reason,
            timestamp=points.timestamp,
            is_deduction=False,
            teacher=TeacherType(
                id=teacher.id,
                name=teacher.name,
                subject=teacher.subject,
                house=HouseEnum(teacher.house) if teacher.house else None
            )
        )
    
    @strawberry.mutation
    def deduct_house_points(self, info, points_data: HousePointsInput) -> HousePointsType:
        """
        GraphQL mutation that deducts points from a house.
        
        Args:
            info: GraphQL resolver info
            points_data: Input data with points details
            
        Returns:
            The newly created HousePointsType (with negative points value)
        """
        if points_data.points <= 0:
            raise ValueError("Points must be positive when deducting")
            
        # Convert to negative for deduction
        points_data.points = -points_data.points
            
        db = next(get_db())
        points = modify_house_points(points_data, db)
        teacher = get_teacher_by_id(points.teacher_id, db)
        
        return HousePointsType(
            id=points.id,
            house=HouseEnum(points.house),
            points=abs(points.points),  # Return absolute value
            reason=points.reason,
            timestamp=points.timestamp,
            is_deduction=True,
            teacher=TeacherType(
                id=teacher.id,
                name=teacher.name,
                subject=teacher.subject,
                house=HouseEnum(teacher.house) if teacher.house else None
            )
        )

# Create the GraphQL schema with the Query and Mutation types
schema = strawberry.Schema(query=Query, mutation=Mutation) 