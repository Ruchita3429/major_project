import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import time

def jump_rope(socketio=None, exercise_data=None, exercise_type=None):
    print("Starting Jump Rope pose detection...")
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    jump_phase = 0  # 0: waiting for jump, 1: in air, need to land
    last_check_time = time.time()
    jump_timer = time.time()
    feedback = "READY TO START JUMPING"
    form_tips = []
    jumps_per_sec = 0
    last_jumps = []  # Track recent jumps for rate calculation
    
    with detector.pose:
        while True:
            ret, img = cap.read()
            
            if not ret:
                print("Failed to grab frame from camera")
                continue
                
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            
            if len(lmList) != 0:
                # Track key body points
                ankle_y = (lmList[27][2] + lmList[28][2]) / 2  # Average Y position of ankles
                hip_y = (lmList[23][2] + lmList[24][2]) / 2    # Average Y position of hips
                knee_y = (lmList[25][2] + lmList[26][2]) / 2   # Average Y position of knees
                
                # Calculate leg extension percentage (for jump detection)
                leg_extension = hip_y - knee_y  # Distance between hips and knees
                jump_progress = 100  # Default value
                
                # Check for proper jump rope form
                left_elbow = detector.findAngle(img, 11, 13, 15)  # Left elbow angle
                right_elbow = detector.findAngle(img, 12, 14, 16)  # Right elbow angle
                
                # Check arm position for proper jump rope form
                if left_elbow > 70 and left_elbow < 120 and right_elbow > 70 and right_elbow < 120:
                    if "Keep elbows close to body" in form_tips:
                        form_tips.remove("Keep elbows close to body")
                else:
                    if "Keep elbows close to body" not in form_tips:
                        form_tips.append("Keep elbows close to body")
                
                # Jump detection logic
                current_time = time.time()
                
                # Reset jump phase if taking too long
                if jump_phase == 1 and current_time - jump_timer > 1.0:  # If more than 1 second in air, reset
                    jump_phase = 0
                    
                if jump_phase == 0:  # Looking for a jump
                    # Calculate previous ankle position - current position to detect upward movement
                    if 'prev_ankle_y' in locals():
                        ankle_movement = prev_ankle_y - ankle_y
                        knee_to_ankle = knee_y - ankle_y
                        
                        # Jump detected if there's significant upward movement
                        if ankle_movement > 15 and knee_to_ankle > 50:
                            jump_phase = 1
                            jump_timer = current_time
                            feedback = "IN THE AIR"
                            if "Jump just high enough to clear the rope" not in form_tips:
                                form_tips.append("Jump just high enough to clear the rope")
                    
                elif jump_phase == 1:  # Looking for landing
                    # Calculate previous ankle position - current position to detect downward movement
                    if 'prev_ankle_y' in locals():
                        ankle_movement = ankle_y - prev_ankle_y
                        
                        # Landing detected
                        if ankle_movement > 10:
                            count += 1
                            jump_phase = 0
                            feedback = "GOOD JUMP"
                            
                            # Calculate jumps per second
                            last_jumps.append(current_time)
                            # Keep only last 10 jumps for rate calculation
                            if len(last_jumps) > 10:
                                last_jumps.pop(0)
                            # Calculate rate if we have enough data
                            if len(last_jumps) >= 2:
                                time_diff = last_jumps[-1] - last_jumps[0]
                                if time_diff > 0:
                                    jumps_per_sec = (len(last_jumps) - 1) / time_diff
                            
                            # Update the global count for this exercise
                            if exercise_data and exercise_type:
                                exercise_data[exercise_type]['count'] = int(count)
                
                # Store current ankle position for next frame
                prev_ankle_y = ankle_y
                
                # Check landing mechanics
                if jump_phase == 0 and 'prev_ankle_y' in locals():
                    ankle_movement = ankle_y - prev_ankle_y
                    if ankle_movement > 20:  # Hard landing
                        if "Land softly on the balls of your feet" not in form_tips:
                            form_tips.append("Land softly on the balls of your feet")
                
                # Update exercise data
                if exercise_data and exercise_type:
                    exercise_data[exercise_type]['status'] = feedback
                    exercise_data[exercise_type]['form_tips'] = form_tips
                
                # Draw jump rate indicator
                cv2.rectangle(img, (0, 0), (250, 40), (245, 117, 16), -1)
                cv2.putText(img, f'Rate: {jumps_per_sec:.1f} jumps/sec', (15, 30), 
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
                
                # Exercise counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
                
                # Feedback display
                cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
            
            # Convert frame to JPEG (fixed indentation to match pose_left.py)
            ret, jpeg = cv2.imencode('.jpg', img)
            
            # Yield the frame as bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n') 