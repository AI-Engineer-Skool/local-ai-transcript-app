"""
Exercise 3: Exercise Library

You've learned about lists for storing multiple items. But what if you need to store
related information together? Like an exercise with its muscle group, equipment, and
difficulty? That's where dictionaries come in - they store data in key-value pairs!

Concepts covered:
- Dictionaries (storing related data with keys and values)
- Nested dictionaries (dictionaries containing other dictionaries)
- Accessing dictionary values
- Iterating over dictionaries
- Dictionary methods (keys(), values(), items())

Learning Goals:
- Understand how to organize related data with dictionaries
- Create and access dictionary values
- Build a library of exercises with their properties
- Loop through dictionary data

Run this exercise: uv run exercise/python/03_exercise_library.py
"""

# ============================================================================
# QUICK INTRO: What are dictionaries?
# ============================================================================
# A dictionary is like a gym equipment card that stores multiple pieces of
# information about one thing. Instead of positions (like lists), you use
# descriptive keys to access values.
#
# Create a dictionary: {"key1": value1, "key2": value2}
# Access values: my_dict["key1"]
#
# Think of it like a real dictionary: you look up a word (key) to find its
# definition (value).


# ============================================================================
# EXAMPLE CODE
# ============================================================================

# Let's create a dictionary for one exercise
bench_press = {
    "name": "Bench Press",
    "muscle_group": "Chest",
    "equipment": "Barbell",
    "difficulty": "Intermediate",
}

print("=== Single Exercise ===")
print(f"Exercise: {bench_press['name']}")
print(f"Targets: {bench_press['muscle_group']}")
print(f"Equipment needed: {bench_press['equipment']}")
print(f"Difficulty: {bench_press['difficulty']}")
print()

# We can modify values
bench_press["difficulty"] = "Beginner"  # Changed our mind!
print(f"Updated difficulty: {bench_press['difficulty']}")
print(bench_press)

# Now let's create a library of multiple exercises
# This is a dictionary where each key is an exercise name, and each value is another dictionary
exercise_library = {
    "bench_press": {
        "name": "Bench Press",
        "muscle_group": "Chest",
        "equipment": "Barbell",
        "difficulty": "Intermediate",
    },
    "squat": {
        "name": "Squat",
        "muscle_group": "Legs",
        "equipment": "Rack",
        "difficulty": "Intermediate",
    },
    "pull_up": {
        "name": "Pull Up",
        "muscle_group": "Back",
        "equipment": "Pull-up Bar",
        "difficulty": "Advanced",
    },
}

print("=== Exercise Library ===")
print(f"Total exercises: {len(exercise_library)}")
print()

# Access a specific exercise
print("Looking up squat info:")
squat_info = exercise_library["squat"]
print(f"  Name: {squat_info['name']}")
print(f"  Targets: {squat_info['muscle_group']}")
print()

# Loop through all exercises
print("All exercises in library:")
for exercise_key, exercise_data in exercise_library.items():
    print(
        f"  → {exercise_data['name']} - {exercise_data['muscle_group']} ({exercise_data['difficulty']})"
    )

print()

# We can also get all muscle groups
print("Muscle groups covered:")
for exercise_data in exercise_library.values():
    print(f"  - {exercise_data['muscle_group']}")


# ============================================================================
# YOUR TURN: TODO EXERCISES
# ============================================================================

# print("\n=== YOUR EXERCISE LIBRARY ===")

# TODO 1: Create a dictionary for a deadlift
# Create a dictionary called deadlift with these keys and values:
# - "name": "Deadlift"
# - "muscle_group": "Back"
# - "equipment": "Barbell"
# - "difficulty": "Advanced"
#
# Then print each piece of information using dictionary access (deadlift["key"])
#
# Stuck? Ask: "How do I create a dictionary in Python?"
# Or: "How do I access dictionary values?"

# Write your code here:


# TODO 2: Add the deadlift to the exercise library
# Add your deadlift dictionary to the exercise_library using the key "deadlift"
#
# HINT: Use assignment like: exercise_library["deadlift"] = deadlift
#
# Then print the total number of exercises in the library
#
# Need help? Ask: "How do I add a new key-value pair to a dictionary?"

# Write your code here:


# TODO 3: Create a dictionary for a shoulder press
# Create a dictionary called shoulder_press with:
# - "name": "Overhead Press"
# - "muscle_group": "Shoulders"
# - "equipment": "Barbell"
# - "difficulty": "Intermediate"
#
# Add it directly to the exercise_library with the key "shoulder_press"
# (You can do this in one step without creating a separate variable first)
#
# Stuck? Ask: "Can I create and add a dictionary in one line?"

# Write your code here:


# TODO 4: Print all exercise names
# Use a for loop to iterate through exercise_library and print just the name
# of each exercise in the library.
#
# HINT: Use .values() to loop through the exercise dictionaries
# Format: "- Exercise Name"
#
# Need help? Ask: "How do I loop through dictionary values in Python?"

# Write your code here:


# TODO 5: Find all chest exercises
# Loop through the exercise_library and print the names of exercises
# where the muscle_group is "Chest"
#
# HINT: Use an if statement inside your loop to check the muscle_group
# Format: "Chest exercise: Exercise Name"
#
# Stuck? Ask: "How do I filter dictionary items based on a condition?"
# Or: "Show me an if statement inside a for loop"

# Write your code here:


# ============================================================================
# BONUS CHALLENGES (Optional)
# ============================================================================

# BONUS 1: Count exercises by difficulty
# Create a new dictionary called difficulty_count with keys "Beginner",
# "Intermediate", and "Advanced", each starting at 0.
# Loop through exercise_library and count how many exercises are at each difficulty.
# Print the results.
#
# For help: Ask "How do I count occurrences of values in a dictionary?"

# Write your code here:


# BONUS 2: Add a new property to all exercises
# Add a new key "favorite" to each exercise in the library, set to False initially.
# Then set your favorite exercise's "favorite" key to True.
# Print all exercises showing their favorite status.
#
# Want guidance? Ask: "How do I add a new key to existing dictionaries in a loop?"

# Write your code here:


# BONUS 3: Create an equipment list
# Create a list of all unique equipment types used in your exercise library.
# (Hint: Use a set to automatically remove duplicates, then convert to a list)
# Print the list of equipment.
#
# Need help? Ask: "How do I get unique values from dictionary data?"

# Write your code here:


# ============================================================================
# TESTING YOUR CODE
# ============================================================================

# Expected output should include:
# - Deadlift dictionary created with all 4 keys
# - Exercise library now has 5 exercises (original 3 + deadlift + shoulder press)
# - List of all exercise names printed
# - Only "Bench Press" shown when filtering for chest exercises
#
# To verify: print(len(exercise_library)) should show 5
# To debug: print(exercise_library) to see the entire library


if __name__ == "__main__":
    pass
