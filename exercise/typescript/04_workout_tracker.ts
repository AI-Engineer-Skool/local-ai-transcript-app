/**
 * Exercise 4: Personal Workout Tracker with Typed Functions
 *
 * You've mastered types, arrays, and interfaces. Now let's organize code with FUNCTIONS!
 * In TypeScript, functions have types too - for parameters AND return values.
 * This makes your functions self-documenting and catches errors when you pass wrong data.
 *
 * IMPORTANT: Function parameters MUST have explicit types (inference doesn't work here).
 * Return types CAN be inferred, but explicit types make code clearer.
 *
 * Concepts covered:
 * - Function parameter types (required!)
 * - Function return types
 * - Void return type (for functions that don't return)
 * - Optional parameters
 * - Function type annotations
 * - Type safety in function calls
 *
 * Run this exercise: node exercise/typescript/04_workout_tracker.ts
 */

// ============================================================================
// QUICK INTRO: Typed Functions
// ============================================================================
// In TypeScript, functions need types for parameters and (optionally) return values:
//
//   function add(a: number, b: number): number {
//     return a + b;
//   }
//
// - Parameters: MUST have explicit types (a: number, b: number)
// - Return type: Optional but recommended (: number)
//
// TypeScript checks:
// - You pass the right types when calling
// - The function returns the declared type
// - All code paths return a value (if return type is not void)

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

// We can define the type of a function itself!
type VolumeCalculator = (reps: number, weight: number) => number;

// ============================================================================
// EXAMPLE CODE
// ============================================================================

/**
 * Calculate volume for a single set.
 *
 * @param reps - Number of repetitions
 * @param weight - Weight in pounds
 * @returns The volume (reps × weight)
 */
function calculateVolume(reps: number, weight: number): number {
  const volume = reps * weight;
  return volume;
}

/**
 * Calculate total volume across multiple sets.
 */
function calculateTotalVolume(reps: number[], weights: number[]): number {
  let total = 0;
  for (let i = 0; i < reps.length; i++) {
    total += calculateVolume(reps[i], weights[i]);
  }
  return total;
}

/**
 * Display a workout summary (no return value).
 * The void return type means this function doesn't return anything.
 */
function displayWorkoutSummary(
  exerciseName: string,
  reps: number[],
  weights: number[]
): void {
  console.log(`\n=== ${exerciseName} Summary ===`);
  console.log(`Sets completed: ${reps.length}`);
  console.log(`Total reps: ${reps.reduce((sum, r) => sum + r, 0)}`);

  const totalVol = calculateTotalVolume(reps, weights);
  console.log(`Total volume: ${totalVol} lbs`);

  console.log("\nSet breakdown:");
  for (let i = 0; i < reps.length; i++) {
    console.log(`  Set ${i + 1}: ${reps[i]} reps × ${weights[i]} lbs`);
  }
}

/**
 * Function with optional parameter (uses ?)
 */
function logWorkout(exercise: string, sets: number, reps?: number): void {
  if (reps !== undefined) {
    console.log(`Logged: ${sets} sets of ${reps} reps of ${exercise}`);
  } else {
    console.log(`Logged: ${sets} sets of ${exercise}`);
  }
}

// Test the functions
console.log("=== Testing Functions ===");

// TypeScript checks the parameter types!
const setVolume = calculateVolume(10, 135);
console.log(`Single set volume: ${setVolume} lbs`);

// Try uncommenting this to see a type error:
// calculateVolume("10", 135); // ERROR! String is not assignable to number

const benchReps = [10, 8, 8, 6];
const benchWeights = [135, 155, 175, 185];
const total = calculateTotalVolume(benchReps, benchWeights);
console.log(`Total volume: ${total} lbs`);

displayWorkoutSummary("Bench Press", benchReps, benchWeights);

console.log();
logWorkout("Squats", 5, 5); // With reps
logWorkout("Plank", 3); // Without reps (optional)

// ============================================================================
// YOUR TURN: TODO EXERCISES
// ============================================================================

console.log("\n\n=== YOUR WORKOUT TRACKER ===");

// TODO 1: Create a function to calculate one-rep max
// The Brzycki formula: weight × (36 / (37 - reps))
//
// Create a function called calculateOneRepMax with:
// - Parameters: weight (number), reps (number)
// - Return type: number
// - Calculate and return the estimated 1RM
//
// Type hint: function name(param: type, param: type): returnType { }
//
// Stuck? Ask: "How do I create a function with typed parameters in TypeScript?"

// Write your code here:

// TODO 2: Test your calculateOneRepMax function
// Call your function with weight=225, reps=5
// Store the result in a variable with explicit type: number
// Print the result with a message
//
// Type hint: const result: number = functionName(arg1, arg2);
//
// Need help? Ask: "How do I call a typed function in TypeScript?"

// Write your code here:

