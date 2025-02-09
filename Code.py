import tkinter as tk
from tkinter import messagebox
import json
import hashlib
from datetime import datetime
import matplotlib.pyplot as plt


# Utility Functions
def hash_password(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_data():
    """Loads user data from a JSON file."""
    try:
        with open("fitness_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data(data):
    """Saves user data to a JSON file."""
    with open("fitness_data.json", "w") as file:
        json.dump(data, file, indent=4)


# Application Class
class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health and Fitness Tracker")
        self.root.configure(bg="lightgreen")  # Set root background
        self.data = load_data()
        self.username = None
        self.login_screen()

    def login_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="lightblue", padx=60, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text="Login 💪", font=("Helvetica", 18, "bold"), bg="lightblue").pack(pady=10)
        tk.Label(frame, text="Username:", bg="lightblue").pack()
        username_entry = tk.Entry(frame)
        username_entry.pack(pady=5)

        tk.Label(frame, text="Password:", bg="lightblue").pack()
        password_entry = tk.Entry(frame, show="*")
        password_entry.pack(pady=5)

        def login_action():
            username = username_entry.get()
            password = hash_password(password_entry.get())
            if username in self.data and self.data[username]["password"] == password:
                self.username = username
                self.dashboard()
            else:
                messagebox.showerror("Login Error", "Invalid username or password.")

        tk.Button(frame, text="Login", command=login_action, bg="green", fg="white").pack(pady=10)
        tk.Button(frame, text="Register", command=self.registration_screen, bg="green", fg="white").pack()

    def registration_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="lightyellow", padx=60, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text="Register 🫣", font=("Arial", 18, "bold"), bg="lightyellow").pack(pady=10)
        tk.Label(frame, text="Name:", bg="lightyellow").pack()
        name_entry = tk.Entry(frame)
        name_entry.pack(pady=5)

        tk.Label(frame, text="Age:", bg="lightyellow").pack()
        age_entry = tk.Entry(frame)
        age_entry.pack(pady=5)

        tk.Label(frame, text="Height (cm):", bg="lightyellow").pack()
        height_entry = tk.Entry(frame)
        height_entry.pack(pady=5)

        tk.Label(frame, text="Weight (kg):", bg="lightyellow").pack()
        weight_entry = tk.Entry(frame)
        weight_entry.pack(pady=5)

        tk.Label(frame, text="Username:", bg="lightyellow").pack()
        username_entry = tk.Entry(frame)
        username_entry.pack(pady=5)

        tk.Label(frame, text="Password:", bg="lightyellow").pack()
        password_entry = tk.Entry(frame, show="*")
        password_entry.pack(pady=5)

        def register_action():
            name = name_entry.get()
            try:
                age = int(age_entry.get())
                height = float(height_entry.get())
                weight = float(weight_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for age, height, and weight.")
                return

            username = username_entry.get()
            password = password_entry.get()
            if username in self.data:
                messagebox.showerror("Registration Error", "Username already exists!")
                return

            hashed_password = hash_password(password)
            water_goal = weight * 35
            bmi = weight / (height / 100) ** 2

            self.data[username] = {
                "password": hashed_password,
                "profile": {
                    "name": name,
                    "age": age,
                    "height": height,
                    "weight": weight,
                    "water_goal": water_goal,
                    "logs": {}
                }
            }
            save_data(self.data)
            messagebox.showinfo("Registration Successful", f"Welcome {name}! Your BMI is {bmi:.2f}. Water goal: {water_goal:.2f} ml.")
            self.login_screen()

        tk.Button(frame, text="Register", command=register_action, bg="green", fg="white").pack(pady=10)
        tk.Button(frame, text="Back to Login", command=self.login_screen, bg="red", fg="white").pack()

    def dashboard(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="lightblue", padx=60, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text=f"Welcome {self.username}!", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=10)
        tk.Button(frame, text="Log Activity", command=self.log_activity_screen, bg="green", fg="white").pack(pady=5)
        tk.Button(frame, text="View Progress", command=self.view_progress_screen, bg="green", fg="white").pack(pady=5)
        tk.Button(frame, text="Update Profile", command=self.update_profile_screen, bg="green", fg="white").pack(pady=5)
        tk.Button(frame, text="Logout", command=self.login_screen, bg="red", fg="white").pack(pady=5)

    def log_activity_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="lightyellow", padx=60, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text="Log Activity", font=("Arial", 18, "bold"), bg="lightyellow").pack(pady=10)
        tk.Label(frame, text="Steps Walked:", bg="lightyellow").pack()
        steps_entry = tk.Entry(frame)
        steps_entry.pack(pady=5)

        tk.Label(frame, text="Calories Burned:", bg="lightyellow").pack()
        calories_entry = tk.Entry(frame)
        calories_entry.pack(pady=5)

        tk.Label(frame, text="Water Intake (ml):", bg="lightyellow").pack()
        water_entry = tk.Entry(frame)
        water_entry.pack(pady=5)

        def log_action():
            today = str(datetime.today().date())
            try:
                steps = int(steps_entry.get())
                calories = int(calories_entry.get())
                water = int(water_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")
                return

            if today not in self.data[self.username]["profile"]["logs"]:
                self.data[self.username]["profile"]["logs"][today] = {"steps": 0, "calories": 0, "water": 0}

            log = self.data[self.username]["profile"]["logs"][today]
            log["steps"] += steps
            log["calories"] += calories
            log["water"] += water
            save_data(self.data)
            messagebox.showinfo("Log Successful", "Activity logged successfully!")
            self.dashboard()

        tk.Button(frame, text="Log Activity", command=log_action, bg="green", fg="white").pack(pady=10)
        tk.Button(frame, text="Back to Dashboard", command=self.dashboard, bg="red", fg="white").pack()

    def view_progress_screen(self):
        logs = self.data[self.username]["profile"]["logs"]
        if not logs:
            messagebox.showinfo("Progress", "No activity logged yet!")
            self.dashboard()
            return

        dates = list(logs.keys())
        steps = [log["steps"] for log in logs.values()]
        water = [log["water"] for log in logs.values()]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, steps, marker='o', label="Steps Walked")
        plt.plot(dates, water, marker='s', label="Water Intake (ml)")

        plt.title(f"{self.username}'s Fitness Progress")
        plt.xlabel("Date")
        plt.ylabel("Values")
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def update_profile_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="lightyellow", padx=60, pady=40)
        frame.pack(expand=True)

        tk.Label(frame, text="Update Profile", font=("Arial", 18, "bold"), bg="lightyellow").pack(pady=10)
        tk.Label(frame, text="New Weight (kg):", bg="lightyellow").pack()
        weight_entry = tk.Entry(frame)
        weight_entry.pack(pady=5)

        def update_action():
            try:
                new_weight = float(weight_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid weight.")
                return

            self.data[self.username]["profile"]["weight"] = new_weight
            self.data[self.username]["profile"]["water_goal"] = new_weight * 35
            save_data(self.data)
            messagebox.showinfo("Update Successful", f"Weight updated! New water goal: {new_weight * 35:.2f} ml.")
            self.dashboard()

        tk.Button(frame, text="Update", command=update_action, bg="green", fg="white").pack(pady=10)
        tk.Button(frame, text="Back to Dashboard", command=self.dashboard, bg="red", fg="white").pack()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = FitnessApp(root)
    root.mainloop()

