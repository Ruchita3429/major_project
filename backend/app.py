from flask import Flask, render_template, Response, request, redirect, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from pose_left import left_curl
from pose_right import right_curl
from pose_pushup import pushup
from pose_squat import squat
from pose_yoga_sun import sun_salutation
from pose_mountain_climbers import mountain_climbers
from pose_jump_rope import jump_rope
from pose_yoga_blocks import yoga_blocks
import cv2
import mediapipe as mp
import numpy as np
import threading
import time
from workout_generator import generate_workout

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables to track counts for each exercise
exercise_data = {
    'left-bicep': {'count': 0, 'status': 'Ready to start', 'form_tips': []},
    'right-bicep': {'count': 0, 'status': 'Ready to start', 'form_tips': []},
    'pushup': {'count': 0, 'status': 'Ready to start', 'form_tips': []},
    'squat': {'count': 0, 'status': 'Ready to start', 'form_tips': []},
    'sun-salutation': {'count': 0, 'status': 'Ready to start', 'form_tips': []},
    'mountain-climbers': {'count': 0, 'status': 'Ready to start', 'form_tips': []},
    'jump-rope': {'count': 0, 'status': 'Ready to start', 'form_tips': []},
    'yoga-blocks': {'count': 0, 'status': 'Ready to start', 'form_tips': []}
}

# Thread to update frontend with counts
def send_exercise_updates():
    while True:
        for exercise_type, data in exercise_data.items():
            socketio.emit('exercise-count', {'count': data['count']}, room=exercise_type)
            socketio.emit('exercise-status', {'status': data['status']}, room=exercise_type)
            if data['form_tips']:
                socketio.emit('exercise-update', {'formTips': data['form_tips']}, room=exercise_type)
        time.sleep(0.5)  # Send updates every 0.5 seconds

# Start the update thread
update_thread = threading.Thread(target=send_exercise_updates, daemon=True)
update_thread.start()

@app.route('/api', methods = ['GET'])
def index():
    return render_template('request_page.html')

@app.route('/video_feed_left')
def video_feed_left():
    # Pass the socketio instance and exercise type to the curl function
    return Response(left_curl(socketio, exercise_data, 'left-bicep'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_right')
def video_feed_right():
    return Response(right_curl(socketio, exercise_data, 'right-bicep'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_pushup')
def video_feed_pushup():
    return Response(pushup(socketio, exercise_data, 'pushup'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_squat')
def video_feed_squat():
    return Response(squat(socketio, exercise_data, 'squat'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_sun_salutation')
def video_feed_sun_salutation():
    return Response(sun_salutation(socketio, exercise_data, 'sun-salutation'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_mountain_climbers')
def video_feed_mountain_climbers():
    return Response(mountain_climbers(socketio, exercise_data, 'mountain-climbers'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_jump_rope')
def video_feed_jump_rope():
    return Response(jump_rope(socketio, exercise_data, 'jump-rope'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_yoga_blocks')
def video_feed_yoga_blocks():
    return Response(yoga_blocks(socketio, exercise_data, 'yoga-blocks'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/show')
def show():
    subject = request.args.get('sub')
    return redirect(f'/video_feed_{subject}')

@app.route('/api/generate-workout', methods=['POST'])
def create_workout():
    data = request.json
    try:
        workout = generate_workout(
            fitness_goal=data['fitnessGoal'],
            available_equipment=data['availableEquipment'],
            duration=data['duration'],
            experience_level=data['experienceLevel'],
            workout_type=data['workoutType'],
            restrictions=data.get('restrictions', [])
        )
        return jsonify(workout)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join-exercise')
def handle_join_exercise(data):
    exercise_type = data.get('type')
    if exercise_type:
        join_room(exercise_type)
        # Send initial data
        socketio.emit('exercise-count', {'count': exercise_data[exercise_type]['count']}, room=exercise_type)
        socketio.emit('exercise-status', {'status': exercise_data[exercise_type]['status']}, room=exercise_type)
        print(f'Client joined exercise room: {exercise_type}')

@socketio.on('leave-exercise')
def handle_leave_exercise():
    for room in socketio.server.rooms(request.sid):
        if room != request.sid:
            leave_room(room)
            print(f'Client left exercise room: {room}')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=False)