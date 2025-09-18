import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

def move_motor(direction, steps, step_delay=0.005):
    """
    Move the stepper motor in the specified direction for a given number of steps.
    
    Args:
        direction: CW (1) for clockwise, CCW (0) for counterclockwise
        steps: Number of steps to move
        step_delay: Delay between steps (controls speed)
    """
    print(f"Moving motor {'clockwise' if direction == CW else 'counterclockwise'} for {steps} steps...")
    
    # Set direction
    GPIO.output(DIR, direction)
    
    # Allow time for direction change
    sleep(0.1)
    
    # Execute steps
    for step in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(step_delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(step_delay)
    
    print("Movement complete!")

def get_user_input():
    """Get direction and step count from user input."""
    try:
        print("\nStepper Motor Control")
        print("Direction options: 1 for Clockwise, 0 for Counterclockwise")
        
        direction = int(input("Enter direction (1 for CW, 0 for CCW): "))
        if direction not in [0, 1]:
            print("Invalid direction! Please enter 0 or 1.")
            return None, None
        
        steps = int(input("Enter number of steps: "))
        if steps <= 0:
            print("Invalid step count! Please enter a positive number.")
            return None, None
        
        return direction, steps
    
    except ValueError:
        print("Invalid input! Please enter numbers only.")
        return None, None

def main():
    """Main program loop."""
    try:
        print("Stepper Motor Controller")
        print("Press Ctrl+C to exit")
        
        while True:
            direction, steps = get_user_input()
            
            if direction is not None and steps is not None:
                move_motor(direction, steps)
            
            # Ask if user wants to continue
            continue_choice = input("\nDo you want to move the motor again? (y/n): ").lower()
            if continue_choice != 'y' and continue_choice != 'yes':
                break
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    
    finally:
        print("Cleaning up GPIO...")
        GPIO.cleanup()
        print("GPIO cleanup complete!")

if __name__ == "__main__":
    main()