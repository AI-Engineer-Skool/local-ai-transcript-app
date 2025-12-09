/**
 * Exercise 6: Complete Gym Simulator with Data Serialization
 *
 * This is the final exercise - bringing EVERYTHING together! You'll build a complete
 * gym simulator using types, interfaces, classes, and DATA SERIALIZATION. This demonstrates
 * how TypeScript's type system scales to real-world applications.
 *
 * JSON serialization is the technique used to store data in browsers (localStorage)
 * or send data to APIs - you'll use this constantly in frontend development!
 *
 * Concepts covered:
 * - JSON serialization with types (JSON.stringify/JSON.parse)
 * - Type-safe data structures for storage
 * - Error handling (try/catch)
 * - Complex class systems
 * - Type safety in a full application
 * - Bringing together all TypeScript concepts
 *
 * Run this exercise: npx tsx exercise/typescript/06_gym_simulator.ts
 */

// ============================================================================
// QUICK INTRO: JSON Serialization in TypeScript
// ============================================================================
// JSON (JavaScript Object Notation) is how we save and load data:
//
// - JSON.stringify(object) - converts object to JSON string
// - JSON.parse(string) - converts JSON string back to object
// - try/catch - handles errors (like invalid JSON)
//
// The key TypeScript feature: You can TYPE the data you're serializing!
// You'll use this constantly for:
// - Saving to localStorage in browsers
// - Sending/receiving data from APIs
// - Storing user preferences and app state

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
    const timeStr = now.toTimeString().split(" ")[0] ?? "00:00:00";
    const dateStr =
      now.toISOString().split("T")[0] + " " + timeStr.slice(0, 5);

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
    console.log(`  Logged workout for ${this.name}: ${exercise}`);
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
   * Convert to plain object for JSON serialization.
   * This pattern is used for saving to localStorage or sending to APIs.
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
   * Static factory method pattern.
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
   * Serialize gym data to JSON string.
   * In a real app, this could be saved to localStorage or sent to an API.
   */
  toJSON(): string {
    const membersObj: { [id: number]: MemberData } = {};
    this.members.forEach((member, id) => {
      membersObj[id] = member.toData();
    });

    const data: GymData = {
      gymName: this.name,
      nextMemberId: this.nextMemberId,
      members: membersObj,
    };

    return JSON.stringify(data, null, 2);
  }

  /**
   * Load gym data from a JSON string.
   * Returns true if successful, false if there was an error.
   */
  loadFromJSON(jsonString: string): boolean {
    try {
      const data: GymData = JSON.parse(jsonString);

      this.name = data.gymName;
      this.nextMemberId = data.nextMemberId;
      this.members.clear();

      for (const idStr in data.members) {
        const id = parseInt(idStr);
        const memberData = data.members[id];
        if (memberData) {
          this.members.set(id, GymMember.fromData(memberData));
        }
      }

      console.log(`Loaded gym: ${this.name} with ${this.members.size} members`);
      return true;
    } catch (error) {
      console.log(`Error loading data: ${error}`);
      return false;
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

// Demonstrate serialization
console.log("\n=== Serialized Gym Data (JSON) ===");
const gymJson = myGym.toJSON();
console.log(gymJson);

// Demonstrate loading from JSON
console.log("\n=== Loading from JSON ===");
const newGym = new Gym("Empty Gym");
newGym.loadFromJSON(gymJson);
console.log("\nLoaded member summaries:");
for (const member of newGym.getAllMembers()) {
  console.log(member.getSummary());
}

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

// TODO 6: Serialize your gym data
// Call toJSON() on your gym and store the result
// Print the JSON string to see your gym data serialized
//
// Type hint: const jsonData: string = yourGym.toJSON();
//
// This is the same format you'd use to:
// - Save to localStorage in a browser
// - Send to an API endpoint
// - Store in a database
//
// Need help? Ask: "How do I convert an object to JSON in TypeScript?"

// Write your code here:

// TODO 7: Test loading data from JSON
// Create a NEW empty gym (different name)
// Load your serialized JSON data using loadFromJSON()
// Print all member summaries to verify it loaded correctly
//
// This demonstrates data persistence - the data survives being
// serialized and deserialized!
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

// BONUS 3: Simulate localStorage (advanced)
// Create a simple in-memory "storage" object:
// const storage: { [key: string]: string } = {};
//
// Create functions:
// - saveToStorage(key: string, data: string): void
// - loadFromStorage(key: string): string | undefined
//
// Use these to "save" and "load" your gym data by key
// This simulates how localStorage works in browsers!
//
// Ask: "How does localStorage work in browsers?"

// Write your code here:

// ============================================================================
// TESTING YOUR CODE
// ============================================================================

// After completing the TODOs, you should have:
// - A gym with at least 2 members
// - Multiple workouts logged for each member
// - Member summaries showing visits and total volume
// - JSON output showing serialized gym data
// - A second gym loaded from that JSON data
//
// TypeScript ensures:
// - All method parameters have correct types
// - Properties are accessed safely
// - Optional values (like getMember result) are checked
// - JSON data matches expected structure
//
// Key learning points:
// - TypeScript provides type safety for data serialization
// - Interfaces define data structure for JSON
// - Optional types (T | undefined) require checking
// - Type system scales to complex applications
// - All the concepts work together seamlessly
//
// Real-world applications:
// - Browser localStorage: localStorage.setItem("gym", gym.toJSON())
// - API calls: fetch("/api/gym", { body: gym.toJSON() })
// - State management: Redux/Zustand use similar patterns
//
// If you get type errors:
// - Read the error message carefully
// - Check for undefined values
// - Verify all types match
// - Use type guards (if checks) for optional values
//
// Ask me: "What's the best way to improve my TypeScript skills?"

// Make this file a module to avoid variable name conflicts with other exercise files
export {};
