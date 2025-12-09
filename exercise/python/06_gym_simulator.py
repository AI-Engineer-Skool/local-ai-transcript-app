"""
Exercise 6: Complete Gym Simulator

This is it - the culmination of everything you've learned! You'll build a complete
gym simulator that brings together variables, lists, dictionaries, functions, classes,
and now FILE I/O to save and load data. This is a real-world application!

Concepts covered:
- File I/O (reading and writing files)
- JSON format (saving structured data)
- Error handling (try/except blocks)
- Bringing together all previous concepts
- Building a complete application

Learning Goals:
- Save and load data from files
- Handle errors gracefully
- Build a multi-class system
- Create a complete, working simulation
- See how all Python concepts work together

Run this exercise: uv run exercise/python/06_gym_simulator.py
"""

import json
from datetime import datetime

# ============================================================================
# QUICK INTRO: File I/O and JSON
# ============================================================================
# Until now, when your program ends, all data disappears. File I/O lets you
# save data to disk and load it back later!
#
# JSON is a popular format for storing structured data (lists, dictionaries).
# It's like a text version of Python data structures.
#
# Key operations:
# - json.dump(data, file) - saves data to a file
# - json.load(file) - reads data from a file
# - try/except - handles errors (like file not found)


# ============================================================================
# EXAMPLE CODE
# ============================================================================


class GymMember:
    """Represents a gym member with workout history."""

    def __init__(self, name, membership_id):
        self.name = name
        self.membership_id = membership_id
        self.workouts = []
        self.total_visits = 0

    def log_workout(self, exercise, sets, reps, weight):
        """Log a workout session."""
        workout = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "exercise": exercise,
            "sets": sets,
            "reps": reps,
            "weight": weight,
            "volume": sets * reps * weight,
        }
        self.workouts.append(workout)
        self.total_visits += 1
        print(f"✓ Logged workout for {self.name}: {exercise}")

    def get_summary(self):
        """Get a summary of the member's activity."""
        if not self.workouts:
            return f"{self.name} - No workouts logged yet"

        total_volume = sum(w["volume"] for w in self.workouts)
        return f"{self.name} - {self.total_visits} visits - {total_volume} lbs total volume"

    def to_dict(self):
        """Convert member to dictionary for JSON saving."""
        return {
            "name": self.name,
            "membership_id": self.membership_id,
            "workouts": self.workouts,
            "total_visits": self.total_visits,
        }

    @staticmethod
    def from_dict(data):
        """Create a GymMember from a dictionary (for loading from JSON)."""
        member = GymMember(data["name"], data["membership_id"])
        member.workouts = data["workouts"]
        member.total_visits = data["total_visits"]
        return member


