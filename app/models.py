from sqlalchemy import Column, Integer, String, Date ,Text ,Time, Float ,ForeignKey,PrimaryKeyConstraint, event
from app.extensions import db
from sqlalchemy.orm import validates

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50))
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(255))  # Store hashed passwords
#     access = db.Column(db.String(50))  # Access level

class Admin(db.Model):
    __tablename__ = 'admin'
    
    admin_id = Column(Integer, primary_key=True)
    adminUniqe_id = Column(String(50), unique=True)
    admin_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_no = Column(String(15), nullable=False)
    dob = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    experience = Column(String(50), nullable=True)
    account_number = Column(String(20), nullable=True)
    security_clearance = Column(String(50), nullable=True)
    highest_qualification = Column(String(50), nullable=True)
    designation = Column(String(50), nullable=True)
    authority = Column(String(20), nullable=False)
    identification = Column(String(50), nullable=True)
    department = Column(String(50), nullable=True)

    @validates('adminUniqe_id')
    def generate_adminUnique_id(self, key, value):
        # Do not set adminUniqe_id directly through this validator.
        return value
# Listen for the "before insert" event to generate adminUniqe_id dynamically
@event.listens_for(Admin, 'before_insert')
def generate_adminUnique_id(mapper, connection, target):
    if not target.adminUniqe_id:  # If the adminUnique_id is not already set
        target.adminUniqe_id = f"admin_{target.admin_id}"


class Investigator(db.Model):
    __tablename__ = 'investigator'

    investigator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    investigatorUniqe_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    identification = db.Column(db.String(50), nullable=False, unique=True)
    investigator_name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String, nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String, nullable=False)
    security_clearance = db.Column(db.String(50), nullable=True)
    authority = db.Column(db.String(20), nullable=False)
    highest_qualification = db.Column(db.String(100), nullable=False)

    # This will generate the investigatorUniqe_id after insert
    @validates('investigatorUniqe_id')
    def generate_investigatorUniqe_id(self, key, value):
        # Leave this as it is to ensure the value is correctly set after insert
        return value
@event.listens_for(Investigator, 'after_insert')
def generate_investigatorUniqe_id(mapper, connection, target):
    # After the investigator record is inserted and we have an id, update investigatorUniqe_id
    if not target.investigatorUniqe_id:  # If investigatorUniqe_id is not set yet
        target.investigatorUniqe_id = f"investigator_{target.investigator_id}"
        db.session.merge(target)  # Use merge to update the row


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
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)  # FK from ProjectTable

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
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)  # FK from ProjectTable

class ProjectTable(db.Model):
    _tablename_ = 'project_table'

    project_id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    project_name = Column(String(255), nullable=False)  # Project Name
    approval_date = Column(Date)  # Approval Date
    investigator_id = Column(Integer, ForeignKey('investigator.investigator_id'), nullable=False)  # FK from Investigator
    # project_fund_id = Column(Integer, ForeignKey('project_fund.project_fund_id'), nullable=False)  # FK from ProjectFund
    # sub_implementing_id = Column(Integer, ForeignKey('sub_agency.sub_implementing_id'), nullable=False)  # FK from SubAgency
    # project_status_id = Column(Integer, ForeignKey('project_status.project_status_id'), nullable=False)  # FK from ProjectStatus
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

class Message(db.Model):
    __tablename__ = 'message'

    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(50), nullable=False)  # String to accommodate IDs like "admin_1"
    sender_type = db.Column(db.String(50), nullable=False)  # Specifies the sender type ("investigator" or "admin")
    receiver_id = db.Column(db.String(50), nullable=False)  # String to accommodate IDs like "investigator_9"
    receiver_type = db.Column(db.String(50), nullable=False)  # Specifies the receiver type ("investigator" or "admin")
    subject = db.Column(db.String(255), nullable=False)  # Message subject
    body = db.Column(db.Text, nullable=False)  # Message body
    attachment = db.Column(db.LargeBinary, nullable=True)  # Binary data for file attachments
    attachment_name = db.Column(db.String(255), nullable=True)  # Name of the attachment file
    attachment_mime_type = db.Column(db.String(100), nullable=True)  # MIME type of the file (e.g., "application/pdf")
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)


