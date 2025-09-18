#!/usr/bin/env python3
"""
Stepper Motor Control with TB6600 Driver for Raspberry Pi
Commands: "right [steps]" or "left [steps]"
Note: ENABLE_PIN is not used in this Raspberry Pi version
"""

import RPi.GPIO as GPIO
import time
import sys

# Pin definitions
STEP_PIN = 8  # GPIO 8
DIR_PIN = 10   # GPIO 10
ENABLE_PIN = 12  # GPIO 12 - Add enable pin for better control

# Motor parameters
STEP_DELAY = 0.002  # seconds between steps (increased for stability)
DIR_SETUP_TIME = 0.001  # delay after direction change

def setup_gpio():
    """Initialize GPIO pins"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    # Setup pins as outputs
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(ENABLE_PIN, GPIO.OUT)
    
    # Initialize pins to LOW
    GPIO.output(STEP_PIN, GPIO.LOW)
    GPIO.output(DIR_PIN, GPIO.LOW)
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Enable the driver (active LOW)
    
    print("Stepper Motor Controller Ready")
    print("Commands: 'right [steps]' or 'left [steps]'")
    print("Type 'quit' to exit")

def cleanup_gpio():
    """Clean up GPIO on exit"""
    # Disable motor driver before cleanup
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable driver (active LOW)
    time.sleep(0.1)  # Brief delay to ensure driver disables
    GPIO.cleanup()
    print("GPIO cleanup complete")

def move_motor(clockwise, steps):
    """
    Move the stepper motor
    
    Args:
        clockwise (bool): True for clockwise, False for counterclockwise
        steps (int): Number of steps to move
    """
    # Set direction
    GPIO.output(DIR_PIN, GPIO.HIGH if clockwise else GPIO.LOW)
    
    # Wait for direction to stabilize
    time.sleep(DIR_SETUP_TIME)
    
    # Step the motor
    for i in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY / 2)  # Half delay for HIGH pulse
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY / 2)  # Half delay for LOW pulse
        
        # Optional: Print progress for large step counts
        if steps > 100 and (i + 1) % 50 == 0:
            print(f"Progress: {i + 1}/{steps} steps")
    
    print("Movement complete")

def parse_and_execute_command(command):
    """
    Parse and execute motor commands
    
    Args:
        command (str): Command string like "right 100" or "left 50"
    """
    try:
        parts = command.strip().split()
        
        if len(parts) != 2:
            print("Invalid command format. Use: 'right [steps]' or 'left [steps]'")
            return
        
        direction = parts[0].lower()
        steps = int(parts[1])
        
        if steps <= 0:
            print("Invalid step count. Must be positive integer.")
            return
        
        if direction == "right":
            move_motor(True, steps)
            print(f"Moving right {steps} steps")
        elif direction == "left":
            move_motor(False, steps)
            print(f"Moving left {steps} steps")
        else:
            print("Invalid direction. Use 'right' or 'left'")
            
    except ValueError:
        print("Invalid step count. Must be a number.")
    except Exception as e:
        print(f"Error executing command: {e}")

def main():
    """Main program loop"""
    try:
        setup_gpio()
        
        print("\nEnter commands (or 'quit' to exit):")
        
        while True:
            try:
                command = input("> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                
                if command:
                    parse_and_execute_command(command)
                    
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected")
                break
            except EOFError:
                print("\nEOF detected")
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup_gpio()
        print("Program terminated")

if __name__ == "__main__":
    main()