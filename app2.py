from BackendModule import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=False, port=6002)
