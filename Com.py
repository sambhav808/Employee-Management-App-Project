import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

# Global variables to store data
employees_data = []
teams_data = []
projects_data = []

# Establish database connection
def connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Company',
            user='root',
            password='Sambhav@808'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL database: {e}")
        return None

# Fetch all employees from the Employee table
def fetch_employees():
    global employees_data
    employees_data = []  # Clear previous data
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT emp_id, emp_name, dob, contact, email, address, dept_id, supervisor_id FROM Employee")
            employees_data = cursor.fetchall()
    except Error as e:
        messagebox.showerror("Error", f"Error fetching employees: {e}")
    finally:
        if connection:
            connection.close()

# Fetch all teams from the Team table
def fetch_teams():
    global teams_data
    teams_data = []  # Clear previous data
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT team_id, team_name, dept_id FROM Team")
            teams_data = cursor.fetchall()
    except Error as e:
        messagebox.showerror("Error", f"Error fetching teams: {e}")
    finally:
        if connection:
            connection.close()

# Fetch all projects from the Project table
def fetch_projects():
    global projects_data
    projects_data = []  # Clear previous data
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT p.proj_id, p.proj_name, p.start_date, p.end_date, p.dept_id, p.team_head, p.budget,
                       COUNT(w.emp_id) AS num_employees
                FROM Project p
                LEFT JOIN Works_On w ON p.proj_id = w.proj_id
                GROUP BY p.proj_id
            """)
            projects_data = cursor.fetchall()
    except Error as e:
        messagebox.showerror("Error", f"Error fetching projects: {e}")
    finally:
        if connection:
            connection.close()

# Populate the employee listbox
def populate_employee_listbox():
    fetch_employees()
    listbox_employees.delete(0, tk.END)  # Clear previous items
    for employee in employees_data:
        listbox_employees.insert(tk.END, employee[1])  # Insert emp_name

# Populate the team listbox
def populate_team_listbox():
    fetch_teams()
    listbox_teams.delete(0, tk.END)  # Clear previous items
    for team in teams_data:
        listbox_teams.insert(tk.END, team[1])  # Insert team_name

# Populate the project listbox
def populate_project_listbox():
    fetch_projects()
    listbox_projects.delete(0, tk.END)  # Clear previous items
    for project in projects_data:
        listbox_projects.insert(tk.END, project[1])  # Insert proj_name

# Handle selection in the employee listbox
def on_employee_select(event):
    selected_index = listbox_employees.curselection()
    if selected_index:
        selected_employee = employees_data[selected_index[0]]
        emp_id.set(selected_employee[0])
        emp_name.set(selected_employee[1])
        dob.set(selected_employee[2])
        contact.set(selected_employee[3])
        email.set(selected_employee[4])
        address.set(selected_employee[5])
        dept_id.set(selected_employee[6])
        supervisor_id.set(selected_employee[7])  # Set supervisor_id value

# Handle selection in the project listbox
def on_project_select(event):
    selected_index = listbox_projects.curselection()
    if selected_index:
        selected_project = projects_data[selected_index[0]]
        proj_id.set(selected_project[0])
        proj_name.set(selected_project[1])
        start_date.set(selected_project[2])
        end_date.set(selected_project[3])
        proj_dept_id.set(selected_project[4])
        team_head.set(selected_project[5])
        budget.set(selected_project[6])
        num_employees.set(selected_project[7])  # Number of employees in the project

# Add a new employee
def open_add_employee_window():
    add_employee_window = tk.Toplevel(root)
    add_employee_window.title("Add Employee")

    # Employee details labels and entry fields
    tk.Label(add_employee_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="DOB (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Contact:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Email:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Address:").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Department ID:").grid(row=5, column=0, padx=5, pady=5)
    tk.Label(add_employee_window, text="Supervisor ID:").grid(row=6, column=0, padx=5, pady=5)  # Add supervisor label

    add_emp_name = tk.StringVar()
    add_dob = tk.StringVar()
    add_contact = tk.StringVar()
    add_email = tk.StringVar()
    add_address = tk.StringVar()
    add_dept_id = tk.StringVar()
    add_supervisor_id = tk.StringVar()  # Add supervisor variable

    emp_name_entry = tk.Entry(add_employee_window, textvariable=add_emp_name)
    dob_entry = tk.Entry(add_employee_window, textvariable=add_dob)
    contact_entry = tk.Entry(add_employee_window, textvariable=add_contact)
    email_entry = tk.Entry(add_employee_window, textvariable=add_email)
    address_entry = tk.Entry(add_employee_window, textvariable=add_address)
    dept_id_entry = tk.Entry(add_employee_window, textvariable=add_dept_id)
    supervisor_id_entry = tk.Entry(add_employee_window, textvariable=add_supervisor_id)  # Add supervisor entry

    emp_name_entry.grid(row=0, column=1, padx=5, pady=5)
    dob_entry.grid(row=1, column=1, padx=5, pady=5)
    contact_entry.grid(row=2, column=1, padx=5, pady=5)
    email_entry.grid(row=3, column=1, padx=5, pady=5)
    address_entry.grid(row=4, column=1, padx=5, pady=5)
    dept_id_entry.grid(row=5, column=1, padx=5, pady=5)
    supervisor_id_entry.grid(row=6, column=1, padx=5, pady=5)  # Add supervisor entry grid

    # Function to save a new employee to the database
    def save_employee():
        name = add_emp_name.get()
        dob = add_dob.get()
        contact = add_contact.get()
        email = add_email.get()
        address = add_address.get()
        dept_id = add_dept_id.get()
        supervisor_id = add_supervisor_id.get()  # Add supervisor ID

        try:
            connection = connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO Employee (emp_name, dob, contact, email, address, dept_id, supervisor_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, dob, contact, email, address, dept_id, supervisor_id))
                connection.commit()
                messagebox.showinfo("Success", "Employee added successfully!")
                populate_employee_listbox()
                add_employee_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Error adding employee: {e}")
        finally:
            if connection:
                connection.close()

    # Save button in the "Add Employee" window
    tk.Button(add_employee_window, text="Save", command=save_employee).grid(row=7, column=0, columnspan=2, pady=10)

# Update employee details
def update_employee():
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Employee
                SET emp_name = %s, dob = %s, contact = %s, email = %s, address = %s, dept_id = %s, supervisor_id = %s
                WHERE emp_id = %s
            """, (emp_name.get(), dob.get(), contact.get(), email.get(), address.get(), dept_id.get(), supervisor_id.get(), emp_id.get()))  # Update supervisor_id
            connection.commit()
            messagebox.showinfo("Success", "Employee updated successfully!")
            populate_employee_listbox()
    except Error as e:
        messagebox.showerror("Error", f"Error updating employee: {e}")
    finally:
        if connection:
            connection.close()

