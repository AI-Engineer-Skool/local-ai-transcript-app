/**
 * Exercise 5: Gym Equipment Manager with Classes
 *
 * You've mastered functions and interfaces. Now let's learn about CLASSES with TypeScript!
 * Classes combine data (properties) and behavior (methods) into reusable blueprints.
 * TypeScript adds type safety to properties, methods, and access modifiers.
 *
 * Concepts covered:
 * - Class properties with types
 * - Constructor parameters with types
 * - Method parameter and return types
 * - Access modifiers (public, private, readonly)
 * - Creating and using class instances
 * - Type safety in object-oriented code
 *
 * Run this exercise: node exercise/typescript/05_gym_equipment.ts
 */

// ============================================================================
// QUICK INTRO: Classes in TypeScript
// ============================================================================
// A class is a blueprint for creating objects.
//
// class Equipment {
//   name: string;              // Property type
//   weight: number;
//
//   constructor(name: string, weight: number) {  // Constructor types
//     this.name = name;
//     this.weight = weight;
//   }
//
//   display(): void {          // Method return type
//     console.log(this.name);
//   }
// }
//
// const barbell = new Equipment("Barbell", 45);  // TypeScript knows the type!

// ============================================================================
// EXAMPLE CODE
// ============================================================================

/**
 * Represents a piece of gym equipment.
 */
class GymEquipment {
  // Property declarations with types
  name: string;
  weight: number;
  inUse: boolean;
  usesToday: number;

  /**
   * Constructor with typed parameters.
   */
  constructor(name: string, weight: number) {
    this.name = name;
    this.weight = weight;
    this.inUse = false;
    this.usesToday = 0;
  }

  /**
   * Mark equipment as in use.
   * Method with no return value (void).
   */
  checkOut(): void {
    if (this.inUse) {
      console.log(`${this.name} is already in use!`);
    } else {
      this.inUse = true;
      this.usesToday++;
      console.log(`${this.name} checked out. Uses today: ${this.usesToday}`);
    }
  }

  /**
   * Mark equipment as available.
   */
  checkIn(): void {
    if (!this.inUse) {
      console.log(`${this.name} is already checked in!`);
    } else {
      this.inUse = false;
      console.log(`${this.name} checked back in. Ready for next person!`);
    }
  }

  /**
   * Get status message.
   * Method with string return type.
   */
  getStatus(): string {
    const status = this.inUse ? "IN USE" : "AVAILABLE";
    return `${this.name} (${this.weight} lbs) - ${status} - Used ${this.usesToday} times today`;
  }
}

// TypeScript's access modifiers (more advanced)
class SecureEquipment {
  // public: accessible everywhere (default)
  public name: string;

  // private: only accessible inside the class
  private maintenanceCount: number;

  // readonly: can only be set in constructor
  readonly serialNumber: string;

  constructor(name: string, serialNumber: string) {
    this.name = name;
    this.serialNumber = serialNumber;
    this.maintenanceCount = 0;
  }

  // Public method
  public performMaintenance(): void {
    this.maintenanceCount++;
    console.log(`Maintenance performed. Total: ${this.maintenanceCount}`);
  }

  // Private method (only accessible inside class)
  private resetMaintenance(): void {
    this.maintenanceCount = 0;
  }

  // Getter (like a property but calculated)
  get needsMaintenance(): boolean {
    return this.maintenanceCount < 5;
  }
}

// Create instances
console.log("=== Creating Equipment ===");
const barbell = new GymEquipment("Olympic Barbell", 45);
const dumbbell = new GymEquipment("50lb Dumbbell", 50);

// TypeScript knows the type of barbell!
// Hover over barbell to see: const barbell: GymEquipment

console.log("\n=== Using Equipment ===");
console.log(barbell.getStatus());
barbell.checkOut();
console.log(barbell.getStatus());

console.log();
dumbbell.checkOut();
dumbbell.checkIn();
console.log(dumbbell.getStatus());

// Each instance has its own data
console.log("\n=== Multiple Uses ===");
barbell.checkIn();
barbell.checkOut();
barbell.checkIn();
barbell.checkOut();
console.log(`Barbell uses: ${barbell.usesToday}`);
console.log(`Dumbbell uses: ${dumbbell.usesToday}`);

// ============================================================================
// YOUR TURN: TODO EXERCISES
// ============================================================================

console.log("\n\n=== YOUR GYM EQUIPMENT MANAGER ===");

// TODO 1: Create three equipment objects
// Create instances with proper types:
// - bench: type GymEquipment, "Bench Press Bench", 50 lbs
// - squatRack: type GymEquipment, "Squat Rack", 100 lbs
// - kettlebell: type GymEquipment, "32kg Kettlebell", 70 lbs
//
// Type hint: const varName: ClassName = new ClassName(args);
// OR let TypeScript infer: const varName = new ClassName(args);
//
// Stuck? Ask: "How do I create an instance of a class in TypeScript?"

