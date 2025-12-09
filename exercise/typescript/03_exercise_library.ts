/**
 * Exercise 3: Exercise Library with Interfaces
 *
 * You've mastered basic types and arrays. Now let's learn about INTERFACES - one
 * of TypeScript's superpowers! Interfaces define the shape of objects, making your
 * code self-documenting and catching errors when objects have the wrong structure.
 *
 * This is similar to Python dictionaries, but with TYPE SAFETY - TypeScript ensures
 * every object has the right properties with the right types!
 *
 * Concepts covered:
 * - Interfaces (defining object shapes)
 * - Object types and type checking
 * - Type aliases
 * - Optional properties
 * - Nested objects with interfaces
 * - Type safety for complex data structures
 *
 * Run this exercise: node exercise/typescript/03_exercise_library.ts
 */

// ============================================================================
// QUICK INTRO: Interfaces
// ============================================================================
// An interface defines the structure of an object:
//
//   interface Person {
//     name: string;
//     age: number;
//   }
//
//   const user: Person = { name: "Alex", age: 28 }; // ✓ OK
//   const invalid: Person = { name: "Bob" };        // ✗ ERROR! Missing age
//
// Interfaces make your code clear and catch mistakes early!

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

// Define the structure of an exercise
interface Exercise {
  name: string;
  muscleGroup: string;
  equipment: string;
  difficulty: string;
}

// You can also use type aliases (similar to interfaces for simple cases)
type DifficultyLevel = "Beginner" | "Intermediate" | "Advanced"; // Union type!

// A more advanced interface with optional properties
interface DetailedExercise {
  name: string;
  muscleGroup: string;
  equipment: string;
  difficulty: DifficultyLevel; // Using our type alias
  repsRange?: string; // Optional property (notice the ?)
  notes?: string; // Optional property
}

// ============================================================================
// EXAMPLE CODE
// ============================================================================

// Create an object that matches the Exercise interface
const benchPress: Exercise = {
  name: "Bench Press",
  muscleGroup: "Chest",
  equipment: "Barbell",
  difficulty: "Intermediate",
};

// TypeScript checks that all required properties exist and have correct types!
// Try uncommenting this to see the error:
// const invalid: Exercise = { name: "Test" }; // ERROR! Missing properties

console.log("=== Single Exercise ===");
console.log(`Exercise: ${benchPress.name}`);
console.log(`Targets: ${benchPress.muscleGroup}`);
console.log(`Equipment: ${benchPress.equipment}`);
console.log(`Difficulty: ${benchPress.difficulty}`);
console.log();

// An object with optional properties
const pullUp: DetailedExercise = {
  name: "Pull Up",
  muscleGroup: "Back",
  equipment: "Pull-up Bar",
  difficulty: "Advanced",
  repsRange: "5-10", // Optional property included
  notes: "Use full range of motion", // Optional property included
};

console.log("Pull Up notes:", pullUp.notes);

// Creating a library - an object where values are Exercise objects
// This is like Python's nested dictionaries, but with full type safety!
interface ExerciseLibrary {
  [key: string]: Exercise; // Index signature: any string key -> Exercise value
}

const exerciseLibrary: ExerciseLibrary = {
  bench_press: {
    name: "Bench Press",
    muscleGroup: "Chest",
    equipment: "Barbell",
    difficulty: "Intermediate",
  },
  squat: {
    name: "Squat",
    muscleGroup: "Legs",
    equipment: "Barbell",
    difficulty: "Intermediate",
  },
  pull_up: {
    name: "Pull Up",
    muscleGroup: "Back",
    equipment: "Pull-up Bar",
    difficulty: "Advanced",
  },
};

console.log("=== Exercise Library ===");
console.log(`Total exercises: ${Object.keys(exerciseLibrary).length}`);
console.log();

// Access specific exercise (TypeScript knows it's an Exercise!)
const squatInfo = exerciseLibrary["squat"];
console.log("Squat info:");
console.log(`  Name: ${squatInfo.name}`);
console.log(`  Targets: ${squatInfo.muscleGroup}`);
console.log();

// Loop through all exercises
console.log("All exercises:");
for (const key in exerciseLibrary) {
  const ex = exerciseLibrary[key];
  console.log(`  → ${ex.name} - ${ex.muscleGroup} (${ex.difficulty})`);
}

// ============================================================================
// YOUR TURN: TODO EXERCISES
// ============================================================================

console.log("\n=== YOUR EXERCISE LIBRARY ===");

// TODO 1: Create an interface for a workout set
// Define an interface called WorkoutSet with these properties:
// - reps: number
// - weight: number
// - restTime: number (in seconds)
//
// Type hint: Follow the pattern of the Exercise interface above
//
// Stuck? Ask: "How do I create an interface in TypeScript?"

