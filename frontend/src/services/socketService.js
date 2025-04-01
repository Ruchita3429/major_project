import { io } from 'socket.io-client';

class SocketService {
  constructor() {
    this.socket = null;
  }

  connect() {
    this.socket = io('http://localhost:5000');
    
    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });
  }

  subscribeToExerciseUpdates(exerciseType, callbacks) {
    if (!this.socket) this.connect();

    this.socket.emit('join-exercise', { type: exerciseType });

    this.socket.on('exercise-update', (data) => {
      if (callbacks.onUpdate) callbacks.onUpdate(data);
    });

    this.socket.on('status', (data) => {
      console.log('Status update:', data);
    });
  }

  unsubscribeFromExerciseUpdates() {
    if (this.socket) {
      this.socket.emit('leave-exercise');
      this.socket.off('exercise-update');
      this.socket.off('status');
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