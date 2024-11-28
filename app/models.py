from sqlalchemy import Column, Integer, String, Date ,Text ,Time, Float ,ForeignKey,PrimaryKeyConstraint
from app.extensions import db

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50))
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(255))  # Store hashed passwords
#     access = db.Column(db.String(50))  # Access level

class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.String(50), nullable=True)
    account_number = db.Column(db.String(20), nullable=True)
    security_clearance = db.Column(db.String(50), nullable=True)
    highest_qualification = db.Column(db.String(50), nullable=True)
    designation = db.Column(db.String(50), nullable=True)
    authority = db.Column(db.String(20), nullable=False)
    identification = db.Column(db.String(50), nullable=True)
    department = db.Column(db.String(50), nullable=True)


class Investigator(db.Model):
    __tablename__ = 'investigator'

    investigator_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = Column(Date, nullable=False)  # Date of birth
    designation = Column(String(50), nullable=False)
    department = Column(String(100), nullable=False)
    identification = Column(String(50), nullable=False, unique=True)  # Could be Aadhar or another ID
    investigator_name = Column(String(100), nullable=False)
    phone_no = Column(String(15), nullable=False)
    address = Column(String, nullable=False)
    experience = Column(String(100), nullable=False)
    account_number = Column(String, nullable=False)
    security_clearance = db.Column(db.String(50), nullable=True)
    authority = db.Column(db.String(20), nullable=False)
    highest_qualification = Column(String(100), nullable=False)
    # foreign key definition
    # implementin_agency_id = Column(Integer, db.ForeignKey('agency.id'), nullable=False)
    # # You can also define a relationship to the "agency" table if needed
    # implementin_agency = db.relationship('Agency', backref='investigators')
    # def __repr__(self):
    #     return f'<Investigator {self.investigator_name}>'

class SubInvestigator(db.Model):
    __tablename__ = 'sub_investigator'

    sub_investigator_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    # username = db.Column(db.String(50), unique=True, nullable=False)
    # password = db.Column(db.String(255), nullable=False)
    dob = Column(Date, nullable=False)  # Date of birth
    designation = Column(String(50), nullable=False)
    department = Column(String(100), nullable=False)
    identification = Column(String(50), nullable=False, unique=True)  # Could be Aadhar or another ID
    sub_investigator_name = Column(String(100), nullable=False)
    phone_no = Column(String(15), nullable=False)
    address = Column(String(120), nullable=False)
    experience = Column(String(100), nullable=False)
    # account_number = Column(String, nullable=False)
    # security_clearance = db.Column(db.String(50), nullable=True)
    # authority = db.Column(db.String(20), nullable=False)
    highest_qualification = Column(String(100), nullable=False)

class Agency(db.Model):
    __tablename__ = 'agency'

    agency_id = Column(Integer, primary_key=True, autoincrement=True)
    agency_name = Column(String(100), nullable=False, unique=True)
    phone_no = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    agency_professionals = Column(String(255), nullable=False)  # Description of professionals in the agency
    ceo = Column(String(100), nullable=False)  # CEO name
    address = Column(String, nullable=False)  # Agency address
    established_date = Column(Date, nullable=False)  # Date when the agency was established

class SubAgency(db.Model):
    __tablename__ = 'sub_agency'

    sub_agency_id = Column(Integer, primary_key=True, autoincrement=True)
    sub_agency_name = Column(String(100), nullable=False, unique=True)
    phone_no = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    sub_agency_professionals = Column(String(255), nullable=False)  # Description of professionals in the sub-agency
    head_of_agency = Column(String(100), nullable=False)  # Head of the sub-agency
    address = Column(String, nullable=False)  # Sub-agency address
    established_date = Column(Date, nullable=False)  # Date when the sub-agency was established

class ProjectStatus(db.Model):
    __tablename__ = 'project_status'

    project_status_id = Column(Integer, primary_key=True, autoincrement=True)
    phase = Column(String(100), nullable=False)  # Name of the current project phase
    description = Column(Text, nullable=True)  # Detailed description of the project status
    date_of_updation = Column(Date, nullable=False)  # Date when the status was last updated
    time_of_updation = Column(Time, nullable=False)

