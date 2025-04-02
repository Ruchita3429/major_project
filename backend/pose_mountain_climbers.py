import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import time

def mountain_climbers(socketio=None, exercise_data=None, exercise_type=None):
    print("Starting Mountain Climbers pose detection...")
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0  # 0: waiting for knee to chest, 1: waiting for leg to extend
    active_leg = 'right'  # Alternating between right and left leg
    form = 0
    feedback = "GET INTO PLANK POSITION"
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
                # Track key body angles
                left_hip = detector.findAngle(img, 11, 23, 25)  # Left hip angle
                right_hip = detector.findAngle(img, 12, 24, 26)  # Right hip angle
                left_knee = detector.findAngle(img, 23, 25, 27)  # Left knee angle
                right_knee = detector.findAngle(img, 24, 26, 28)  # Right knee angle
                spine_angle = detector.findAngle(img, 7, 11, 23)  # Upper spine to hip angle
                
                # Check if in proper plank position
                if spine_angle > 160:
                    form = 1
                    if "Get into proper plank position" in form_tips:
                        form_tips.remove("Get into proper plank position")
                else:
                    form = 0
                    if "Get into proper plank position" not in form_tips:
                        form_tips.append("Get into proper plank position")
                
                # Track mountain climbers movement
                if form == 1:
                    # Right leg movement (knee to chest)
                    if active_leg == 'right':
                        # Calculate percentage of knee movement toward chest
                        knee_progress = np.interp(right_knee, (170, 90), (0, 100))
                        # Visual progress bar
                        bar = np.interp(right_knee, (170, 90), (380, 50))
                        
                        if direction == 0:  # Waiting for knee to chest
                            feedback = "BRING RIGHT KNEE TO CHEST"
                            if right_knee < 100 and right_hip < 100:  # Knee is close to chest
                                direction = 1
                                if "Bring your knee closer to your chest" in form_tips:
                                    form_tips.remove("Bring your knee closer to your chest")
                            else:
                                if "Bring your knee closer to your chest" not in form_tips and right_knee > 120:
                                    form_tips.append("Bring your knee closer to your chest")
                                    
                        elif direction == 1:  # Waiting for leg to extend
                            feedback = "EXTEND RIGHT LEG"
                            if right_knee > 160 and right_hip > 160:  # Leg is extended
                                direction = 0
                                active_leg = 'left'  # Switch to left leg
                                count += 0.5  # Half a rep completed
                                # Update the global count for this exercise
                                if exercise_data and exercise_type:
                                    exercise_data[exercise_type]['count'] = int(count)
                            else:
                                if "Extend your leg fully" not in form_tips and right_knee < 150:
                                    form_tips.append("Extend your leg fully")
                                    
                    # Left leg movement
                    elif active_leg == 'left':
                        # Calculate percentage of knee movement toward chest
                        knee_progress = np.interp(left_knee, (170, 90), (0, 100))
                        # Visual progress bar
                        bar = np.interp(left_knee, (170, 90), (380, 50))
                        
                        if direction == 0:  # Waiting for knee to chest
                            feedback = "BRING LEFT KNEE TO CHEST"
                            if left_knee < 100 and left_hip < 100:  # Knee is close to chest
                                direction = 1
                                if "Bring your knee closer to your chest" in form_tips:
                                    form_tips.remove("Bring your knee closer to your chest")
                            else:
                                if "Bring your knee closer to your chest" not in form_tips and left_knee > 120:
                                    form_tips.append("Bring your knee closer to your chest")
                                    
                        elif direction == 1:  # Waiting for leg to extend
                            feedback = "EXTEND LEFT LEG"
                            if left_knee > 160 and left_hip > 160:  # Leg is extended
                                direction = 0
                                active_leg = 'right'  # Switch back to right leg
                                count += 0.5  # Another half rep completed
                                # Update the global count for this exercise
                                if exercise_data and exercise_type:
                                    exercise_data[exercise_type]['count'] = int(count)
                            else:
                                if "Extend your leg fully" not in form_tips and left_knee < 150:
                                    form_tips.append("Extend your leg fully")
                
                # Check for core engagement
                if form == 1 and spine_angle < 170:
                    if "Keep your core tight throughout the movement" not in form_tips:
                        form_tips.append("Keep your core tight throughout the movement")
                
                # Update exercise data
                if exercise_data and exercise_type:
                    exercise_data[exercise_type]['status'] = feedback
                    exercise_data[exercise_type]['form_tips'] = form_tips
                
                # Draw Bar if in proper form
                if form == 1:
                    cv2.rectangle(img, (1080, 50), (1100, 380), (0, 255, 0), 3)
                    cv2.rectangle(img, (1080, int(bar)), (1100, 380), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(knee_progress)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
                
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