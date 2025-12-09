/**
 * Exercise 1: Gym Basics with Types
 *
 * Welcome to TypeScript! If you've completed the Python exercises, you already know
 * the basics of programming. TypeScript adds TYPE SAFETY - the compiler checks your
 * code for type errors before you even run it! This catches bugs early.
 *
 * Key difference from Python: TypeScript has STATIC TYPING - you can (and often should)
 * declare what type each variable is. But TypeScript is also smart - it can INFER types!
 *
 * Concepts covered:
 * - Variables with type annotations (explicit types)
 * - Type inference (TypeScript figures out the type)
 * - Basic types: string, number, boolean
 * - Template literals for string formatting
 * - Understanding that TypeScript enforces types with BOTH approaches
 *
 * Run this exercise: node exercise/typescript/01_gym_basics.ts
 */

// ============================================================================
// QUICK INTRO: Types in TypeScript
// ============================================================================
// TypeScript has two ways to work with types:
//
// 1. EXPLICIT TYPE ANNOTATIONS - You tell TypeScript the type:
//    let name: string = "Bench Press";
//
// 2. TYPE INFERENCE - TypeScript figures it out:
//    let reps = 10;  // TypeScript knows this is a number!
//
// IMPORTANT: Even with inference, TypeScript ENFORCES the type!
// Try this and you'll get an error: let count = 5; count = "five"; // ERROR!
//
// For learning, we'll show BOTH approaches. In real code, you can use
// inference for simple cases and explicit types when you want to be clear.

// ============================================================================
// EXAMPLE CODE
// ============================================================================

// Explicit type annotations (clear and self-documenting)
const exerciseName: string = "Bench Press";
const muscleGroup: string = "Chest";

// Type inference (TypeScript infers the types)
const setsCompleted = 3; // TypeScript infers: number
const repsPerSet = 10; // TypeScript infers: number
const weightUsed = 135.5; // TypeScript infers: number

// Both approaches give you TYPE SAFETY!
// Uncomment this line to see TypeScript catch an error:
// setsCompleted = "three"; // ERROR! Can't assign string to number

console.log("=== Workout Log ===");
console.log("Exercise:", exerciseName);
console.log("Target:", muscleGroup);
console.log("Sets:", setsCompleted);
console.log("Reps per set:", repsPerSet);
console.log("Weight:", weightUsed, "lbs");

// Math works the same as Python
const totalReps: number = setsCompleted * repsPerSet;
console.log("Total reps:", totalReps);

// Template literals are like Python f-strings (use backticks ` and ${})
const summary = `You completed ${totalReps} reps of ${exerciseName} at ${weightUsed} lbs!`;
console.log(summary);

// Demonstrating type safety with inference
let isWarmupComplete = true; // Inferred as boolean
console.log("Warmup complete?", isWarmupComplete);
// isWarmupComplete = "yes"; // ERROR! TypeScript knows it's a boolean

// ============================================================================
// YOUR TURN: TODO EXERCISES
// ============================================================================

console.log("\n=== YOUR WORKOUT LOG ===");

// TODO 1: Create variables for YOUR workout using EXPLICIT type annotations
// Create variables with EXPLICIT types for a squat workout:
// - squatExercise: string = "Squat"
// - squatMuscle: string = "Legs"
// - squatSets: number = 4
// - squatReps: number = 8
// - squatWeight: number = 185.0
//
// Type hint: The pattern is: const variableName: type = value;
//
// Stuck? Ask: "How do I declare a variable with a type annotation in TypeScript?"

// Write your code here:

// TODO 2: Now try using TYPE INFERENCE
// Create similar variables but WITHOUT type annotations (let TypeScript infer):
// - Use names like: inferredExercise, inferredMuscle, inferredSets, inferredReps, inferredWeight
// - Assign similar values (you choose the exercise!)
// - Hover over them in your editor to see the inferred types!
//
// Type hint: Without annotations: const variableName = value;
// TypeScript will still know the types and enforce them!
//
// Experiment: Try assigning a string to one of these inferred number variables
// and see TypeScript catch the error!
//
// Need help? Ask: "What's the difference between explicit types and type inference?"

// Write your code here:

// TODO 3: Calculate and display total reps with explicit types
// Create a variable totalSquatReps with an explicit number type
// Calculate: squatSets × squatReps (using your variables from TODO 1)
// Print it with console.log()
//
// Type hint: const totalSquatReps: number = ...
//
// Stuck? Ask: "How do I do arithmetic in TypeScript?"

// Write your code here:

// TODO 4: Create a summary using a template literal
// Create a workoutSummary variable (you choose: explicit type or inference!)
// Use a template literal (backticks and ${}) to create a message like:
// "Today I did 32 reps of Squats at 185.0 lbs targeting my Legs!"
//
// Type hint: Template literals use backticks ` and ${variable} for interpolation
//
// Need help? Ask: "How do I use template literals in TypeScript?"

// Write your code here:

// TODO 5: Track rest time and calculate total rest in minutes
// Create a restSeconds variable (number type - your choice on explicit vs inference)
// Set it to 90 seconds
// Calculate total rest in minutes: (restSeconds × setsCompleted) / 60
// Store in totalRestMinutes variable
// Print it
//
// Type challenge: What type is totalRestMinutes? Hover to see!
//
// Stuck? Ask: "How do I convert seconds to minutes in TypeScript?"

// Write your code here:

// ============================================================================
// BONUS CHALLENGES (Optional)
// ============================================================================

// BONUS 1: Calculate total volume with explicit typing
// Create a totalVolume variable with explicit number type
// Calculate: setsCompleted × repsPerSet × weightUsed
// Print a message about the volume
//
// Type hint: This is your workout "volume" in fitness terms!
//
// For help: Ask "How do I calculate workout volume in TypeScript?"

// Write your code here:

// BONUS 2: Experiment with type errors
// Try creating a variable with type inference, then try to assign a wrong type:
// let active = true;
// active = "yes"; // This should show a TypeScript error!
//
// This demonstrates that TypeScript enforces types EVEN WITH INFERENCE.
// Comment out the error after you see it.
//
// Want to learn more? Ask: "Why does TypeScript show type errors?"

// Write your code here:

// BONUS 3: Create a complete workout report with mixed typing
// Use a combination of explicit types and inference to create variables for:
// - Exercise name, muscle group, sets, reps, weight
// - Calculated: total reps, total volume, rest time
// Then use template literals to create a nice formatted multi-line report
// Use console.log() with \n for line breaks or multiple console.log() calls
//
// Get creative! Ask: "Show me how to format multi-line output in TypeScript"

// Write your code here:

// ============================================================================
// TESTING YOUR CODE
// ============================================================================

// When you run this file with: node exercise/typescript/01_gym_basics.ts
//
// You should see:
// - The example workout log output
// - Your workout log with squat information
// - Calculated values (total reps, rest minutes, volume)
// - Your summary messages
//
// If you see TypeScript errors (red squiggly lines in your editor):
// - Read the error message carefully - it tells you what type was expected
// - Check that you're using the right type (string, number, boolean)
// - Make sure you're not mixing types (like assigning a string to a number)
//
// Ask me: "I got a TypeScript error, what does it mean?"
//
// Key learning: TypeScript catches errors BEFORE you run the code!
// This is the power of static typing.
