from flask import Flask, render_template, Response, request, redirect
from pose_left import left_curl
from pose_right import right_curl
from pose_pushup import pushup
from pose_squat import squat
import cv2
import mediapipe as mp
import numpy as np
from websocket_handler import init_socketio, process_exercise_feed
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__)
init_socketio(app)

def generate_frames(exercise_type):
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Process frame and send WebSocket updates
            processed_frame = process_exercise_feed(exercise_type, frame)
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)  # Add small delay to prevent overwhelming the system

@app.route('/api', methods = ['GET'])
def index():
    return render_template('request_page.html')

@app.route('/video_feed_left')
def video_feed_left():
    return Response(generate_frames('left-bicep'),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_right')
def video_feed_right():
    return Response(generate_frames('right-bicep'),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_pushup')
def video_feed_pushup():
    return Response(generate_frames('pushup'),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_squat')
def video_feed_squat():
    return Response(generate_frames('squat'),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/show')
def show():
    subject = request.args.get('sub')
    return redirect(f'/video_feed_{subject}')

if __name__ == '__main__':
    app.run(host = "0.0.0.0" , debug=False)