# Delete an employee
def delete_employee():
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Employee WHERE emp_id = %s", (emp_id.get(),))
            connection.commit()
            messagebox.showinfo("Success", "Employee deleted successfully!")
            populate_employee_listbox()
    except Error as e:
        messagebox.showerror("Error", f"Error deleting employee: {e}")
    finally:
        if connection:
            connection.close()

# GUI setup
root = tk.Tk()
root.title("Company Management System")
root.geometry("800x600")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Employee Management Tab
frame_employees = ttk.Frame(notebook, width=780, height=580)
frame_employees.pack(fill='both', expand=True)

# Team Management Tab
frame_teams = ttk.Frame(notebook, width=780, height=580)
frame_teams.pack(fill='both', expand=True)

# Project Management Tab
frame_projects = ttk.Frame(notebook, width=780, height=580)
frame_projects.pack(fill='both', expand=True)

# Add tabs to the notebook
notebook.add(frame_employees, text='Employee Management')
notebook.add(frame_teams, text='Team Management')
notebook.add(frame_projects, text='Project Management')

# Employee Management UI
tk.Label(frame_employees, text="Employees").pack()
listbox_employees = tk.Listbox(frame_employees)
listbox_employees.pack(fill=tk.BOTH, expand=True)
listbox_employees.bind("<<ListboxSelect>>", on_employee_select)

