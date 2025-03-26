import json
import random

# Define possible values for each field
names = ["John Doe", "Jane Smith", "Alex Nguyen", "Maria Tran", "Peter Le", "Sophie Pham", "David Vo", "Emma Ho", "Liam Bui", "Olivia Dang"]
ages = list(range(22, 51))  # Ages from 22 to 50
roles = ["dev", "test", "qa"]
levels = ["junior", "senior", "principal"]
skills = ["Java", "Python", "JavaScript", "React", "Node.js", "C#", ".NET", "Ruby"]
foreign_languages = ["English", "French", "Spanish", "German"]
certs = ["PMP", "AWS", "IELTS", "Scrum Master", "CCNA", "None"]
locations = ["HoChiMinh", "DaNang"]

# Function to generate a random employee
def generate_employee(employee_id):
    return {
        "name": f"{random.choice(names).split()[0]} {random.choice(names).split()[1]}",  # Unique name with ID
        "age": random.choice(ages),
        "role": random.choice(roles),
        "level": random.choice(levels),
        "skill": random.choice(skills),
        "foreign_language": random.choice(foreign_languages),
        "certs": random.choice(certs),
        "location": random.choice(locations)
    }

# Generate 100 employees
employees = [generate_employee(i) for i in range(1, 101)]

# Save to JSON file
with open("employees.json", "w") as f:
    json.dump(employees, f, indent=4)

print("Generated 100 employees and saved to 'employees.json'")
