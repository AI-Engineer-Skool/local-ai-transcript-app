"""
Exercise 1: Gym Basics - Your First Workout

Welcome to your first programming exercise! In this exercise, you'll learn how to
store and display information about a workout. Think of variables as containers
that hold information - like tracking your workout details on a gym card.

Concepts covered:
- Variables (containers for storing data)
- Data types (text, numbers, decimals)
- String formatting (displaying information nicely)
- Basic output with print()

Learning Goals:
- Understand how to create and use variables
- Learn different types of data (strings, integers, floats)
- Display workout information in a readable format

Run this exercise: uv run exercise/python/01_gym_basics.py
"""

# ============================================================================
# QUICK INTRO: What are variables?
# ============================================================================
# Variables are like labeled containers. Just like you might write your name
# on a water bottle at the gym, you give names to pieces of information in code.
#
# In Python, you create a variable like this:
#   variable_name = value
#
# No need to declare types - Python figures it out!


# ============================================================================
# EXAMPLE CODE
# ============================================================================
# Let's track a workout session. Here's how we store different types of information:

# Text information uses quotes (called "strings")
exercise_name = "Bench Press"
muscle_group = "Chest"

# Whole numbers are called "integers"
sets_completed = 3
reps_per_set = 10

# Numbers with decimals are called "floats"
weight_used = 135.5  # in pounds

# We can display this information using print()
print("=== Workout Log ===")
print("Exercise:", exercise_name)
print("Target:", muscle_group)
print("Sets:", sets_completed)
print("Reps per set:", reps_per_set)
print("Weight:", weight_used, "lbs")

# We can also do simple math with numbers
total_reps = sets_completed * reps_per_set
print("Total reps:", total_reps)

# Python lets us create formatted strings with f-strings (notice the 'f' before the quote)
summary = f"You completed {total_reps} reps of {exercise_name} at {weight_used} lbs!"
print(summary)


# ============================================================================
# YOUR TURN: TODO EXERCISES
# ============================================================================

print("\n=== YOUR WORKOUT LOG ===")

# TODO 1: Create variables for YOUR workout
# Create variables to track a squat workout:
# - exercise_name should be "Squat"
# - muscle_group should be "Legs"
# - sets_completed should be 4
# - reps_per_set should be 8
# - weight_used should be 185.0
#
# Stuck? Try asking me: "How do I create a variable in Python?"
# Or: "What's the difference between 185 and 185.0?"

# Write your code here:

# TODO 2: Calculate and display the total reps
# Calculate the total reps (sets × reps per set) and store it in a variable called total_reps
# Then print it out with a descriptive message.
#
# HINT: Use the * operator to multiply numbers
# Stuck? Ask: "How do I multiply two variables in Python?"

# Write your code here:


# TODO 3: Create a workout summary using an f-string
# Create a variable called workout_summary that contains a message like:
# "Today I did 32 reps of Squats at 185.0 lbs targeting my Legs!"
#
# Use an f-string (start with f" and use {variable_name} to insert variables)
# Then print your summary.
#
# Need help? Ask: "How do I use f-strings in Python?"
# Or: "Show me an example of an f-string with variables"

# Write your code here:

# TODO 4: Track rest time
# Create a variable called rest_seconds and set it to 90 (seconds of rest between sets)
# Then calculate and print how many total minutes of rest you took
# (Hint: multiply rest_seconds by the number of sets, then divide by 60 to get minutes)
#
# HINT: Use / for division
# Stuck? Ask: "How do I convert seconds to minutes in Python?"

# Write your code here:

# ============================================================================
# BONUS CHALLENGES (Optional)
# ============================================================================

# BONUS 1: Calculate total weight lifted
# Calculate the total weight you lifted: sets × reps per set × weight used
# This is called "volume" in fitness tracking!
#
# For help: Ask me "How do I calculate workout volume?"

# Write your code here:


# BONUS 2: Create a complete workout report
# Use multiple print statements or f-strings to create a nice-looking report
# that includes all the information: exercise name, muscle group, sets, reps,
# weight, total reps, rest time, and total volume.
#
# Get creative with the formatting! Use separators like "===" to make it look nice.
#
# Want ideas? Ask: "Show me how to format output nicely in Python"

# Write your code here:


# ============================================================================
# TESTING YOUR CODE
# ============================================================================

# When you run this file, you should see output similar to:
#
# === Workout Log ===
# Exercise: Bench Press
# Target: Chest
# Sets: 3
# Reps per set: 10
# Weight: 135.5 lbs
# Total reps: 30
# You completed 30 reps of Bench Press at 135.5 lbs!
#
# === YOUR WORKOUT LOG ===
# [Your output will appear here based on your TODO solutions]
#
# If you see Python errors (red text), don't worry! Errors are a normal part of coding.
# Try asking me: "I got an error on line X, what does it mean?"


if __name__ == "__main__":
    # This special block runs when you execute the file
    # Everything above this line runs automatically
    pass