tk.Button(frame_employees, text="Add Employee", command=open_add_employee_window).pack(pady=10)
tk.Button(frame_employees, text="Update Employee", command=update_employee).pack(pady=10)
tk.Button(frame_employees, text="Delete Employee", command=delete_employee).pack(pady=10)

# Team Management UI
tk.Label(frame_teams, text="Teams").pack()
listbox_teams = tk.Listbox(frame_teams)
listbox_teams.pack(fill=tk.BOTH, expand=True)

# Populate the listbox with teams
populate_team_listbox()

# Project Management UI
tk.Label(frame_projects, text="Projects").pack()
listbox_projects = tk.Listbox(frame_projects)
listbox_projects.pack(fill=tk.BOTH, expand=True)
listbox_projects.bind("<<ListboxSelect>>", on_project_select)

# Populate the listbox with projects
populate_project_listbox()

# Employee details section
emp_id = tk.StringVar()
emp_name = tk.StringVar()
dob = tk.StringVar()
contact = tk.StringVar()
email = tk.StringVar()
address = tk.StringVar()
dept_id = tk.StringVar()
supervisor_id = tk.StringVar()  # Supervisor ID

tk.Label(root, text="Employee Details").pack()

details_frame = tk.Frame(root)
details_frame.pack(pady=20)

tk.Label(details_frame, text="Name:").grid(row=0, column=0)
tk.Entry(details_frame, textvariable=emp_name).grid(row=0, column=1)

tk.Label(details_frame, text="DOB (YYYY-MM-DD):").grid(row=1, column=0)
tk.Entry(details_frame, textvariable=dob).grid(row=1, column=1)

tk.Label(details_frame, text="Contact:").grid(row=2, column=0)
tk.Entry(details_frame, textvariable=contact).grid(row=2, column=1)

tk.Label(details_frame, text="Email:").grid(row=3, column=0)
tk.Entry(details_frame, textvariable=email).grid(row=3, column=1)

tk.Label(details_frame, text="Address:").grid(row=4, column=0)
tk.Entry(details_frame, textvariable=address).grid(row=4, column=1)

tk.Label(details_frame, text="Department ID:").grid(row=5, column=0)
tk.Entry(details_frame, textvariable=dept_id).grid(row=5, column=1)

tk.Label(details_frame, text="Supervisor ID:").grid(row=6, column=0)  # Add supervisor label
tk.Entry(details_frame, textvariable=supervisor_id).grid(row=6, column=1)  # Add supervisor entry

# Project details section
proj_id = tk.StringVar()
proj_name = tk.StringVar()
start_date = tk.StringVar()
end_date = tk.StringVar()
proj_dept_id = tk.StringVar()
team_head = tk.StringVar()
budget = tk.StringVar()
num_employees = tk.StringVar()

tk.Label(root, text="Project Details").pack()

project_details_frame = tk.Frame(root)
project_details_frame.pack(pady=20)

tk.Label(project_details_frame, text="Name:").grid(row=0, column=0)
tk.Entry(project_details_frame, textvariable=proj_name).grid(row=0, column=1)

tk.Label(project_details_frame, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0)
tk.Entry(project_details_frame, textvariable=start_date).grid(row=1, column=1)

tk.Label(project_details_frame, text="End Date (YYYY-MM-DD):").grid(row=2, column=0)
tk.Entry(project_details_frame, textvariable=end_date).grid(row=2, column=1)

tk.Label(project_details_frame, text="Department ID:").grid(row=3, column=0)
tk.Entry(project_details_frame, textvariable=proj_dept_id).grid(row=3, column=1)

tk.Label(project_details_frame, text="Team Head ID:").grid(row=4, column=0)
tk.Entry(project_details_frame, textvariable=team_head).grid(row=4, column=1)

tk.Label(project_details_frame, text="Budget:").grid(row=5, column=0)
tk.Entry(project_details_frame, textvariable=budget).grid(row=5, column=1)

tk.Label(project_details_frame, text="Number of Employees:").grid(row=6, column=0)
tk.Entry(project_details_frame, textvariable=num_employees).grid(row=6, column=1)

# Initial population of listboxes
populate_employee_listbox()
populate_team_listbox()
populate_project_listbox()

root.mainloop()
