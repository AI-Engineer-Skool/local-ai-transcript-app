"""
Exercise 4: Personal Workout Tracker

You've learned the building blocks: variables, lists, dictionaries, and loops.
Now it's time to organize your code with functions! Functions are like creating your
own custom exercises - you define them once, then use them whenever you need.

Concepts covered:
- Functions (defining reusable blocks of code)
- Function parameters (inputs)
- Return values (outputs)
- Function documentation
- Organizing code with functions

Learning Goals:
- Create functions to organize your code
- Pass data into functions using parameters
- Return calculated results from functions
- Build a workout tracking system using multiple functions

Run this exercise: uv run exercise/python/04_workout_tracker.py
"""

# ============================================================================
# QUICK INTRO: What are functions?
# ============================================================================
# A function is a named block of code that performs a specific task.
# Think of it like a gym routine - you define the routine once, then
# execute it whenever you want.
#
# Define a function:
#   def function_name(parameters):
#       # code here
#       return result
#
# Call a function:
#   result = function_name(arguments)


# ============================================================================
# EXAMPLE CODE
# ============================================================================
def calculate_volume(reps, weight):
    """
    Calculate the volume for a single set.

    Parameters:
        reps: Number of repetitions
        weight: Weight used in pounds

    Returns:
        The volume (reps × weight)
    """
    weight = 50
    volume = reps * weight
    return volume


def calculate_total_volume(reps_list, weights_list):
    """
    Calculate total volume across multiple sets.

    Parameters:
        reps_list: List of reps for each set
        weights_list: List of weights for each set

    Returns:
        Total volume across all sets
    """
    total = 0
    for i in range(len(reps_list)):
        set_volume = calculate_volume(reps_list[i], weights_list[i])
        total += set_volume
    return total


def display_workout_summary(exercise_name, reps_list, weights_list):
    """
    Display a formatted summary of a workout.

    This function doesn't return anything - it just prints output.
    """
    print(f"\n=== {exercise_name} Summary ===")
    print(f"Sets completed: {len(reps_list)}")
    print(f"Total reps: {sum(reps_list)}")

    total_vol = calculate_total_volume(reps_list, weights_list)
    print(f"Total volume: {total_vol} lbs")

    print("\nSet breakdown:")
    for i in range(len(reps_list)):
        set_num = i + 1
        print(f"  Set {set_num}: {reps_list[i]} reps × {weights_list[i]} lbs")


# Test the functions
print("=== Testing Functions ===")

# Call calculate_volume
set_volume = calculate_volume(10, 135)
print(f"Single set volume: {set_volume} lbs")

# Call calculate_total_volume
bench_reps = [10, 8, 8, 6]
bench_weights = [135, 155, 175, 185]
total = calculate_total_volume(bench_reps, bench_weights)
print(f"Total bench press volume: {total} lbs")

# Call display_workout_summary
display_workout_summary("Bench Press", bench_reps, bench_weights)


# ============================================================================
# YOUR TURN: TODO EXERCISES
# ============================================================================

print("\n\n=== YOUR WORKOUT TRACKER ===")

# TODO 1: Create a function to calculate one-rep max (1RM)
# The Brzycki formula for estimating 1RM is: weight × (36 / (37 - reps))
#
# Create a function called calculate_one_rep_max that takes two parameters:
# - weight: the weight lifted
# - reps: number of reps performed
#
# The function should return the estimated 1RM
#
# HINT: Use the formula above and return the result
#
# Stuck? Ask: "How do I create a function with parameters in Python?"
# Or: "What does the return keyword do?"

# Write your code here:

# TODO 2: Test your one_rep_max function
# Call your calculate_one_rep_max function with weight=225 and reps=5
# Store the result in a variable called estimated_max
# Print the result with a descriptive message
#
# Need help? Ask: "How do I call a function and use its return value?"

# Write your code here:


# TODO 3: Create a function to log a workout
# Create a function called log_workout that takes three parameters:
# - exercise_name: name of the exercise
# - sets: number of sets
# - reps: number of reps per set
#
# The function should print a message like:
# "Logged: 4 sets of 8 reps of Squats"
#
# This function doesn't need to return anything (it just prints)
#
# HINT: Use print() with an f-string inside the function
#
# Stuck? Ask: "How do I create a function that prints but doesn't return anything?"

# Write your code here:


# TODO 4: Test your log_workout function
# Call log_workout with:
# - exercise_name: "Deadlift"
# - sets: 5
# - reps: 5
#
# Need help? Ask: "How do I call a function with multiple arguments?"

# Write your code here:


# TODO 5: Create a function to calculate workout duration
# Create a function called calculate_workout_duration that takes:
# - num_sets: number of sets
# - rest_time: rest time between sets in seconds
# - work_time_per_set: time spent working per set in seconds
#
# Calculate total time: (num_sets × work_time_per_set) + ((num_sets - 1) × rest_time)
# Note: There's rest between sets, but not after the last set
#
# Return the total time in minutes (divide by 60)
#
# HINT: Do the calculation, then divide by 60 before returning
#
# Stuck? Ask: "How do I calculate total workout time with rest periods?"

# Write your code here:


# TODO 6: Test your workout duration function
# Call calculate_workout_duration with:
# - 5 sets
# - 90 seconds rest
# - 30 seconds work time per set
#
# Store the result and print how long the workout will take
#
# Need help? Ask: "Show me an example of calling a function with three parameters"

# Write your code here:


# ============================================================================
# BONUS CHALLENGES (Optional)
# ============================================================================

# BONUS 1: Create a workout comparison function
# Create a function called compare_workouts that takes two volume values
# and returns which one is higher (or if they're equal)
#
# Parameters: volume1, volume2
# Return: A string like "Workout 1 had higher volume" or "Equal volume"
#
# For help: Ask "How do I compare two values and return different strings?"

# Write your code here:


# BONUS 2: Create a comprehensive workout report function
# Create a function called generate_workout_report that takes:
# - exercise_name, reps_list, weights_list
#
# The function should:
# 1. Calculate and display total volume
# 2. Calculate and display average reps
# 3. Find and display the heaviest weight used
# 4. Estimate the 1RM from the first set
#
# Want guidance? Ask: "How do I create a function that does multiple calculations?"

# Write your code here:


# BONUS 3: Create a rest recommendation function
# Create a function called recommend_rest_time that takes a weight parameter
# and returns recommended rest time in seconds:
# - Light weight (< 135 lbs): 60 seconds
# - Medium weight (135-225 lbs): 90 seconds
# - Heavy weight (> 225 lbs): 180 seconds
#
# Need help? Ask: "How do I use if/elif/else in a function?"

# Write your code here:


# ============================================================================
# TESTING YOUR CODE
# ============================================================================

# Test cases for your functions:
#
# calculate_one_rep_max(225, 5) should return approximately 258.75
# log_workout("Deadlift", 5, 5) should print "Logged: 5 sets of 5 reps of Deadlift"
# calculate_workout_duration(5, 90, 30) should return approximately 8.5 minutes
#
# If your functions aren't working as expected:
# - Check that you're using the correct parameter names
# - Make sure you're returning values (not just printing them) when needed
# - Verify your math in the calculations
#
# Ask me: "Can you help me debug my function?"


if __name__ == "__main__":
    # You can add test calls here to run when the file executes
    pass
