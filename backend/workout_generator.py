import random
from typing import List, Dict, Any

# Exercise database with ONLY implemented pose detection models
EXERCISES = {
    "bodyweight": {
        "Push-ups": {
            "type": ["Strength Training"],
            "target": "Chest, Shoulders, Triceps",
            "equipment": "None",
            "difficulty": ["Beginner", "Intermediate"],
            "instructions": "Start in a plank position with hands shoulder-width apart. Lower your body until your chest nearly touches the ground, then push back up.",
            "form_tips": [
                "Keep your core tight throughout the movement",
                "Maintain a straight line from head to heels",
                "Don't let your hips sag"
            ],
            "fitness_goals": ["Strength Training"]
        },
        "Squats": {
            "type": ["Strength Training"],
            "target": "Quadriceps, Hamstrings, Glutes",
            "equipment": "None",
            "difficulty": ["Beginner", "Intermediate"],
            "instructions": "Stand with feet shoulder-width apart. Lower your body by bending your knees and hips, as if sitting back into a chair. Return to standing.",
            "form_tips": [
                "Keep your chest up",
                "Keep your knees in line with your toes",
                "Push through your heels"
            ],
            "fitness_goals": ["Strength Training"]
        },
        "Sun Salutation": {
            "type": ["Yoga"],
            "target": "Full Body",
            "equipment": "None",
            "difficulty": ["Beginner", "Intermediate"],
            "instructions": "Start in mountain pose, raise arms overhead, fold forward, step back to plank, lower to ground, cobra pose, downward dog, step forward, fold forward, return to mountain pose.",
            "form_tips": [
                "Keep your breath steady and controlled",
                "Maintain proper alignment in each pose",
                "Move with awareness and mindfulness"
            ],
            "fitness_goals": ["Flexibility", "Mind-Body Connection"]
        },
        "Mountain Climbers": {
            "type": ["Cardio"],
            "target": "Core, Shoulders, Legs",
            "equipment": "None",
            "difficulty": ["Beginner", "Intermediate"],
            "instructions": "Start in plank position, alternate bringing knees to chest in a running motion while maintaining core stability.",
            "form_tips": [
                "Keep your core tight",
                "Maintain a straight line from head to heels",
                "Move at a controlled pace"
            ],
            "fitness_goals": ["Cardiovascular Endurance"]
        }
    },
    "equipment": {
        "Dumbbell Row": {
            "type": ["Strength Training"],
            "target": "Back, Biceps",
            "equipment": "Dumbbells",
            "difficulty": ["Beginner", "Intermediate"],
            "instructions": "Bend over with a flat back, holding dumbbells. Pull the weights up towards your hips, squeezing your shoulder blades together.",
            "form_tips": [
                "Keep your back straight",
                "Squeeze shoulder blades",
                "Keep core engaged",
                "Control the weight"
            ],
            "fitness_goals": ["Strength Training"]
        },
        "Jump Rope": {
            "type": ["Cardio"],
            "target": "Full Body",
            "equipment": "Jump Rope",
            "difficulty": ["Beginner", "Intermediate"],
            "instructions": "Hold jump rope handles, swing rope overhead and jump over it as it comes under your feet.",
            "form_tips": [
                "Keep elbows close to body",
                "Jump just high enough to clear the rope",
                "Land softly on the balls of your feet"
            ],
            "fitness_goals": ["Cardiovascular Endurance"]
        },
        "Yoga with Blocks": {
            "type": ["Yoga"],
            "target": "Full Body",
            "equipment": "Yoga Blocks",
            "difficulty": ["Beginner", "Intermediate"],
            "instructions": "Use blocks to support poses and improve alignment in various yoga postures.",
            "form_tips": [
                "Use blocks to maintain proper alignment",
                "Keep spine long and engaged",
                "Breathe deeply and steadily"
            ],
            "fitness_goals": ["Flexibility", "Mind-Body Connection"]
        }
    }
}

# Available workout types
WORKOUT_TYPES = ["Yoga", "Cardio"]

# Available fitness goals
FITNESS_GOALS = ["Flexibility", "Mind-Body Connection", "Cardiovascular Endurance"]

# Available equipment
EQUIPMENT_LIST = ["Jump Rope", "Yoga Blocks"]

def generate_workout(
    fitness_goal: str,
    available_equipment: List[str],
    duration: int,
    experience_level: str,
    workout_type: str,
    restrictions: List[str] = None
) -> Dict[str, Any]:
    """
    Generate a personalized workout plan based on user preferences.
    """
    print(f"\nWorkout Generation Debug:")
    print(f"Input parameters:")
    print(f"- Fitness Goal: {fitness_goal}")
    print(f"- Available Equipment: {available_equipment}")
    print(f"- Duration: {duration}")
    print(f"- Experience Level: {experience_level}")
    print(f"- Workout Type: {workout_type}")
    print(f"- Restrictions: {restrictions}")

    # Initialize workout structure
    workout = {
        "type": workout_type,
        "duration": duration,
        "description": f"A {duration}-minute {workout_type.lower()} workout focused on {fitness_goal.lower()}",
        "exercises": []
    }

    # Determine exercise pool based on available equipment
    exercise_pool = []
    
    # Always include bodyweight exercises
    bodyweight_exercises = [(name, details) for name, details in EXERCISES["bodyweight"].items()]
    exercise_pool.extend(bodyweight_exercises)
    print(f"\nAdded bodyweight exercises to pool: {[name for name, _ in bodyweight_exercises]}")
    
    # Add equipment exercises if equipment is available and not bodyweight only
    if available_equipment and not any(eq.lower() == "bodyweight only" for eq in available_equipment):
        equipment_exercises = []
        for name, details in EXERCISES["equipment"].items():
            required_equipment = details["equipment"].split(", ")
            if all(any(req.lower() in eq.lower() for eq in available_equipment) for req in required_equipment):
                equipment_exercises.append((name, details))
        exercise_pool.extend(equipment_exercises)
        print(f"Added equipment exercises to pool: {[name for name, _ in equipment_exercises]}")

    print(f"\nTotal exercise pool size: {len(exercise_pool)}")

    # Filter exercises based on workout type and fitness goal
    filtered_exercises = [
        (name, details) for name, details in exercise_pool
        if workout_type in details["type"] and fitness_goal in details["fitness_goals"]
    ]
    print(f"\nExercises matching both workout type and fitness goal: {[name for name, _ in filtered_exercises]}")

    # Further filter by experience level
    if filtered_exercises:
        filtered_exercises = [
            (name, details) for name, details in filtered_exercises
            if experience_level in details["difficulty"]
        ]
        print(f"\nExercises matching experience level: {[name for name, _ in filtered_exercises]}")

    # Calculate number of exercises based on duration
    num_exercises = max(2, duration // 15)  # Minimum 2 exercises
    print(f"\nAttempting to select {num_exercises} exercises")

    # Select exercises
    if filtered_exercises:
        selected_exercises = random.sample(filtered_exercises, min(num_exercises, len(filtered_exercises)))
        print(f"Selected exercises: {[name for name, _ in selected_exercises]}")
        
        # Generate workout structure
        for name, details in selected_exercises:
            exercise = {
                "name": name,
                "sets": 3,  # Default for all exercise types
                "reps": "12-15 reps",  # Only strength training exercises remain
                "rest": 60,  # Standard rest for strength training
                "targetMuscle": details["target"],
                "equipment": details["equipment"],
                "instructions": details["instructions"],
                "formTips": details["form_tips"]
            }
            workout["exercises"].append(exercise)
        
        return workout
    else:
        print("\nNo exercises found after all filtering steps!")
        return None