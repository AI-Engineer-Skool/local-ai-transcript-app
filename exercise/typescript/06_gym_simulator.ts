/**
 * Exercise 6: Complete Gym Simulator with File I/O
 *
 * This is the final exercise - bringing EVERYTHING together! You'll build a complete
 * gym simulator using types, interfaces, classes, and FILE I/O. This demonstrates
 * how TypeScript's type system scales to real-world applications.
 *
 * Concepts covered:
 * - File I/O with Node.js (fs module)
 * - JSON serialization with types
 * - Error handling (try/catch)
 * - Complex class systems
 * - Type safety in a full application
 * - Bringing together all TypeScript concepts
 *
 * Run this exercise: node exercise/typescript/06_gym_simulator.ts
 */

import * as fs from "fs";

// ============================================================================
// QUICK INTRO: File I/O in TypeScript
// ============================================================================
// TypeScript works with Node.js's fs (file system) module:
//
// - fs.writeFileSync(path, data) - saves data to a file
// - fs.readFileSync(path, 'utf8') - reads data from a file
// - JSON.stringify(object) - converts object to JSON string
// - JSON.parse(string) - converts JSON string to object
// - try/catch - handles errors (like file not found)
//
// The key TypeScript feature: You can TYPE the data you're saving/loading!

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

/**
 * Represents a single workout session.
 */
interface Workout {
  date: string;
  exercise: string;
  sets: number;
  reps: number;
  weight: number;
  volume: number;
}

/**
 * Saved member data structure.
 */
interface MemberData {
  name: string;
  membershipId: number;
  workouts: Workout[];
  totalVisits: number;
}

/**
 * Saved gym data structure.
 */
interface GymData {
  gymName: string;
  nextMemberId: number;
  members: { [id: number]: MemberData };
}

// ============================================================================
// EXAMPLE CODE
// ============================================================================

/**
 * Represents a gym member with workout history.
 */
class GymMember {
  name: string;
  membershipId: number;
  workouts: Workout[];
  totalVisits: number;

  constructor(name: string, membershipId: number) {
    this.name = name;
    this.membershipId = membershipId;
    this.workouts = [];
    this.totalVisits = 0;
  }

  /**
   * Log a workout session.
   */
  logWorkout(
    exercise: string,
    sets: number,
    reps: number,
    weight: number
  ): void {
    const now = new Date();
    const dateStr =
      now.toISOString().split("T")[0] +
      " " +
      now.toTimeString().split(" ")[0].slice(0, 5);

    const workout: Workout = {
      date: dateStr,
      exercise: exercise,
      sets: sets,
      reps: reps,
      weight: weight,
      volume: sets * reps * weight,
    };

    this.workouts.push(workout);
    this.totalVisits++;
    console.log(`✓ Logged workout for ${this.name}: ${exercise}`);
  }

  /**
   * Get member summary.
   */
  getSummary(): string {
    if (this.workouts.length === 0) {
      return `${this.name} - No workouts logged yet`;
    }

    const totalVolume = this.workouts.reduce((sum, w) => sum + w.volume, 0);
    return `${this.name} - ${this.totalVisits} visits - ${totalVolume} lbs total volume`;
  }

  /**
   * Convert to plain object for JSON saving.
   */
  toData(): MemberData {
    return {
      name: this.name,
      membershipId: this.membershipId,
      workouts: this.workouts,
      totalVisits: this.totalVisits,
    };
  }

  /**
   * Create from plain object (for loading from JSON).
   */
  static fromData(data: MemberData): GymMember {
    const member = new GymMember(data.name, data.membershipId);
    member.workouts = data.workouts;
    member.totalVisits = data.totalVisits;
    return member;
  }
}

/**
 * Represents the entire gym.
 */
class Gym {
  name: string;
  private members: Map<number, GymMember>; // Map: key type -> value type
  private nextMemberId: number;

  constructor(name: string) {
    this.name = name;
    this.members = new Map();
    this.nextMemberId = 1;
  }

