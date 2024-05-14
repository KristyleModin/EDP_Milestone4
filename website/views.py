from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Employee, Department, AssignDesignation, Designation, Signatories, Leaves
from flask import session
from datetime import datetime
from sqlalchemy.orm import joinedload
from flask import request, jsonify
from datetime import datetime
from flask import request
from flask import redirect, url_for, render_template
from datetime import date
from .models import Employee




views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/home_login', methods=['POST'])
def dummy_login():
    # Dummy login logic
    # For now, just set a session variable to indicate user is logged in
    session['logged_in'] = True
    # Redirect to the employee list page or wherever you want to redirect after login
    return redirect(url_for('views.render_employee_list'))

@views.route('/employee_list')
def render_employee_list():
    employees = Employee.query.all()
    return render_template("employee_list.html", employees=employees)

@views.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('views.render_employee_list'))  

@views.route('/update_employee/<int:employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    departments = Department.query.all()
    designations = Designation.query.all()
    if request.method == 'POST':
        
        employee.firstname = request.form['firstname']
        employee.middlename = request.form['middlename']
        employee.lastname = request.form['lastname']
        employee.address_line = request.form['address_line']
        employee.brgy = request.form['brgy']
        employee.province = request.form['province']
        employee.country = request.form['country']
        employee.zipcode = request.form['zipcode']

        department_name = request.form['department']
        department = Department.query.filter_by(dept_name=department_name).first()
        if department is None:
            department = Department(dept_name=department_name)
            db.session.add(department)

        employee.department = department

        designation_name = request.form['designation']
        designation = Designation.query.filter_by(designation_name=designation_name).first()
        if designation is None:
            designation = Designation(designation_name=designation_name)
            db.session.add(designation)

        assign_designation = AssignDesignation(employee_type=request.form['employee_type'], status=request.form['status'], designation=designation)
        employee.assign_designation = [assign_designation]

        db.session.commit()
        return redirect(url_for('views.render_employee_list'))

    return render_template('update_employee.html', employee=employee, departments=departments, designations=designations)

@views.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        address_line = request.form['address_line']
        brgy = request.form['brgy']
        province = request.form['province']
        country = request.form['country']
        zipcode = request.form['zipcode']
        department_name = request.form['department']
        employee_type = request.form['employee_type']
        status = request.form['status']
        designation_name = request.form['designation']

        department = Department.query.filter_by(dept_name=department_name).first()
        if department is None:
            department = Department(dept_name=department_name)
            db.session.add(department)

        designation = Designation.query.filter_by(designation_name=designation_name).first()
        if designation is None:
            designation = Designation(designation_name=designation_name)
            db.session.add(designation)

        new_employee = Employee(
            
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            address_line=address_line,
            brgy=brgy,
            province=province,
            country=country,
            zipcode=zipcode,
            department=department,
        )

        assign_designation = AssignDesignation(employee_type=employee_type, status=status, designation=designation)
        new_employee.assign_designation.append(assign_designation)

        db.session.add(new_employee)
        db.session.commit()
        
        return redirect(url_for('views.render_employee_list'))
    return render_template('add_employee.html')


@views.route('/logout')
def logout():
    # Clear session data to log out the user
    session.pop('logged_in', None)
    return redirect(url_for('views.home'))



@views.route('/update_signatory/<int:signatory_id>', methods=['GET', 'POST'])
def update_signatory(signatory_id):
    # Your update signatory logic here
    return render_template('update_signatory.html', signatory_id=signatory_id)


@views.route('/apply_leave/<int:employee_id>', methods=['GET', 'POST'])
def apply_leave(employee_id):
    if request.method == 'POST':
        # Extract form data
        leave_type = request.form['leave_type']
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']

        # Parse date strings into datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Set leave_status to "Pending"
        leave_status = "Pending"
        
        # Create a new leave record with the provided data
        new_leave = Leaves(employee_id=employee_id, start_leave=start_date, end_leave=end_date, 
                           leave_type=leave_type, status=leave_status)
        db.session.add(new_leave)
        db.session.commit()
        
        return redirect(url_for('views.leave_list'))  # Updated endpoint name
    else:
        # Render the form, passing the employee_id to the template
        return render_template("apply_leave.html", employee_id=employee_id)




@views.route('/apply_leave_html')
def apply_leave_html():
    # Render apply_leave.html template
    return render_template("apply_leave.html")

@views.route('/add_signatories', methods=['GET', 'POST'])
def add_signatory():
    if request.method == 'POST':
        # Handle form submission to add a new signatory
        # Extract form data and create a new signatory record
        firstname = request.form['firstname']
        middlename = request.form.get('middlename', '')  # Handle the possibility of middlename being empty
        lastname = request.form['lastname']
        email = request.form['email']
        highersuperior = request.form['highersuperior']
        department_name = request.form['department']
        designation_name = request.form['designation']
        employee_type = request.form['employee_type']
        status = request.form['status']

        # Fetch the associated employee
        employee = Employee.query.filter_by(firstname=firstname, middlename=middlename, lastname=lastname).first()

        # Assuming you have proper validation to ensure an employee is found

        # Create a new signatory record associated with the employee
        new_signatory = Signatories(
            employee_id=employee.employee_id,  # Associate the signatory with the employee
            highersuperior=highersuperior,
            status=status
        )

        # Add the new signatory to the database
        db.session.add(new_signatory)
        db.session.commit()

        # Redirect to the signatories list page after adding
        return redirect(url_for('views.signatories_list'))
    else:
        # Render the add_signatory template for GET request
        # Fetch the list of employees to pass to the template
        employees = Employee.query.all()
        return render_template("add_signatories.html", employees=employees)

    
def get_employee_id():
    # Example implementation: retrieve employee_id from session
    return session.get('employee_id')

@views.route('/leave_list')
def leave_list():
    # Fetch all leave applications from the database
    leaves = Leaves.query.all()
    # Fetch all employees from the database
    employees = Employee.query.all()
    return render_template("leave_list.html", leaves=leaves, employees=employees)


@views.route('/approve_leave/<int:leave_id>', methods=['POST'])
def approve_leave(leave_id):
    # Retrieve the leave request by leave_id
    leave = Leaves.query.get_or_404(leave_id)

    # Extract director's first name and last name from the form data
    director_first_name = request.form['director_first_name']
    director_last_name = request.form['director_last_name']

    # Find if the director exists and is authorized
    authorized_director = Employee.query \
        .join(AssignDesignation) \
        .join(Designation) \
        .filter(Employee.firstname == director_first_name,
                Employee.lastname == director_last_name,
                Designation.designation_name == 'Director') \
        .first()

    if authorized_director:
        # Director is authorized, update leave status to 'Approved'
        leave.status = 'Approved'  # Corrected to leave.status
        db.session.commit()

        return jsonify(message="Leave approved successfully."), 200
    else:
        # Director is not authorized, return an error message
        return jsonify({'error': 'Invalid director name. Please provide correct first name and last name of the director.'}), 400


    
@views.route('/decline_leave/<int:leave_id>', methods=['POST'])
def decline_leave(leave_id):
    # Retrieve the leave request by leave_id
    leave = Leaves.query.get_or_404(leave_id)

    # Extract director's first name and last name from the form data
    director_first_name = request.form['director_first_name']
    director_last_name = request.form['director_last_name']

    # Find if the director exists and is authorized
    authorized_director = Employee.query \
        .join(AssignDesignation) \
        .join(Designation) \
        .filter(Employee.firstname == director_first_name,
                Employee.lastname == director_last_name,
                Designation.designation_name == 'Director') \
        .first()

    if authorized_director:
        # Director is authorized, update leave status to 'Declined'
        leave.status = 'Declined'
        db.session.commit()

        return jsonify(message="Leave declined successfully."), 200
    else:
        # Director is not authorized, return an error message
        return jsonify({'error': 'Invalid director name. Please provide correct first name and last name of the director.'}), 400


@views.route('/signatories_list')
def signatories_list():
    director_signatories = Employee.query \
        .join(AssignDesignation) \
        .join(Designation) \
        .filter(Designation.designation_name == 'Director') \
        .options(joinedload(Employee.assign_designation)) \
        .all()
    return render_template("signatories_list.html", employees=director_signatories)


@views.route('/leave_details')
def leave_details():
    # Fetch leaves along with their associated employees and designations
    leaves = Leaves.query \
        .options(joinedload(Leaves.employee)
        .joinedload(Employee.assign_designation)
        .joinedload(AssignDesignation.designation)) \
        .all()

    return render_template("leave_details.html", leaves=leaves) 


# # -------------------------------------------------------------------
# @views.route('/subordinates/<int:director_id>')
# def show_subordinates(director_id):
#     # Get the director
#     director = Employee.query.get_or_404(director_id)
#     # Get the department
#     department = director.department
#     # Get all employees under the same department
#     subordinates = Employee.query.filter_by(department=department).all()
#     return render_template('subordinates.html', director=director, subordinates=subordinates)

# @views.route('/subordinates/<int:director_id>')
# def show_subordinates(director_id):
#     # Get the director
#     director = Employee.query.get_or_404(director_id)
#     # Get the department
#     department = director.department
#     # Get all employees under the same department, excluding the director
#     subordinates = Employee.query.filter(Employee.department == department, Employee.id != director_id).all()
#     return render_template('subordinates.html', director=director, subordinates=subordinates)

@views.route('/subordinates/<int:director_id>')
def show_subordinates(director_id):
    # Get the director
    director = Employee.query.get_or_404(director_id)
    # Get the department
    department = director.department
    # Get all employees under the same department, excluding the director
    subordinates = Employee.query.filter(Employee.department == department, Employee.employee_id != director_id).all()
    return render_template('subordinates.html', director=director, subordinates=subordinates)

@views.route('/payroll_list')
def render_payroll_list():
    # Assuming you have a method in your Employee model to fetch payroll-related data
    employees = Employee.query.all()  # Adjust this according to your actual implementation
    return render_template('payroll_list.html', employees=employees)

@views.route('/check_payroll/<int:employee_id>')
def check_payroll(employee_id):
    # Fetch the employee details from the database based on the employee ID
    employee = Employee.query.get_or_404(employee_id)
    
    # Calculate initial income and tax rate based on the employee's position
    initial_income, tax_rate = calculate_initial_income_and_tax_rate(employee)
    
    # Pass the employee details, date today, initial income, and tax rate to the template
    return render_template('check_payroll.html', employee=employee, date_today=date.today(), initial_income=initial_income, tax_rate=tax_rate)

def calculate_initial_income_and_tax_rate(employee):
    position = employee.assign_designation[0].designation.designation_name
    employee_type = employee.assign_designation[0].employee_type
    
    # Set initial income and tax rate based on employee's position and type
    if position == 'Director':
        initial_income = 2000.00
        tax_rate = 0.05
    elif position == 'Manager':
        initial_income = 1500.00
        tax_rate = 0.04
    elif position == 'Team Leader':
        initial_income = 1200.00
        tax_rate = 0.03
    elif position == 'Team Member':
        initial_income = 1000.00
        tax_rate = 0.03

    return initial_income, tax_rate


