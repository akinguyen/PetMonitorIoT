import socketio
sio = socketio.Client()
sio.connect('https://lbhack.herokuapp.com/')
sio.emit('mouse', {'foo': 'bar'})