from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import mediapipe as mp
from pose_module import PoseDetector
import time

socketio = SocketIO()

def process_exercise_feed(exercise_type, frame):
    detector = PoseDetector()
    img = detector.findPose(frame, draw=False)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        count = 0
        if exercise_type == 'left-bicep':
            # Left bicep curl logic
            angle = detector.findAngle(img, 11, 13, 15)
            if angle > 160:
                count += 0.5
            elif angle < 30:
                count += 0.5
        elif exercise_type == 'right-bicep':
            # Right bicep curl logic
            angle = detector.findAngle(img, 12, 14, 16)
            if angle > 160:
                count += 0.5
            elif angle < 30:
                count += 0.5
        elif exercise_type == 'pushup':
            # Pushup logic
            angle = detector.findAngle(img, 11, 13, 15)
            if angle > 160:
                count += 0.5
            elif angle < 90:
                count += 0.5
        elif exercise_type == 'squat':
            # Squat logic
            angle = detector.findAngle(img, 23, 25, 27)
            if angle > 160:
                count += 0.5
            elif angle < 90:
                count += 0.5

        # Emit updates via WebSocket
        socketio.emit('exercise-update', {
            'count': int(count),
            'status': 'In Progress' if count > 0 else 'Ready to start',
            'formTips': []  # Add form tips based on pose analysis
        }, room=exercise_type)

    return img

def init_socketio(app):
    socketio.init_app(app, cors_allowed_origins="*")

    @socketio.on('join-exercise')
    def handle_join_exercise(data):
        room = data.get('type')
        if room:
            socketio.join_room(room)
            emit('status', {'msg': f'Joined {room}'}, room=room)

    @socketio.on('leave-exercise')
    def handle_leave_exercise():
        socketio.leave_room()
        emit('status', {'msg': 'Left room'}) 