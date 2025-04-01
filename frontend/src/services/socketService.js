import { io } from 'socket.io-client';

class SocketService {
  constructor() {
    this.socket = null;
    this.backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
  }

  connect() {
    this.socket = io(this.backendUrl);
    
    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error);
    });
  }

  subscribeToExerciseUpdates(exerciseType, callbacks) {
    if (!this.socket) this.connect();

    this.socket.emit('join-exercise', { type: exerciseType });
    console.log(`Joining exercise room: ${exerciseType}`);

    this.socket.on('exercise-update', (data) => {
      console.log('Received form tips update:', data);
      if (callbacks.onUpdate) callbacks.onUpdate(data);
    });

    this.socket.on('exercise-count', (data) => {
      console.log('Received count update:', data);
      if (callbacks.onCount) callbacks.onCount(data);
    });

    this.socket.on('exercise-status', (data) => {
      console.log('Received status update:', data);
      if (callbacks.onStatus) callbacks.onStatus(data);
    });
  }

  unsubscribeFromExerciseUpdates() {
    if (this.socket) {
      this.socket.emit('leave-exercise');
      this.socket.off('exercise-update');
      this.socket.off('exercise-count');
      this.socket.off('exercise-status');
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }
}

export default new SocketService(); 