"""
Exercise 5: Gym Equipment Manager

So far you've used basic data types, lists, dictionaries, and functions. Now let's
learn about CLASSES - a way to create your own custom data types! A class is like
a blueprint for creating objects. Think of it as a template for gym equipment.

Concepts covered:
- Classes (blueprints for creating objects)
- Objects (instances of a class)
- Attributes (data stored in an object)
- Methods (functions that belong to a class)
- The __init__ method (constructor)
- The self parameter

Learning Goals:
- Understand the concept of classes and objects
- Create your own class to represent gym equipment
- Use methods to perform actions on objects
- Manage state (data that changes over time)
- Build a gym equipment tracking system

Run this exercise: uv run exercise/python/05_gym_equipment.py
"""

# ============================================================================
# QUICK INTRO: What are classes?
# ============================================================================
# A class is a blueprint for creating objects. An object is a specific instance
# of that blueprint.
#
# Think about it: "Barbell" is a type of equipment (the class). But the specific
# 45-pound Olympic barbell in your gym that's currently being used is an object
# (an instance of the Barbell class).
#
# Classes bundle data (attributes) and functions (methods) together.


# ============================================================================
# EXAMPLE CODE
# ============================================================================


class GymEquipment:
    """
    A class representing a piece of gym equipment.

    Attributes:
        name: The equipment name
        weight: The weight in pounds
        in_use: Whether it's currently being used
        uses_today: How many times it's been used today
    """

    def __init__(self, name, weight):
        """
        The __init__ method is called when you create a new object.
        'self' refers to the specific object being created.

        Parameters:
            name: Equipment name
            weight: Equipment weight in pounds
        """
        self.name = name
        self.weight = weight
        self.in_use = False
        self.uses_today = 0

    def check_out(self):
        """
        Mark equipment as in use.
        Methods are functions that belong to the class.
        They can access and modify the object's attributes using 'self'.
        """
        if self.in_use:
            print(f"{self.name} is already in use!")
        else:
            self.in_use = True
            self.uses_today += 1
            print(f"{self.name} checked out. Uses today: {self.uses_today}")

    def check_in(self):
        """Mark equipment as available."""
        if not self.in_use:
            print(f"{self.name} is already checked in!")
        else:
            self.in_use = False
            print(f"{self.name} checked back in. Ready for next person!")

    def get_status(self):
        """Return a status message about this equipment."""
        status = "IN USE" if self.in_use else "AVAILABLE"
        return f"{self.name} ({self.weight} lbs) - {status} - Used {self.uses_today} times today"


# Create objects (instances) of the GymEquipment class
print("=== Creating Equipment ===")
barbell = GymEquipment("Olympic Barbell", 45)
dumbbell = GymEquipment("50lb Dumbbell", 50)

print(barbell.name)

# Use methods on the objects
print("\n=== Using Equipment ===")
print(barbell.get_status())
barbell.check_out()
print(barbell.get_status())

print()
print(dumbbell.get_status())
dumbbell.check_out()
dumbbell.check_in()
print(dumbbell.get_status())

# Each object has its own separate data
print("\n=== Multiple Uses ===")
barbell.check_in()
barbell.check_out()
barbell.check_in()
barbell.check_out()
print(f"Barbell uses: {barbell.uses_today}")
print(f"Dumbbell uses: {dumbbell.uses_today}")  # Different from barbell!


# ============================================================================
# YOUR TURN: TODO EXERCISES
# ============================================================================

print("\n\n=== YOUR GYM EQUIPMENT MANAGER ===")

# TODO 1: Create objects for your gym
# Create three equipment objects:
# - bench: A "Bench Press Bench" weighing 50 lbs
# - squat_rack: A "Squat Rack" weighing 100 lbs
# - kettlebell: A "32kg Kettlebell" weighing 70 lbs
#
# Then print the status of each using the get_status() method
#
# HINT: Use the same pattern as the examples above
#
# Stuck? Ask: "How do I create an object from a class in Python?"
# Or: "What's the difference between a class and an object?"

# Write your code here:


# TODO 2: Simulate checking out and using equipment
# Simulate someone using the bench:
# 1. Check out the bench
# 2. Print its status
# 3. Check it back in
# 4. Print its status again
#
# Need help? Ask: "How do I call methods on an object?"

# Write your code here:


# TODO 3: Track multiple uses
# Simulate the squat_rack being used 3 times in a row:
# - Check it out, check it in, check it out, check it in, check it out, check it in
# Then print how many times it's been used today (access the uses_today attribute)
#
# HINT: You can access attributes directly: squat_rack.uses_today
#
# Stuck? Ask: "How do I access an object's attributes?"

# Write your code here:


# TODO 4: Create a new class for a Treadmill
# Create a class called Treadmill that has:
# - __init__ method taking: name, max_speed (in mph)
# - Attributes: name, max_speed, is_running (starts as False), distance_today (starts as 0)
# - Method start_running(): sets is_running to True, prints a message
# - Method stop_running(): sets is_running to False, prints a message
# - Method log_distance(miles): adds miles to distance_today
# - Method get_status(): returns a string with treadmill info
#
# HINT: Follow the same pattern as GymEquipment class above
#
# Stuck? Ask: "How do I create a class in Python?"
# Or: "Show me the structure of a class with methods"

# Write your code here:


# TODO 5: Test your Treadmill class
# Create a Treadmill object called treadmill1:
# - Name: "Treadmill #1"
# - Max speed: 12.0 mph
#
# Then:
# 1. Print its status
# 2. Start it running
# 3. Log 3.5 miles
# 4. Stop it running
# 5. Print its status again
#
# Need help? Ask: "How do I use a class I just created?"

# Write your code here:


# ============================================================================
# BONUS CHALLENGES (Optional)
# ============================================================================

# BONUS 1: Add a maintenance tracking feature
# Add a method to the GymEquipment class called needs_maintenance() that returns
# True if uses_today is greater than 10, False otherwise.
# Then add a method called perform_maintenance() that resets uses_today to 0
# and prints a maintenance message.
#
# HINT: You'll need to modify the GymEquipment class definition above
#
# For help: Ask "How do I add new methods to an existing class?"

# Write your code here:


# BONUS 2: Create a BenchPress class that inherits from GymEquipment
# Use class inheritance to create a BenchPress class that:
# - Inherits from GymEquipment
# - Adds a max_weight attribute
# - Adds a method log_lift(weight) that checks if weight > max_weight
#   and updates max_weight if it is
#
# This is advanced! Ask: "How does class inheritance work in Python?"

# Write your code here:


# BONUS 3: Create a gym inventory system
# Create a list called gym_inventory and add all your equipment objects to it.
# Then loop through and print the status of all equipment.
# Calculate and print how many pieces are currently in use.
#
# Want guidance? Ask: "How do I store objects in a list and loop through them?"

# Write your code here:


# ============================================================================
# TESTING YOUR CODE
# ============================================================================

# Expected behavior:
# - bench, squat_rack, and kettlebell should be created and have status messages
# - Equipment should track uses correctly when checked out and in
# - Treadmill class should work with start/stop and distance tracking
# - Each object maintains its own separate state
#
# To test:
# - Print object attributes: print(bench.uses_today)
# - Call methods and verify the output
# - Create multiple objects and verify they're independent
#
# If something's not working: Ask me "Why isn't my [class/method] working?"


if __name__ == "__main__":
    pass
