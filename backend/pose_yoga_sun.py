import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import time

def sun_salutation(socketio=None, exercise_data=None, exercise_type=None):
    print("Starting Sun Salutation pose detection...")
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    position = 0  # Track position in the sequence: 0-mountain, 1-raised arms, 2-forward fold, 3-plank, 4-cobra, 5-downward dog
    last_position = 0
    sequence_complete = False
    feedback = "Begin in Mountain Pose"
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
                shoulder_angle = detector.findAngle(img, 13, 11, 23)  # Right shoulder
                hip_angle = detector.findAngle(img, 11, 23, 25)  # Right hip
                knee_angle = detector.findAngle(img, 23, 25, 27)  # Right knee
                ankle_angle = detector.findAngle(img, 25, 27, 31)  # Right ankle
                
                # Mountain pose detection (standing straight)
                if knee_angle > 160 and hip_angle > 160 and shoulder_angle > 80 and shoulder_angle < 110 and not sequence_complete:
                    position = 0
                    feedback = "Raise arms overhead"
                    
                # Arms raised overhead
                elif knee_angle > 160 and hip_angle > 160 and shoulder_angle > 170 and position == 0 and not sequence_complete:
                    position = 1
                    feedback = "Forward fold"
                    
                # Forward fold
                elif knee_angle > 120 and hip_angle < 90 and position == 1 and not sequence_complete:
                    position = 2
                    feedback = "Step back to plank"
                    
                # Plank position
                elif hip_angle > 160 and shoulder_angle > 80 and shoulder_angle < 100 and position == 2 and not sequence_complete:
                    position = 3
                    feedback = "Lower to cobra"
                    
                # Cobra pose
                elif hip_angle < 160 and shoulder_angle < 80 and position == 3 and not sequence_complete:
                    position = 4
                    feedback = "Push up to downward dog"
                    
                # Downward dog
                elif hip_angle < 100 and shoulder_angle > 160 and position == 4 and not sequence_complete:
                    position = 5
                    feedback = "Step forward to forward fold"
                    
                # Back to forward fold
                elif knee_angle > 120 and hip_angle < 90 and position == 5 and not sequence_complete:
                    position = 6
                    feedback = "Rise to mountain pose"
                    
                # Complete sequence by returning to mountain
                elif knee_angle > 160 and hip_angle > 160 and shoulder_angle > 80 and shoulder_angle < 110 and position == 6:
                    sequence_complete = True
                    position = 0
                    count += 1
                    feedback = "Sequence Complete. Great Work!"
                    sequence_complete = False
                    
                    # Update the global count for this exercise
                    if exercise_data and exercise_type:
                        exercise_data[exercise_type]['count'] = int(count)
                
                # Form tips based on position
                form_tips = []
                if position == 0:  # Mountain pose
                    if knee_angle < 160:
                        form_tips.append("Stand tall with knees straight")
                    if hip_angle < 160:
                        form_tips.append("Align hips with spine")
                elif position == 1:  # Arms raised
                    if shoulder_angle < 170:
                        form_tips.append("Reach arms fully overhead")
                elif position == 2:  # Forward fold
                    if hip_angle > 90:
                        form_tips.append("Bend forward from hips")
                elif position == 3:  # Plank
                    if hip_angle < 160:
                        form_tips.append("Keep body in straight line")
                elif position == 4:  # Cobra
                    if shoulder_angle > 80:
                        form_tips.append("Open chest forward")
                elif position == 5:  # Downward dog
                    if hip_angle > 100:
                        form_tips.append("Push hips up and back")
                        
                # Update exercise data
                if exercise_data and exercise_type:
                    exercise_data[exercise_type]['status'] = feedback
                    exercise_data[exercise_type]['form_tips'] = form_tips
                
                # Draw sequence progress indicator
                cv2.rectangle(img, (0, 0), (600, 40), (245, 117, 16), -1)
                cv2.putText(img, f'Position: {position+1}/7', (15, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                
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