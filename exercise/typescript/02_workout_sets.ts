/**
 * Exercise 2: Multiple Sets Tracking with Typed Arrays
 *
 * Now that you understand TypeScript's type system, let's work with ARRAYS.
 * In TypeScript, arrays have types too! An array can hold numbers, strings, etc.
 * TypeScript makes sure you don't accidentally mix types (unless you want to).
 *
 * Concepts covered:
 * - Typed arrays (number[], string[], etc.)
 * - Array type inference
 * - For loops with proper typing
 * - Array methods (reduce, map, filter)
 * - Type safety with arrays
 *
 * Run this exercise: node exercise/typescript/02_workout_sets.ts
 */

// ============================================================================
// QUICK INTRO: Typed Arrays
// ============================================================================
// In TypeScript, arrays have types:
//   let numbers: number[] = [1, 2, 3];        // Explicit: array of numbers
//   let names = ["Alice", "Bob"];             // Inferred: string[]
//
// TypeScript enforces the array type:
//   numbers.push(4);     // ✓ OK
//   numbers.push("5");   // ✗ ERROR! Can't add string to number[]
//
// This catches bugs early! If you expect numbers, TypeScript ensures you get numbers.

// ============================================================================
// EXAMPLE CODE
// ============================================================================

const exercise: string = "Deadlift";

// Explicit array types
const repsPerSet: number[] = [5, 5, 5, 5, 5]; // Array of numbers
const weights: number[] = [135, 185, 225, 275, 315];

// Type inference for arrays
const setNotes = [
  "Felt strong",
  "Good form",
  "PR attempt!",
  "Success!",
  "Max effort",
];
// Hover over setNotes - TypeScript inferred: string[]

console.log("=== Workout Session ===");
console.log(`Exercise: ${exercise}`);
console.log(`Number of sets: ${repsPerSet.length}`);
console.log();

// Accessing array elements (same as Python, 0-indexed)
console.log(`First set: ${repsPerSet[0]} reps at ${weights[0]} lbs`);
console.log(
  `Last set: ${repsPerSet[repsPerSet.length - 1]} reps at ${
    weights[weights.length - 1]
  } lbs`
);
console.log();

// For loop with proper typing
console.log("Set-by-set breakdown:");
for (let i = 0; i < repsPerSet.length; i++) {
  const setNumber: number = i + 1;
  console.log(`  Set ${setNumber}: ${repsPerSet[i]} reps × ${weights[i]} lbs`);
}
console.log();

// Calculate totals using reduce (a functional approach)
const totalReps: number = repsPerSet.reduce((sum, reps) => sum + reps, 0);
console.log(`Total reps: ${totalReps}`);

// Calculate volume with reduce
const totalVolume: number = repsPerSet.reduce((sum, reps, index) => {
  return sum + reps * weights[index];
}, 0);
console.log(`Total volume: ${totalVolume} lbs`);

// For...of loop (when you don't need the index)
console.log("\nWeight progression:");
for (const weight of weights) {
  // TypeScript knows weight is a number!
  console.log(`  → ${weight} lbs`);
}

// Demonstrate type safety
// Uncomment to see TypeScript catch the error:
// repsPerSet.push("ten"); // ERROR! Can't add string to number[]

// ============================================================================
// YOUR TURN: TODO EXERCISES
// ============================================================================

console.log("\n=== YOUR WORKOUT ===");

// TODO 1: Create typed arrays for a squat workout
// Create two arrays with EXPLICIT types:
// - squatReps: number[] = [8, 8, 8, 6]
// - squatWeights: number[] = [135, 185, 225, 245]
//
// Then print how many sets you'll do using .length
//
// Type hint: arrayName: type[] = [values]
//
// Stuck? Ask: "How do I create a typed array in TypeScript?"

// Write your code here:

// TODO 2: Create arrays using type inference
// Create the same arrays but let TypeScript INFER the types:
// - Use different names like: squatRepsInferred, squatWeightsInferred
// - Assign the same values without type annotations
// - Hover over them to see TypeScript inferred the types!
//
// Type challenge: Even though you didn't write ': number[]', TypeScript
// still won't let you add a string! Try it and see the error.
//
// Need help? Ask: "How does TypeScript infer array types?"