class Gym:
    """Represents the entire gym with members and operations."""

    def __init__(self, name):
        self.name = name
        self.members = {}  # Dictionary: membership_id -> GymMember
        self.next_member_id = 1

    def add_member(self, name):
        """Add a new member to the gym."""
        member_id = self.next_member_id
        self.next_member_id += 1
        member = GymMember(name, member_id)
        self.members[member_id] = member
        print(f"Welcome {name}! Your membership ID is: {member_id}")
        return member_id

    def get_member(self, member_id):
        """Get a member by their ID."""
        return self.members.get(member_id)

    def save_to_file(self, filename):
        """Save gym data to a JSON file."""
        data = {
            "gym_name": self.name,
            "next_member_id": self.next_member_id,
            "members": {mid: member.to_dict() for mid, member in self.members.items()},
        }

        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✓ Gym data saved to {filename}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")

    def load_from_file(self, filename):
        """Load gym data from a JSON file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            self.name = data["gym_name"]
            self.next_member_id = data["next_member_id"]
            self.members = {}
            for mid_str, member_data in data["members"].items():
                mid = int(mid_str)
                self.members[mid] = GymMember.from_dict(member_data)

            print(f"✓ Loaded gym data from {filename}")
            print(f"  Gym: {self.name} with {len(self.members)} members")
        except FileNotFoundError:
            print(f"✗ File {filename} not found. Starting fresh!")
        except Exception as e:
            print(f"✗ Error loading file: {e}")


# Demo the system
print("=== Gym Simulator Demo ===\n")

# Create a gym
my_gym = Gym("Iron Paradise")

# Add members
member1_id = my_gym.add_member("Alex Johnson")
member2_id = my_gym.add_member("Sam Smith")

# Log some workouts
member1 = my_gym.get_member(member1_id)
member1.log_workout("Bench Press", 3, 10, 135)
member1.log_workout("Squat", 4, 8, 185)

member2 = my_gym.get_member(member2_id)
member2.log_workout("Deadlift", 5, 5, 225)

# Print summaries
print("\n=== Member Summaries ===")
for member in my_gym.members.values():
    print(member.get_summary())

# Save to file
print()
my_gym.save_to_file("gym_data.json")


# ============================================================================
# YOUR TURN: TODO EXERCISES
# ============================================================================

print("\n\n=== YOUR GYM SIMULATOR ===\n")

# TODO 1: Create your own gym
# Create a Gym object with your chosen gym name
# Store it in a variable called your_gym
#
# Stuck? Ask: "How do I create an object from a class?"

# Write your code here:


# TODO 2: Add yourself as a member
# Use the add_member method to add yourself to the gym
# Store your member ID in a variable called my_member_id
#
# Then get your member object using get_member() and store it in my_member
#
# Need help? Ask: "How do I call a method on an object and store the result?"

# Write your code here:


# TODO 3: Log three different workouts
# Log three workouts for yourself using the log_workout method:
# 1. Bench Press: 3 sets, 10 reps, 135 lbs
# 2. Squats: 4 sets, 8 reps, 185 lbs
# 3. Pull-ups: 3 sets, 12 reps, 0 lbs (bodyweight)
#
# HINT: Call my_member.log_workout() three times
#
# Stuck? Ask: "How do I call a method multiple times with different parameters?"

# Write your code here:


# TODO 4: Add another member and log their workout
# Add a friend or workout partner to your gym
# Log at least one workout for them
#
# Need help? Ask: "Show me the pattern for adding a member and logging workouts"

# Write your code here:


# TODO 5: Print summaries of all members
# Loop through all members in your_gym.members and print their summary
#
# HINT: Use .values() to loop through the member objects
# HINT: Call the get_summary() method on each member
#
# Stuck? Ask: "How do I loop through dictionary values and call methods?"

# Write your code here:


# TODO 6: Save your gym data
# Save your gym data to a file called "my_gym_data.json"
# Use the save_to_file method
#
# After running this, check that the file was created in your exercise folder!
#
# Need help? Ask: "How do I call the save_to_file method?"

# Write your code here:


# TODO 7: Test loading data (Optional - requires running twice)
# Comment out TODOs 1-6 above, then create a new empty gym
# and try loading from "my_gym_data.json" using load_from_file()
# This demonstrates data persistence!
#
# Want to see it work? Ask: "How do I test loading saved data?"

# Write your code here:


# ============================================================================
# BONUS CHALLENGES (Optional)
# ============================================================================

# BONUS 1: Create an Equipment class
# Create a class to track gym equipment (like in Exercise 5)
# Add it to the Gym class as a dictionary of equipment
# Save and load equipment data in the JSON file
#
# For help: Ask "How do I add a new class and integrate it with existing code?"

# Write your code here:


# BONUS 2: Add workout statistics
# Add a method to GymMember called get_workout_stats() that returns:
# - Total workouts logged
# - Average volume per workout
# - Most common exercise
# - Total weight lifted (sum of all volume)
#
# Want guidance? Ask: "How do I calculate statistics from a list of dictionaries?"

# Write your code here:


# BONUS 3: Create a simple menu system
# Create a function called run_gym_menu() that:
# 1. Displays a menu of options (add member, log workout, view stats, save, quit)
# 2. Takes user input
# 3. Performs the chosen action
# 4. Loops until user chooses quit
#
# This is advanced! Ask: "How do I create an interactive menu in Python?"
# HINT: Use input() to get user choices, and a while loop to keep running

# Write your code here:


# ============================================================================
# TESTING YOUR CODE
# ============================================================================

# After completing the TODOs, you should have:
# - A gym with at least 2 members
# - Multiple workouts logged
# - Summaries printed showing visits and total volume
# - A "my_gym_data.json" file created (check your exercise folder!)
#
# To verify the file:
# 1. Look for my_gym_data.json in the exercise/python folder
# 2. Open it in your editor - it should be readable JSON
# 3. Try loading it back by running TODO 7
#
# Congratulations! You've built a complete application that:
# - Uses classes and objects
# - Manages complex data
# - Saves and loads from files
# - Handles errors gracefully


if __name__ == "__main__":
    pass