  /**
   * Add a new member.
   */
  addMember(name: string): number {
    const memberId = this.nextMemberId;
    this.nextMemberId++;
    const member = new GymMember(name, memberId);
    this.members.set(memberId, member);
    console.log(`Welcome ${name}! Your membership ID is: ${memberId}`);
    return memberId;
  }

  /**
   * Get a member by ID.
   */
  getMember(memberId: number): GymMember | undefined {
    return this.members.get(memberId);
  }

  /**
   * Get all members.
   */
  getAllMembers(): GymMember[] {
    return Array.from(this.members.values());
  }

  /**
   * Save gym data to a JSON file.
   */
  saveToFile(filename: string): void {
    const membersObj: { [id: number]: MemberData } = {};
    this.members.forEach((member, id) => {
      membersObj[id] = member.toData();
    });

    const data: GymData = {
      gymName: this.name,
      nextMemberId: this.nextMemberId,
      members: membersObj,
    };

    try {
      const jsonString = JSON.stringify(data, null, 2);
      fs.writeFileSync(filename, jsonString, "utf8");
      console.log(`✓ Gym data saved to ${filename}`);
    } catch (error) {
      console.log(`✗ Error saving file: ${error}`);
    }
  }

  /**
   * Load gym data from a JSON file.
   */
  loadFromFile(filename: string): void {
    try {
      const jsonString = fs.readFileSync(filename, "utf8");
      const data: GymData = JSON.parse(jsonString);

      this.name = data.gymName;
      this.nextMemberId = data.nextMemberId;
      this.members.clear();

      for (const idStr in data.members) {
        const id = parseInt(idStr);
        const memberData = data.members[id];
        this.members.set(id, GymMember.fromData(memberData));
      }

      console.log(`✓ Loaded gym data from ${filename}`);
      console.log(`  Gym: ${this.name} with ${this.members.size} members`);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") {
        console.log(`✗ File ${filename} not found. Starting fresh!`);
      } else {
        console.log(`✗ Error loading file: ${error}`);
      }
    }
  }
}

// Demo the system
console.log("=== Gym Simulator Demo ===\n");

const myGym = new Gym("Iron Paradise");

const member1Id = myGym.addMember("Alex Johnson");
const member2Id = myGym.addMember("Sam Smith");

const member1 = myGym.getMember(member1Id);
const member2 = myGym.getMember(member2Id);

if (member1) {
  member1.logWorkout("Bench Press", 3, 10, 135);
  member1.logWorkout("Squat", 4, 8, 185);
}

if (member2) {
  member2.logWorkout("Deadlift", 5, 5, 225);
}

console.log("\n=== Member Summaries ===");
for (const member of myGym.getAllMembers()) {
  console.log(member.getSummary());
}

console.log();
myGym.saveToFile("gym_data.json");

// ============================================================================
// YOUR TURN: TODO EXERCISES
// ============================================================================

console.log("\n\n=== YOUR GYM SIMULATOR ===\n");

// TODO 1: Create your own gym
// Create a Gym object with your chosen name
// Store it in a variable called yourGym
//
// Type hint: const yourGym: Gym = new Gym("Your Gym Name");
// OR: const yourGym = new Gym("Your Gym Name");
//
// Stuck? Ask: "How do I create a class instance in TypeScript?"

// Write your code here:

// TODO 2: Add yourself as a member
// Use the addMember method to add yourself to the gym
// Store your member ID in myMemberId (type: number)
// Then get your member object using getMember() and store in myMember
//
// Type hint: const myMember = yourGym.getMember(myMemberId);
// Note: getMember returns GymMember | undefined, so check if it exists!
//
// Need help? Ask: "How do I use a method that returns a value in TypeScript?"

// Write your code here:

// TODO 3: Check if member exists before using
// Since getMember can return undefined, check if myMember exists
// Use: if (myMember) { ... }
//
// Inside the if block, log three workouts:
// 1. Bench Press: 3 sets, 10 reps, 135 lbs
// 2. Squats: 4 sets, 8 reps, 185 lbs
// 3. Pull-ups: 3 sets, 12 reps, 0 lbs
//
// Type hint: TypeScript knows myMember is defined inside the if block!
//
// Stuck? Ask: "How do I check for undefined in TypeScript?"

