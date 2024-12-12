from sqlalchemy import Column, Integer, String, Date ,Text ,Time, Float ,ForeignKey,PrimaryKeyConstraint, event
from app.extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String, Date ,Text ,Time, Float ,ForeignKey,PrimaryKeyConstraint, event,LargeBinary,DateTime  
from datetime import datetime  # For default value

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50))
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(255))  # Store hashed passwords
#     access = db.Column(db.String(50))  # Access level

from sqlalchemy import Boolean

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
    is_verified = Column(Boolean, default=False, nullable=False)  # New column

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

#     # This will generate the investigatorUniqe_id after insert
#     @validates('investigatorUniqe_id')
#     def generate_investigatorUniqe_id(self, key, value):
#         # Leave this as it is to ensure the value is correctly set after insert
#         return value
# @event.listens_for(Investigator, 'after_insert')
# def generate_investigatorUniqe_id(mapper, connection, target):
#     # After the investigator record is inserted and we have an id, update investigatorUniqe_id
#     if not target.investigatorUniqe_id:  # If investigatorUniqe_id is not set yet
#         target.investigatorUniqe_id = f"investigator_{target.investigator_id}"
#         db.session.merge(target)  # Use merge to update the row


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
    start_date = Column(Date, nullable=False)  # Start date of the project phase
    end_date = Column(Date, nullable=True)  # End date of the project phase
    project_completion_status = Column(String(50), nullable=False, default="In Progress")  # Completion status of the project
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

class Form(db.Model):
    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True)
    form_name = db.Column(db.String(255), nullable=False)  # To store the form name
    file_data = db.Column(db.LargeBinary, nullable=False)  # Store the PDF file in binary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # To track when the form was uploaded

    def __init__(self, form_name, file_data):
        self.form_name = form_name
        self.file_data = file_data

class ProjectReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(50), nullable=False)
    phase = db.Column(db.String(100), nullable=False)
    report_doc = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "phase": self.phase,
            "report_doc": self.report_doc,
            "created_at": self.created_at.isoformat()
        }
    
class FileStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "file_name": self.file_name,
            "file_url": self.file_url
        }

class BankDetails(db.Model):
    _tablename_ = 'bank_details'

    bank_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    investigator_id = db.Column(db.Integer, db.ForeignKey('investigator.investigator_id'), nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    account_holder_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    ifsc_code = db.Column(db.String(11), nullable=False)
    branch_name = db.Column(db.String(255), nullable=False)
    branch_address = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

# Expenditure Model
class Expenditure(db.Model):
    __tablename__ = 'expenditure'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_table.project_id'), nullable=False)

    land_building = db.Column(db.Float, nullable=False)
    equipment = db.Column(db.Float, nullable=False)
    totalCapital = db.Column(db.Float, nullable=False)
    
    salary = db.Column(db.Float, nullable=False)
    consumables = db.Column(db.Float, nullable=False)
    travel = db.Column(db.Float, nullable=False)
    workshopSeminar = db.Column(db.Float, nullable=False)
    totalRevenue = db.Column(db.Float, nullable=False)
    
    contingency = db.Column(db.Float, nullable=False)
    institutionalOverhead = db.Column(db.Float, nullable=False)
    applicableTaxes = db.Column(db.Float, nullable=False)
    grandTotal = db.Column(db.Float, nullable=False)

    implementingAgency = db.Column(db.Boolean, default=False)
    subImplementingAgency1 = db.Column(db.Boolean, default=False)
    subImplementingAgency2 = db.Column(db.Boolean, default=False)
    subImplementingAgency3 = db.Column(db.Boolean, default=False)


class FormIII(db.Model):
    _tablename_ = 'form_iii'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)
    quarter_end_date = Column(Date, nullable=False)
    land_building_cost = Column(Float, default=0.0)
    capital_equipment_cost = Column(Float, default=0.0)
    manpower_cost = Column(Float, default=0.0)
    consumable_cost = Column(Float, default=0.0)
    ta_da_cost = Column(Float, default=0.0)
    contingencies_cost = Column(Float, default=0.0)
    seminar_cost = Column(Float, default=0.0)
    other_costs = Column(Float, default=0.0)
    funds_advanced = Column(Float, default=0.0)
    expenditure_incurred = Column(Float, default=0.0)
    unspent_balance = Column(Float, default=0.0)


class FormVI(db.Model):
    _tablename_ = 'form_vi'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)
    title = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    approved_completion_date = Column(Date, nullable=False)
    actual_completion_date = Column(Date)
    objectives = Column(String)
    work_programme = Column(String)
    work_done_details = Column(String)
    objectives_fulfillment = Column(String)
    scope_for_further_studies = Column(String)
    conclusions = Column(String)
    recommendations = Column(String)
    industry_application_scope = Column(String)
    associated_persons = Column(String)
    final_expenditure_statement = Column(String)



class FormVII(db.Model):
    _tablename_ = 'form_vii'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)
    principal_agency = Column(String, nullable=False)
    project_leader = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    scheduled_completion_date = Column(Date, nullable=False)
    approved_objectives = Column(String)
    approved_work_programme = Column(String)
    work_done_details = Column(String)
    revised_schedule = Column(String)
    extension_time = Column(String)
    extension_reason = Column(String)
    total_project_cost = Column(Float, default=0.0)
    actual_expenditure = Column(Float, default=0.0)

