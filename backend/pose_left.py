import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import time

def left_curl(socketio=None, exercise_data=None, exercise_type=None):
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "LOWER YOUR ARM"
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
                elbow = detector.findAngle(img, 11, 13, 15)
                shoulder = detector.findAngle(img, 13, 11, 23)

                #Percentage of success of curl
                per = np.interp(elbow, (40, 160), (100, 0))
                
                #Bar to show curl progress
                bar = np.interp(elbow, (40, 160), (50, 380))

                #Check to ensure right form before starting the program
                if shoulder < 40:
                    form = 1
                    if "Keep your shoulder stable" in form_tips:
                        form_tips.remove("Keep your shoulder stable")
                else:
                    if "Keep your shoulder stable" not in form_tips:
                        form_tips.append("Keep your shoulder stable")

                #Check for full range of motion for the pushup
                if form == 1:
                    if per == 0:
                        if elbow > 160 and shoulder < 40:
                            feedback = "UP"
                            if direction == 0:
                                count += 0.5
                                direction = 1
                                # Update the global count for this exercise
                                if exercise_data and exercise_type:
                                    exercise_data[exercise_type]['count'] = int(count)
                        else:
                            feedback = "LOWER YOUR ARM"
                            if "Extend your arm fully" not in form_tips and elbow <= 160:
                                form_tips.append("Extend your arm fully")
                            
                    if per == 100:
                        if elbow < 40 and shoulder < 40:
                            feedback = "DOWN"
                            if direction == 1:
                                count += 0.5
                                direction = 0
                                # Update the global count for this exercise
                                if exercise_data and exercise_type:
                                    exercise_data[exercise_type]['count'] = int(count)
                        else:
                            feedback = "LOWER YOUR ARM"
                            if "Curl your arm completely" not in form_tips and elbow >= 40:
                                form_tips.append("Curl your arm completely")

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