class ProjectCoordinator(db.Model):
    _tablename_ = 'project_coordinator'
    
    project_coordinator_id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    project_coordinator_name = Column(String(255), nullable=False)  # Coordinator Name
    phone_number = Column(String(15), nullable=False)  # Phone Number
    address = Column(Text, nullable=False)  # Address
    experience = Column(Integer, nullable=False)  # Experience (in years)
    bank_details = Column(String(255), nullable=False)  # Bank Detailsaa
    security_clearance = Column(String(50))  # Security Clearance
    highest_qualification = Column(String(100))  # Highest Qualification
    email = Column(String(255), unique=True, nullable=False)  # Email
    dob = Column(Date, nullable=False)  # Date of Birth
    designation = Column(String(100), nullable=False)  # Designation
    department = Column(String(100), nullable=False)  # Department
    identification = Column(String(100), nullable=False)  # Identification (ID proof)
    branch = Column(String(100), nullable=False)# Branch

# class FundUtilization(db.Model):
#     _tablename_ = 'fund_utilization'

#     utilization_id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
#     quarter = Column(String(20), nullable=False)  # Quarter (e.g., Q1, Q2)
#     agency_name = Column(String(255), nullable=False)  # Agency Name
#     budget_head = Column(String(100), nullable=False)  # Budget Head
#     submission_date = Column(Date, nullable=False)  # Submission Date
#     utilized_amount = Column(Float, nullable=False)  # Utilized Amount
class ProjectFund(db.Model):
    _tablename_ = 'project_fund'

    project_fund_id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    fund_amount = Column(Float, nullable=False)  # Fund Amount
    fund_releasing_authority = Column(String(255), nullable=False)  # Fund Releasing Authority
    project_phase = Column(String(100), nullable=False)  # Project Phase
    fund_release_date = Column(Date, nullable=False)  # Fund Release Date

class ProjectTable(db.Model):
    _tablename_ = 'project_table'

    project_id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    project_name = Column(String(255), nullable=False)  # Project Name
    approval_date = Column(Date, nullable=False)  # Approval Date
    investigator_id = Column(Integer, ForeignKey('investigator.investigator_id'), nullable=False)  # FK from Investigator
    project_fund_id = Column(Integer, ForeignKey('project_fund.project_fund_id'), nullable=False)  # FK from ProjectFund
    # sub_implementing_id = Column(Integer, ForeignKey('sub_agency.sub_implementing_id'), nullable=False)  # FK from SubAgency
    project_status_id = Column(Integer, ForeignKey('project_status.project_status_id'), nullable=False)  # FK from ProjectStatus
    sub_agency_id = Column(Integer, ForeignKey('sub_agency.sub_agency_id'), nullable=False)  # FK from SubAgency
    agency_id = Column(Integer, ForeignKey('agency.agency_id'), nullable=False)  # FK from Agency
    sub_investigator_id = Column(Integer, ForeignKey('sub_investigator.sub_investigator_id'), nullable=False)  # FK from SubInvestigator
    project_type = Column(String(100), nullable=False)  # Project Type
    project_start_date = Column(Date, nullable=False)  # Start Date
    project_end_date = Column(Date, nullable=False)  # End Date
    project_coordinator_id = Column(Integer, ForeignKey('project_coordinator.project_coordinator_id'), nullable=False)  # FK from ProjectCoordinator
    project_description = Column(Text, nullable=True)  # Project Description
    
class FundUtilization(db.Model):
    __tablename__ = 'fund_utilization'

    utilization_id = Column(Integer, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)
    submission_date = Column(Date, nullable=False)
    utilized_amount = Column(Float, nullable=False)
    quarter = Column(String(10), nullable=False)
    agency_name = Column(String(100), nullable=False)
    budget_head = Column(String(100), nullable=False)

    # Define composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('utilization_id', 'project_id'),
    )
