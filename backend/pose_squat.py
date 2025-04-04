import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import time

def squat(socketio=None, exercise_data=None, exercise_type=None):
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "STRAIGHTEN YOUR BACK"
    last_emit_time = 0
    form_tips = []

    with detector.pose:
        while True:
                
            ret, img = cap.read() #640 x 480

            if not ret:
                continue

            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            
            if len(lmList) != 0:
                shoulder = detector.findAngle(img, 7, 11, 23)
                knee = detector.findAngle(img, 23, 25, 27)
                
                #Percentage of success of pushup
                per = np.interp(knee, (90, 160), (0, 100))
                
                #Bar to show Pushup progress
                bar = np.interp(knee, (90, 160), (380, 50))

                #Check to ensure right form before starting the program
                if shoulder > 160:
                    form = 1
                    if "Keep your back straight" in form_tips:
                        form_tips.remove("Keep your back straight")
                else:
                    if "Keep your back straight" not in form_tips:
                        form_tips.append("Keep your back straight")
            
                #Check for full range of motion for the pushup
                if form == 1:
                    if per == 0:
                        if knee <= 90 and shoulder > 160:
                            feedback = "UP"
                            if direction == 0:
                                count += 0.5
                                direction = 1
                                # Update the global count for this exercise
                                if exercise_data and exercise_type:
                                    exercise_data[exercise_type]['count'] = int(count)
                        else:
                            feedback = "STRAIGHTEN YOUR BACK"
                            if shoulder <= 160 and "Keep your back straight during the squat" not in form_tips:
                                form_tips.append("Keep your back straight during the squat")
                            if knee > 90 and "Squat lower" not in form_tips:
                                form_tips.append("Squat lower")
                            
                    if per == 100:
                        if shoulder > 160 and knee > 160:
                            feedback = "DOWN"
                            if direction == 1:
                                count += 0.5
                                direction = 0
                                # Update the global count for this exercise
                                if exercise_data and exercise_type:
                                    exercise_data[exercise_type]['count'] = int(count)
                        else:
                            feedback = "STRAIGHTEN YOUR BACK"
                            if shoulder <= 160 and "Keep your back straight while standing" not in form_tips:
                                form_tips.append("Keep your back straight while standing")
                            if knee <= 160 and "Stand up fully" not in form_tips:
                                form_tips.append("Stand up fully")

                # Update exercise data
                if exercise_data and exercise_type:
                    exercise_data[exercise_type]['status'] = feedback
                    exercise_data[exercise_type]['form_tips'] = form_tips
                
                #Draw Bar
                if form == 1:
                    cv2.rectangle(img, (1080, 50), (1100, 380), (0, 255, 0), 3)
                    cv2.rectangle(img, (1080, int(bar)), (1100, 380), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(per)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 0), 2)


                #Pushup counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                            (255, 0, 0), 5)
                
                #Feedback 
                cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 255, 0), 2)

                
            # Convert the frame to JPEG format
                ret, jpeg = cv2.imencode('.jpg', img)

                # Yield the frame as a bytes-like object
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')