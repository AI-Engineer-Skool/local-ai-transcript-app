"""
Exercise 2: Multiple Sets Tracking

Now that you can track a single piece of information, let's level up! In real workouts,
you perform multiple sets, and each set might have different reps or weights. We need
a way to store multiple values - that's where lists come in!

Concepts covered:
- Lists (storing multiple values in one variable)
- Loops (repeating actions for each item in a list)
- List methods (append, sum, len)
- Iterating with for loops

Learning Goals:
- Create and use lists to store multiple values
- Use loops to process each item in a list
- Perform calculations on list data
- Track sets in a real workout scenario

Run this exercise: uv run exercise/python/02_workout_sets.py
"""

# ============================================================================
# QUICK INTRO: What are lists?
# ============================================================================
# A list is like a workout card that tracks multiple sets. Instead of one number,
# you can store many numbers in order.
#
# Create a list using square brackets: [item1, item2, item3]
# Access items by position (starting at 0): my_list[0] gets the first item


# ============================================================================
# EXAMPLE CODE
# ============================================================================

# Let's track multiple sets of an exercise
exercise = "Deadlift"

# A list of reps for each set
reps_per_set = [5, 5, 5, 5, 5]  # 5 sets of 5 reps

# A list of weights for each set (progressive overload!)
weights = [135, 185, 225, 275, 315]  # increasing weight each set

print("=== Workout Session ===")
print(f"Exercise: {exercise}")
print(f"Number of sets: {len(reps_per_set)}")  # len() gives us the length
print()

# We can access individual sets using their index (position)
print("First set:", reps_per_set[0], "reps at", weights[0], "lbs")
print(
    "Last set:", reps_per_set[-1], "reps at", weights[-1], "lbs"
)  # -1 means last item
print()

# FOR LOOPS: Repeat an action for each item in a list
print("Set-by-set breakdown:")
for i in range(len(reps_per_set)):
    set_number = i + 1  # Add 1 because sets start at 1, not 0
    print(f"  Set {set_number}: {reps_per_set[i]} reps × {weights[i]} lbs")

print()

# Calculate totals
total_reps = sum(reps_per_set)  # sum() adds all numbers in a list
print(f"Total reps: {total_reps}")

# Calculate total volume (reps × weight for each set, then sum)
total_volume = 0
for i in range(len(reps_per_set)):
    set_volume = reps_per_set[i] * weights[i]
    total_volume += set_volume  # += means "add to the current value"

print(f"Total volume: {total_volume} lbs")

# Another way to loop: directly over the items (when you don't need the index)
print("\nWeight progression:")
for weight in weights:
    print(f"  → {weight} lbs")


# ============================================================================
# YOUR TURN: TODO EXERCISES
# ============================================================================

print("\n=== YOUR WORKOUT ===")

# TODO 1: Create lists for a squat workout
# Create two lists:
# - squat_reps: [8, 8, 8, 6] (4 sets, last one fewer reps)
# - squat_weights: [135, 185, 225, 245] (increasing weight)
#
# Then print how many sets you'll do using len()
#
# Stuck? Ask: "How do I create a list in Python?"
# Or: "What does len() do?"

# Write your code here:

# TODO 2: Print each set with its details
# Use a for loop with range() to print each set number, reps, and weight
# Format: "Set 1: 8 reps × 135 lbs"
#
# HINT: Use range(len(squat_reps)) to get indices 0, 1, 2, 3
# HINT: Add 1 to the index to display set numbers starting from 1
#
# Need help? Ask: "How do I loop through a list with indices in Python?"
# Or: "Show me an example of using range() with len()"

# Write your code here:

# TODO 3: Calculate and display total reps
# Use the sum() function to calculate the total reps across all sets
# Store it in a variable called total_squat_reps and print it
#
# Stuck? Ask: "How do I use the sum() function in Python?"

# Write your code here:

# TODO 4: Calculate total volume
# Create a variable called total_squat_volume and set it to 0
# Use a for loop to go through each set and add (reps × weight) to the total
# Then print the total volume
#
# HINT: Use the += operator to add to a running total
# HINT: Access both lists using the same index: squat_reps[i] * squat_weights[i]
#
# Need help? Ask: "How do I calculate a running total in a loop?"
# Or: "What does the += operator do?"

# Write your code here:


# TODO 5: Find your heaviest set
# Use the max() function to find the heaviest weight you lifted
# Store it in a variable called max_weight and print it with a message
#
# HINT: max(squat_weights) returns the largest number in the list
#
# Stuck? Ask: "How do I find the maximum value in a list?"

# Write your code here:

# ============================================================================
# BONUS CHALLENGES (Optional)
# ============================================================================

# BONUS 1: Add a new set
# Sometimes you feel strong and want to add another set!
# Use the .append() method to add one more set to both lists:
# - Add 5 reps to squat_reps
# - Add 265 to squat_weights
# Then print the updated lists
#
# For help: Ask "How do I add an item to a list in Python?"

# Write your code here:

# BONUS 2: Calculate average weight
# Calculate the average weight used across all sets
# (Hint: sum of weights divided by number of sets)
# Store it in avg_weight and print it
#
# Need help? Ask: "How do I calculate an average in Python?"

# Write your code here:

# BONUS 3: Track workout intensity
# Create a list called intensity where each value is reps × weight for that set
# This represents how hard each set was. Then print the list.
#
# HINT: Use a for loop to calculate each set's intensity and .append() it to the list
#
# Want guidance? Ask: "How do I create a new list from calculations on two other lists?"

# Write your code here:


# ============================================================================
# TESTING YOUR CODE
# ============================================================================

# Expected output should include:
# - A list of 4 sets with reps [8, 8, 8, 6]
# - Weights [135, 185, 225, 245]
# - Each set printed in format "Set X: Y reps × Z lbs"
# - Total reps: 30
# - Total volume: 6110 lbs
# - Max weight: 245 lbs
#
# If your calculations don't match, check your loop and math operations!
# Ask me: "Why is my total different from expected?"


if __name__ == "__main__":
    pass