class FormI(db.Model):
    _tablename_ = 'form_i'
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)  # Foreign key for project table
    
    # Basic Information
    project_title = Column(String(255), nullable=False)
    principal_agency_name = Column(String(255))
    principal_agency_address = Column(Text)
    project_leader = Column(String(255))
    sub_agency_name = Column(String(255))
    sub_agency_address = Column(Text)
    co_investigator = Column(String(255))
    
    # Details
    definition_of_issue = Column(Text)
    objectives = Column(Text)
    justification = Column(Text)
    benefit_to_coal_industry = Column(Text)
    work_plan = Column(Text)
    methodology = Column(Text)
    organization_of_work_elements = Column(Text)
    time_schedule = Column(Text)  # You can also implement a JSON field for bar chart data
    
    # Cost Breakdown
    land_building_cost = Column(Float, default=0.0)
    equipment_cost = Column(Float, default=0.0)
    salary_allowances = Column(Float, default=0.0)
    consumables_cost = Column(Float, default=0.0)
    travel_cost = Column(Float, default=0.0)
    workshop_cost = Column(Float, default=0.0)
    contingency_cost = Column(Float, default=0.0)
    overheads = Column(Float, default=0.0)
    taxes = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    foreign_exchange_component = Column(String(255))  # Foreign currency details
    exchange_rate = Column(Float, default=0.0)
    
    # Additional Fields
    fund_phasing = Column(Text)
    land_outlay = Column(Text)
    equipment_outlay = Column(Text)
    consumables_outlay = Column(Text)
    cv_details = Column(Text)  # Combine all CV-related details as JSON or structured text
    past_experience = Column(Text)
    others = Column(Text)
    
    
class FormII(db.Model):
    _tablename_ = 'form_ii'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_table.project_id'), nullable=False)
    project_code = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    year_or_period = db.Column(db.String(255), nullable=False)
    total_approved_cost = db.Column(db.Float, nullable=False)
    total_fund_received = db.Column(db.Float, nullable=False)
    interest_earned = db.Column(db.Float, default=0.0)
    expenditure_incurred = db.Column(db.Float, nullable=False)
    balance_fund_available = db.Column(db.Float, nullable=False)
    fund_provision = db.Column(db.Float, nullable=False)
    fund_required = db.Column(db.Float, nullable=False)
    land_building = db.Column(db.Float, default=0.0)
    capital_equipment = db.Column(db.Float, default=0.0)
    manpower = db.Column(db.Float, default=0.0)
    consumables = db.Column(db.Float, default=0.0)
    travel = db.Column(db.Float, default=0.0)
    contingencies = db.Column(db.Float, default=0.0)
    workshop_seminar = db.Column(db.Float, default=0.0)
    associate_finance_officer = db.Column(db.String(255), nullable=False)
    project_leader = db.Column(db.String(255), nullable=False)
    signature_finance_officer = db.Column(db.String(255), nullable=False)
    signature_project_leader = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self._table_.columns}
    
   
    
 # SQLAlchemy Model for Form IV
class FormIV(db.Model):
    _tablename_ = 'form_iv'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    project_code = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    quarter_ending = db.Column(db.String(50), nullable=False)
    equipment_name = db.Column(db.String(255), nullable=False)
    supplier_name = db.Column(db.String(255), nullable=False)
    no_of_units = db.Column(db.Integer, nullable=False)
    unit_value = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    total_approved_cost = db.Column(db.Float, nullable=False)
    progressive_expenditure = db.Column(db.Float, nullable=False)
    associate_finance_officer = db.Column(db.String(255), nullable=False)
    project_leader = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self._table_.columns}
    
    
# SQLAlchemy Model for Form V
class FormV(db.Model):
    _tablename_ = 'form_v'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    project_code = db.Column(db.String(50), nullable=False)
    progress_for_quarter = db.Column(db.String(255), nullable=False)
    principal_agency = db.Column(db.String(255), nullable=False)
    sub_agency = db.Column(db.String(255), nullable=True)
    project_leader = db.Column(db.String(255), nullable=False)
    date_of_commencement = db.Column(db.Date, nullable=False)
    approved_completion_date = db.Column(db.Date, nullable=False)
    bar_chart_status = db.Column(db.Text, nullable=True)
    work_done = db.Column(db.Text, nullable=True)
    slippage_reasons = db.Column(db.Text, nullable=True)
    corrective_actions = db.Column(db.Text, nullable=True)
    work_expected_next_quarter = db.Column(db.Text, nullable=True)
    quarterly_expenditure_statements = db.Column(db.Text, nullable=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self._table_.columns}
    

class FormVIII(db.Model):
    _tablename_ = 'form_viii'
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('project_table.project_id'), nullable=False)  # Foreign Key for Project Table
    
    # Project Details
    project_name = Column(String(255), nullable=False)
    project_code = Column(String(100), nullable=False)
    
    # Agency Details
    principal_agency_name = Column(String(255))
    sub_implementing_agency_name = Column(String(255))
    
    # Project Leader
    project_leader = Column(String(255))
    
    # Dates
    project_start_date = Column(Date)
    scheduled_completion_date = Column(Date)
    
    # Approved Objectives
    approved_objectives = Column(Text)
    
    # Approved Work Programme
    approved_work_programme = Column(Text)
    
    # Work Progress
    work_done_details = Column(Text)
    
    # Financial Information
    total_approved_cost = Column(Float)
    revised_cost = Column(Float)
    justification_for_revision = Column(Text)
    
    # Time Schedule
    revised_time_schedule = Column(Text)
    
    # Actual Expenditure (to be captured from Form III and IV)
    actual_expenditure_till_last_quarter = Column(Float)

    # Signature Details
    associate_finance_officer_signature = Column(String(255))
    project_leader_signature = Column(String(255))
    
    # Additional Fields
    comments = Column(Text)

# Helper method for serialization
def model_as_dict(self):
    return {column.name: getattr(self, column.name) for column in self._table_.columns}

FormVIII.as_dict = model_as_dict