// Write your code here:

// TODO 4: Add another member and log their workout
// Add a friend or workout partner
// Store their ID and get their member object
// Check if it exists, then log at least one workout for them
//
// Type hint: Follow the same pattern as TODO 2 and 3
//
// Need help? Ask: "How do I repeat a process for a second object?"

// Write your code here:

// TODO 5: Print all member summaries
// Get all members using getAllMembers() and loop through them
// Print each member's summary
//
// HINT: getAllMembers() returns GymMember[]
// HINT: Use a for...of loop: for (const member of array)
//
// Type challenge: Hover over member in the loop - TypeScript knows it's GymMember!
//
// Stuck? Ask: "How do I loop through an array in TypeScript?"

// Write your code here:

// TODO 6: Save your gym data
// Call saveToFile with filename "my_gym_data.json"
// After running, check that the file was created!
//
// Type hint: yourGym.saveToFile("my_gym_data.json");
//
// Need help? Ask: "How do I save data to a file in TypeScript?"

// Write your code here:

// TODO 7: Test loading data (Optional - requires running twice)
// Comment out TODOs 1-6, then create a NEW empty gym
// and try loading from "my_gym_data.json" using loadFromFile()
// Print all member summaries to verify it loaded correctly
//
// This demonstrates data persistence across program runs!
//
// Want to see it work? Ask: "How do I test loading saved data?"

// Write your code here:

// ============================================================================
// BONUS CHALLENGES (Optional)
// ============================================================================

// BONUS 1: Add error handling for undefined members
// Create a function called safeMemberOperation that:
// - Takes: gym (Gym), memberId (number), operation (function)
// - Gets the member, checks if undefined
// - If exists, calls operation with the member
// - If not, logs "Member not found"
//
// Type hint: operation: (member: GymMember) => void
//
// For help: Ask "How do I create a function that takes another function as a parameter?"

// Write your code here:

// BONUS 2: Add workout statistics interface and methods
// Create an interface WorkoutStats with:
// - totalWorkouts: number
// - totalVolume: number
// - averageVolume: number
// - favoriteExercise: string
//
// Add a method to GymMember: getStats(): WorkoutStats
//
// Want guidance? Ask: "How do I add methods that return complex objects?"

// Write your code here:

// BONUS 3: Create a generic save/load utility
// Create functions with proper typing:
// - saveJSON<T>(filename: string, data: T): void
// - loadJSON<T>(filename: string): T | undefined
//
// These are GENERIC functions that work with any type!
//
// This is advanced TypeScript! Ask: "How do generics work in TypeScript?"

// Write your code here:

// ============================================================================
// TESTING YOUR CODE
// ============================================================================

// After completing the TODOs, you should have:
// - A gym with at least 2 members
// - Multiple workouts logged for each member
// - Member summaries showing visits and total volume
// - A "my_gym_data.json" file created
//
// TypeScript ensures:
// - All method parameters have correct types
// - Properties are accessed safely
// - Optional values (like getMember result) are checked
// - JSON data matches expected structure
//
// Key learning points:
// - TypeScript provides type safety for file I/O
// - Interfaces define data structure for serialization
// - Optional types (T | undefined) require checking
// - Type system scales to complex applications
// - All the concepts work together seamlessly
//
// To verify your work:
// 1. Run the file: node exercise/typescript/06_gym_simulator.ts
// 2. Check for "my_gym_data.json" in exercise/typescript/
// 3. Open the JSON file - it should be readable
// 4. Try loading it back (TODO 7)
//
// Congratulations! You've completed all TypeScript exercises!
// You now understand:
// - Basic types and type inference
// - Arrays and typed collections
// - Interfaces and type aliases
// - Functions with type signatures
// - Classes with typed properties and methods
// - File I/O with type safety
// - Building complete applications with TypeScript
//
// If you get type errors:
// - Read the error message carefully
// - Check for undefined values
// - Verify all types match
// - Use type guards (if checks) for optional values
//
// Ask me: "What's the best way to improve my TypeScript skills?"