// Write your code here:

// TODO 3: Print each set with a for loop
// Use a for loop with index to print each set:
// Format: "Set 1: 8 reps × 135 lbs"
//
// Type hint: for (let i: number = 0; i < array.length; i++)
// Or let TypeScript infer i's type: for (let i = 0; ...)
//
// Stuck? Ask: "How do I loop through an array with an index in TypeScript?"

// Write your code here:

// TODO 4: Calculate total reps using reduce
// Use the reduce method to sum all reps
// Store in totalSquatReps (choose: explicit type or inference)
//
// HINT: array.reduce((accumulator, currentValue) => accumulator + currentValue, 0)
//
// Type hint: TypeScript knows reduce returns a number when you start with 0!
//
// Need help? Ask: "How do I use reduce to sum an array in TypeScript?"

// Write your code here:

// TODO 5: Calculate total volume
// Use reduce to calculate volume (sum of reps × weight for each set)
// HINT: You need to access both arrays using the index parameter
// reduce provides: (accumulator, currentValue, currentIndex)
//
// Type hint: squatReps.reduce((sum, reps, index) => sum + reps * squatWeights[index], 0)
//
// Stuck? Ask: "How do I use reduce with two arrays in TypeScript?"

// Write your code here:

// TODO 6: Find the maximum weight using Math.max
// Use Math.max() with the spread operator (...) to find max weight
// HINT: Math.max(...array) spreads the array into individual arguments
//
// Store in maxWeight and print it
//
// Type challenge: What type does Math.max return? Hover to see!
//
// Need help? Ask: "How do I find the maximum value in an array in TypeScript?"

// Write your code here:

// ============================================================================
// BONUS CHALLENGES (Optional)
// ============================================================================

// BONUS 1: Add a new set with type safety
// Use .push() to add one more set to both arrays:
// - Add 5 to squatReps
// - Add 265 to squatWeights
//
// Then try adding a string and watch TypeScript catch the error!
// (Comment out the error after seeing it)
//
// For help: Ask "How do I add elements to a typed array?"

// Write your code here:

// BONUS 2: Calculate average weight with proper typing
// Calculate the average weight: sum of all weights / number of sets
// Use reduce to sum, then divide by length
// Store in a variable with explicit number type
//
// Type hint: const avgWeight: number = ...
//
// Need help? Ask: "How do I calculate the average of an array in TypeScript?"

// Write your code here:

// BONUS 3: Create an intensity array using map
// Use the .map() method to create a new array where each element is reps × weight
// This represents the intensity of each set
//
// HINT: squatReps.map((reps, index) => reps * squatWeights[index])
//
// Type challenge: What type does map return? Hover over the result!
// TypeScript knows it's number[] !
//
// Want guidance? Ask: "How do I use map to create a new array in TypeScript?"

// Write your code here:

// BONUS 4: Filter heavy sets
// Use .filter() to create an array of only the sets where weight >= 200 lbs
// HINT: squatWeights.filter(weight => weight >= 200)
//
// Type challenge: The filtered array is still number[] - TypeScript preserves the type!
//
// Need help? Ask: "How do I filter an array in TypeScript?"

// Write your code here:

// ============================================================================
// TESTING YOUR CODE
// ============================================================================

// Expected output:
// - Arrays created with [8, 8, 8, 6] reps and [135, 185, 225, 245] weights
// - Each set printed with format "Set X: Y reps × Z lbs"
// - Total reps: 30
// - Total volume: 6110 lbs
// - Max weight: 245 lbs
//
// Key TypeScript features demonstrated:
// - Typed arrays ensure you only add the right type of data
// - Array methods (reduce, map, filter) work with types
// - TypeScript infers types from array literals
// - Type safety prevents mixing types accidentally
//
// If you get type errors:
// - Check that all values in an array are the same type
// - Make sure you're not trying to add wrong types with push()
// - Verify your array type annotations match the data
//
// Ask me: "Why am I getting a type error in my array?"