// Write your code here:

// TODO 2: Use the getStatus method
// Call getStatus() on each of your three equipment objects and print the results
//
// Type hint: objectName.methodName()
//
// Need help? Ask: "How do I call methods on a class instance?"

// Write your code here:

// TODO 3: Simulate using equipment
// For the bench:
// 1. Check it out
// 2. Print its status
// 3. Check it back in
// 4. Print its status again
//
// Type hint: Call the checkOut(), getStatus(), and checkIn() methods
//
// Stuck? Ask: "How do I call multiple methods on an object in sequence?"

// Write your code here:

// TODO 4: Track multiple uses
// Check the squatRack out and in 3 times (simulate 3 people using it)
// Then print how many times it's been used today
//
// HINT: Access the usesToday property directly: squatRack.usesToday
//
// Type hint: TypeScript knows usesToday is a number!
//
// Need help? Ask: "How do I access a class property in TypeScript?"

// Write your code here:

// TODO 5: Create a Treadmill class
// Create a class called Treadmill with:
// - Properties (with types!):
//   - name: string
//   - maxSpeed: number
//   - isRunning: boolean (initialize to false)
//   - distanceToday: number (initialize to 0)
//
// - Constructor:
//   - Parameters: name (string), maxSpeed (number)
//   - Initialize all properties
//
// - Methods:
//   - startRunning(): void - sets isRunning to true, prints message
//   - stopRunning(): void - sets isRunning to false, prints message
//   - logDistance(miles: number): void - adds miles to distanceToday
//   - getStatus(): string - returns status with name, speed, running state, distance
//
// Type hint: Follow the GymEquipment class pattern above
//
// Stuck? Ask: "How do I create a class with typed properties and methods in TypeScript?"

// Write your code here:

// TODO 6: Create and test a Treadmill instance
// Create a Treadmill object:
// - Name: "Treadmill #1"
// - Max speed: 12.0
//
// Then:
// 1. Print its status
// 2. Start it running
// 3. Log 3.5 miles
// 4. Stop it running
// 5. Print status again
//
// Type hint: const treadmill = new Treadmill("Treadmill #1", 12.0);
//
// Need help? Ask: "How do I create and use a custom class?"

// Write your code here:

// ============================================================================
// BONUS CHALLENGES (Optional)
// ============================================================================

// BONUS 1: Add access modifiers to Treadmill
// Modify your Treadmill class to use:
// - public for name and getStatus()
// - private for distanceToday
// - readonly for maxSpeed (set only in constructor)
//
// Add a getter for distance: get distance(): number { return this.distanceToday; }
// This lets you read the private property safely!
//
// For help: Ask "How do access modifiers work in TypeScript classes?"

// Write your code here:

// BONUS 2: Create a class that implements an interface
// First, create an interface:
// interface Equipment {
//   name: string;
//   getStatus(): string;
// }
//
// Then create a BenchPress class that implements Equipment:
// class BenchPress implements Equipment {
//   name: string;
//   maxWeight: number;
//   // ... implement required interface members plus your own
// }
//
// Want guidance? Ask: "How do I make a class implement an interface in TypeScript?"

// Write your code here:

// BONUS 3: Create a static method
// Add a static method to your Treadmill class:
// static convertMilesToKm(miles: number): number {
//   return miles * 1.60934;
// }
//
// Static methods are called on the class itself, not instances:
// const km = Treadmill.convertMilesToKm(5);
//
// Need help? Ask: "What are static methods in TypeScript?"

// Write your code here:

// ============================================================================
// TESTING YOUR CODE
// ============================================================================

// Expected behavior:
// - Three equipment objects created (bench, squatRack, kettlebell)
// - Status shows equipment details and usage count
// - Check-out/check-in changes inUse status
// - usesToday increments with each check-out
// - Treadmill class works with all methods
// - Each object maintains its own state
//
// TypeScript provides:
// - Type checking for property access
// - Auto-completion for methods and properties
// - Errors when accessing non-existent members
// - Type safety for method parameters and returns
//
// Key learning points:
// - Properties need type annotations
// - Constructor parameters need types
// - Methods need parameter and return types
// - Access modifiers control visibility (public, private, readonly)
// - TypeScript ensures type safety for classes
//
// If you get type errors:
// - Check all properties have type annotations
// - Verify method parameters have types
// - Ensure return types match what you're returning
// - Check that you're accessing public properties/methods
//
// Ask me: "Why is TypeScript showing an error in my class?"