// TODO 3: Create a function with void return type
// Create a function called logWorkoutSession that:
// - Parameters: exerciseName (string), sets (number), reps (number)
// - Return type: void (doesn't return anything, just prints)
// - Prints: "Logged: X sets of Y reps of ExerciseName"
//
// Type hint: Functions that only print should return void
//
// Stuck? Ask: "What does void mean in TypeScript?"

// Write your code here:

// TODO 4: Test your logWorkoutSession function
// Call it with: "Deadlift", 5, 5
// Then call it again with different values
//
// Type challenge: Try passing wrong types and see TypeScript catch it!
//
// Need help? Ask: "How do I call a function that returns void?"

// Write your code here:

// TODO 5: Create a function to calculate workout duration
// Create a function called calculateWorkoutDuration with:
// - Parameters: numSets (number), restTime (number), workTimePerSet (number)
// - Return type: number
// - Calculate: (numSets × workTimePerSet) + ((numSets - 1) × restTime)
// - Return the result in MINUTES (divide by 60)
//
// Type hint: There's rest between sets but not after the last set
//
// Stuck? Ask: "How do I create a function that does calculations and returns a value?"

// Write your code here:

// TODO 6: Test workout duration function with explicit typing
// Call calculateWorkoutDuration with: 5 sets, 90 seconds rest, 30 seconds work
// Store result in a variable with explicit number type
// Print how long the workout will take
//
// Type hint: const duration: number = ...
//
// Need help? Ask: "How do I store and use a function's return value?"

// Write your code here:

// TODO 7: Create a function with optional parameters
// Create a function called trackWorkout with:
// - Required params: exerciseName (string), sets (number)
// - Optional param: notes (string) - use ? to make it optional
// - Return type: void
// - If notes provided, print: "ExerciseName: X sets - Notes"
// - If no notes, print: "ExerciseName: X sets"
//
// HINT: Use ? after parameter name to make it optional
// HINT: Check if optional param exists: if (notes !== undefined) { }
//
// Stuck? Ask: "How do I create a function with optional parameters in TypeScript?"

// Write your code here:

// TODO 8: Test the optional parameter function
// Call trackWorkout twice:
// 1. With notes: "Bench Press", 3, "Felt strong today"
// 2. Without notes: "Squats", 4
//
// Type hint: Optional parameters can be omitted in the call
//
// Need help? Ask: "How do I call a function with optional parameters?"

// Write your code here:

// ============================================================================
// BONUS CHALLENGES (Optional)
// ============================================================================

// BONUS 1: Create a function that returns an object
// Create a function called analyzeWorkout that takes:
// - reps: number[]
// - weights: number[]
// Returns an object with:
// - totalReps: number
// - totalVolume: number
// - averageWeight: number
// - maxWeight: number
//
// Type hint: You can specify return type as an object:
// function name(): { prop1: type, prop2: type } { }
// OR create an interface for the return type!
//
// For help: Ask "How do I create a function that returns an object in TypeScript?"

// Write your code here:

// BONUS 2: Create a function with a union type parameter
// Create a function called formatWeight that takes:
// - weight: number | string (can be either!)
// - Returns: string
// If weight is a number, return: "X lbs"
// If weight is a string, return: weight (as-is)
//
// HINT: Use typeof to check type: if (typeof weight === "number")
//
// Want guidance? Ask: "How do I use union types in function parameters?"

// Write your code here:

// BONUS 3: Create a higher-order function
// Create a function called createVolumeCalculator that:
// - Takes a multiplier: number
// - Returns a FUNCTION that calculates volume with that multiplier
// - The returned function signature: (reps: number, weight: number) => number
//
// This is advanced! Functions can return functions!
//
// HINT:
// function createCalculator(mult: number): (r: number, w: number) => number {
//   return (reps, weight) => reps * weight * mult;
// }
//
// Need help? Ask: "What are higher-order functions in TypeScript?"

// Write your code here:

// ============================================================================
// TESTING YOUR CODE
// ============================================================================

// Expected behavior:
// - calculateOneRepMax(225, 5) ≈ 258.75
// - logWorkoutSession prints formatted workout logs
// - calculateWorkoutDuration(5, 90, 30) ≈ 8.5 minutes
// - trackWorkout works with and without optional notes parameter
//
// TypeScript ensures:
// - You can't pass wrong types to functions
// - Functions return the declared type
// - Required parameters are always provided
// - Optional parameters work correctly
//
// Key learning points:
// - Parameter types are REQUIRED (can't be inferred)
// - Return types are optional but recommended for clarity
// - void means "no return value"
// - Optional parameters use ? and can be omitted
// - TypeScript checks function calls for type correctness
//
// If you get type errors:
// - Check parameter types match when calling
// - Verify return type matches what you're returning
// - Ensure all code paths return a value (unless void)
// - Check optional parameter usage
//
// Ask me: "Why is TypeScript showing an error in my function?"
