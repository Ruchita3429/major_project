import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import time

def yoga_blocks(socketio=None, exercise_data=None, exercise_type=None):
    print("Starting Yoga with Blocks pose detection...")
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    pose = 0  # Track current yoga pose: 0-initial, 1-triangle, 2-half-moon, 3-bridge
    hold_timer = 0
    pose_start_time = time.time()
    required_hold_time = 5  # 5 seconds per pose
    feedback = "Start in Mountain Pose"
    form_tips = []
    
    with detector.pose:
        while True:
            ret, img = cap.read()
            
            if not ret:
                print("Failed to grab frame from camera")
                continue
                
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            
            if len(lmList) != 0:
                # Key joint angles for yoga poses
                left_hip = detector.findAngle(img, 11, 23, 25)  # Left hip angle
                right_hip = detector.findAngle(img, 12, 24, 26)  # Right hip angle
                left_knee = detector.findAngle(img, 23, 25, 27)  # Left knee angle
                right_knee = detector.findAngle(img, 24, 26, 28)  # Right knee angle
                spine_angle = detector.findAngle(img, 11, 23, 25)  # Spine angle
                
                # Mountain pose detection (initial position)
                if pose == 0:
                    # Check for mountain pose form
                    if left_knee > 160 and right_knee > 160 and left_hip > 160 and right_hip > 160:
                        current_time = time.time()
                        
                        # Initialize timer for first pose
                        if hold_timer == 0:
                            pose_start_time = current_time
                            hold_timer = 1
                            feedback = "Hold Mountain Pose"
                        
                        # Check if held mountain pose long enough
                        if hold_timer == 1 and current_time - pose_start_time >= required_hold_time:
                            pose = 1  # Progress to next pose
                            hold_timer = 0
                            feedback = "Move to Triangle Pose with Block"
                            form_tips = ["Place block outside your forward foot", 
                                        "Extend your arm toward the block"]
                    else:
                        hold_timer = 0
                        if left_knee <= 160 or right_knee <= 160:
                            form_tips = ["Straighten your knees in Mountain Pose"]
                        elif left_hip <= 160 or right_hip <= 160:
                            form_tips = ["Stand tall with hips aligned"]
                
                # Triangle pose with block
                elif pose == 1:
                    # Check for triangle pose form (simplified - in reality would need more angles)
                    if ((left_hip < 120 and right_hip > 160) or (right_hip < 120 and left_hip > 160)) and left_knee > 150 and right_knee > 150:
                        current_time = time.time()
                        
                        if hold_timer == 0:
                            pose_start_time = current_time
                            hold_timer = 1
                            feedback = "Hold Triangle Pose - Use Block for Support"
                            if "Place the block beneath your lower hand" not in form_tips:
                                form_tips = ["Place the block beneath your lower hand", 
                                            "Keep both legs straight", 
                                            "Stack your shoulders"]
                        
                        # Check if held triangle pose long enough
                        if hold_timer == 1 and current_time - pose_start_time >= required_hold_time:
                            pose = 2  # Progress to next pose
                            hold_timer = 0
                            feedback = "Transition to Half Moon Pose with Block"
                            form_tips = ["Place block under supporting hand", 
                                        "Slowly lift back leg parallel to floor"]
                    else:
                        hold_timer = 0
                        if left_knee <= 150 or right_knee <= 150:
                            form_tips = ["Keep your legs straight in Triangle Pose", 
                                        "Use block for stability without bending knees"]
                
                # Half Moon pose with block
                elif pose == 2:
                    # Check for half moon pose (one leg raised)
                    if ((left_knee > 150 and right_knee > 150 and left_hip > 160) or 
                        (left_knee > 150 and right_knee > 150 and right_hip > 160)):
                        current_time = time.time()
                        
                        if hold_timer == 0:
                            pose_start_time = current_time
                            hold_timer = 1
                            feedback = "Hold Half Moon Pose - Block Under Hand"
                            form_tips = ["Gaze at the top hand", 
                                        "Keep standing leg strong", 
                                        "Hips stacked and square to side"]
                        
                        # Check if held half moon pose long enough
                        if hold_timer == 1 and current_time - pose_start_time >= required_hold_time:
                            pose = 3  # Progress to next pose
                            hold_timer = 0
                            feedback = "Move to Bridge Pose with Block"
                            form_tips = ["Lie on back, knees bent", 
                                        "Place block under sacrum for support"]
                    else:
                        hold_timer = 0
                        form_tips = ["Engage your core in Half Moon Pose", 
                                    "Keep block under hand for balance"]
                
                # Bridge pose with block
                elif pose == 3:
                    # Check for bridge pose (knees bent, hips raised)
                    if left_knee < 120 and right_knee < 120:
                        current_time = time.time()
                        
                        if hold_timer == 0:
                            pose_start_time = current_time
                            hold_timer = 1
                            feedback = "Hold Bridge Pose - Block Under Sacrum"
                            form_tips = ["Press feet into floor", 
                                        "Rest weight on shoulders and feet", 
                                        "Let block support your lower back"]
                        
                        # Check if held bridge pose long enough
                        if hold_timer == 1 and current_time - pose_start_time >= required_hold_time:
                            pose = 0  # Return to first pose
                            hold_timer = 0
                            count += 1  # Completed one full sequence
                            feedback = "Sequence Complete! Return to Mountain Pose"
                            form_tips = ["Stand tall", "Breathe deeply"]
                            
                            # Update the global count for this exercise
                            if exercise_data and exercise_type:
                                exercise_data[exercise_type]['count'] = int(count)
                    else:
                        hold_timer = 0
                        form_tips = ["Bend knees at 90 degrees for Bridge Pose", 
                                    "Rest sacrum on block for support"]
                
                # Update exercise data
                if exercise_data and exercise_type:
                    exercise_data[exercise_type]['status'] = feedback
                    exercise_data[exercise_type]['form_tips'] = form_tips
                
                # Calculate and display hold time progress
                if hold_timer == 1:
                    hold_progress = min(100, ((time.time() - pose_start_time) / required_hold_time) * 100)
                    # Draw hold time progress bar
                    bar_value = np.interp(hold_progress, (0, 100), (380, 50))
                    cv2.rectangle(img, (1080, 50), (1100, 380), (0, 255, 0), 3)
                    cv2.rectangle(img, (1080, int(bar_value)), (1100, 380), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(hold_progress)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
                
                # Display pose number
                cv2.rectangle(img, (0, 0), (600, 40), (245, 117, 16), -1)
                cv2.putText(img, f'Pose: {pose+1}/4 - Hold: {int(min(required_hold_time, time.time() - pose_start_time if hold_timer == 1 else 0))}s', 
                          (15, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                
                # Exercise counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
                
                # Feedback display
                cv2.putText(img, feedback, (500, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
            
            # Convert frame to JPEG (fixed indentation to match pose_left.py)
            ret, jpeg = cv2.imencode('.jpg', img)
            
            # Yield the frame as bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n') 