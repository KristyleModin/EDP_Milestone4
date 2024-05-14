from . import db
from sqlalchemy.orm import relationship

class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_num = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    middlename = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    address_line = db.Column(db.String(50))
    brgy = db.Column(db.String(20))
    province = db.Column(db.String(20))
    country = db.Column(db.String(20))
    zipcode = db.Column(db.String(20))
    
    # Add department_id foreign key
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))

    # Define relationship with Department
    department = relationship("Department", back_populates="employees")
    assign_designation = relationship("AssignDesignation", back_populates="employee")
    leaves = relationship("Leaves", back_populates="employee", cascade="all, delete-orphan")

    # Define one-to-one relationship with Signatories
    signatory = relationship("Signatories", uselist=False, back_populates="employee")

    

class AssignDesignation(db.Model):
    __tablename__ = 'assign_designation'
    assign_designation_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    designation_id = db.Column(db.Integer, db.ForeignKey('designation.designation_id'))
    employee_type = db.Column(db.String)
    status = db.Column(db.String)  # Ensure status field is defined correctly

    # Define relationship with Employee
    employee = relationship("Employee", back_populates="assign_designation")
    # Define relationship with Designation
    designation = relationship("Designation", back_populates="assign_designation")

class Designation(db.Model):
    __tablename__ = 'designation'
    designation_id = db.Column(db.Integer, primary_key=True)
    designation_name = db.Column(db.String)
 
    # Define relationship with AssignDesignation
    assign_designation = relationship("AssignDesignation", back_populates="designation")

class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String)

    # Define one-to-many relationship with Employee
    employees = relationship("Employee", back_populates="department")

class Signatories(db.Model):
    __tablename__ = 'signatories'
    signatories_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    highersuperior = db.Column(db.String)
    status = db.Column(db.String)
    
    # Define relationship with Employee
    employee = relationship("Employee", back_populates="signatory")


class Leaves(db.Model):
    __tablename__ = 'leaves'
    leaves_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id', ondelete="CASCADE"), nullable=False)
    start_leave = db.Column(db.Date)  # Add start_leave date field
    end_leave = db.Column(db.Date)    # Add end_leave date field
    leave_type = db.Column(db.String)
    status = db.Column(db.String)

    employee = relationship("Employee", back_populates="leaves")


    