// Write your code here:

// TODO 2: Create an object using your WorkoutSet interface
// Create a variable called firstSet of type WorkoutSet with:
// - reps: 10
// - weight: 135
// - restTime: 90
//
// Then print each property
//
// Type challenge: Try removing one property or adding a wrong type and see
// TypeScript catch the error!
//
// Need help? Ask: "How do I create an object that implements an interface?"

// Write your code here:

// TODO 3: Create an Exercise object for deadlift
// Create a variable called deadlift of type Exercise with:
// - name: "Deadlift"
// - muscleGroup: "Back"
// - equipment: "Barbell"
// - difficulty: "Advanced"
//
// Print out all its properties
//
// Type hint: const variableName: InterfaceName = { ... }
//
// Stuck? Ask: "How do I create an object with a specific interface type?"

// Write your code here:

// TODO 4: Add deadlift to the exercise library
// Add your deadlift to the exerciseLibrary object
// Use the key "deadlift"
//
// Then print the total number of exercises using Object.keys().length
//
// Type hint: exerciseLibrary["deadlift"] = deadlift;
//
// Need help? Ask: "How do I add a property to an object in TypeScript?"

// Write your code here:

// TODO 5: Create and add a shoulder press exercise
// Create a new Exercise object for shoulder press inline (without a separate variable)
// and add it directly to exerciseLibrary with key "shoulder_press"
//
// Properties:
// - name: "Overhead Press"
// - muscleGroup: "Shoulders"
// - equipment: "Barbell"
// - difficulty: "Intermediate"
//
// TypeScript will check that the object matches the Exercise interface!
//
// Stuck? Ask: "Can I create and assign an object in one line?"

// Write your code here:

// TODO 6: Print all exercise names
// Loop through exerciseLibrary and print just the name of each exercise
// Use a for...in loop or Object.values()
//
// Type hint: for (const key in library) or for (const ex of Object.values(library))
//
// Need help? Ask: "How do I loop through an object's values in TypeScript?"

// Write your code here:

// TODO 7: Find chest exercises with type-safe filtering
// Loop through exerciseLibrary and print exercises where muscleGroup is "Chest"
// Notice how TypeScript knows the properties available on each exercise!
//
// HINT: Use an if statement inside your loop
//
// Type challenge: Try accessing a property that doesn't exist and see the error!
//
// Stuck? Ask: "How do I filter objects based on a property in TypeScript?"

// Write your code here:

// ============================================================================
// BONUS CHALLENGES (Optional)
// ============================================================================

// BONUS 1: Create an interface with optional properties
// Create an interface called AdvancedExercise that extends Exercise
// and adds optional properties:
// - caloriesPerRep?: number
// - videoUrl?: string
//
// HINT: Use 'extends' keyword: interface NewInterface extends OldInterface { }
//
// For help: Ask "How do I extend an interface in TypeScript?"

// Write your code here:

// BONUS 2: Create a type for equipment categories
// Create a union type called EquipmentType that can only be:
// "Barbell" | "Dumbbell" | "Machine" | "Bodyweight" | "Cable"
//
// Then modify your Exercise interface (or create a new one) to use this type
// instead of a plain string for equipment
//
// This provides even MORE type safety - only valid equipment types allowed!
//
// Want guidance? Ask: "How do I create a union type in TypeScript?"

// Write your code here:

// BONUS 3: Create a function with interface parameters
// Create a function called displayExercise that:
// - Takes a parameter of type Exercise
// - Returns void (doesn't return anything)
// - Prints a formatted description of the exercise
//
// HINT: function functionName(param: InterfaceType): void { }
//
// Then call it with one of your exercises
//
// Type hint: TypeScript will ensure you only pass Exercise objects!
//
// Need help? Ask: "How do I use an interface as a function parameter?"

// Write your code here:

// ============================================================================
// TESTING YOUR CODE
// ============================================================================

// Expected results:
// - WorkoutSet interface defined with reps, weight, restTime
// - firstSet object created and printed
// - deadlift Exercise object created and added to library
// - shoulder_press added to library
// - Exercise library now has 5 exercises
// - All exercise names printed
// - Only "Bench Press" shown when filtering for chest
//
// Key TypeScript features:
// - Interfaces provide structure and documentation
// - Type checking prevents missing or wrong properties
// - Optional properties allow flexibility
// - Union types restrict values to specific options
// - IDE shows available properties (autocomplete!)
//
// If you get type errors:
// - Check all required properties are present
// - Verify property types match the interface
// - Make sure property names are spelled correctly
//
// Ask me: "Why is TypeScript showing an error on my interface?"
