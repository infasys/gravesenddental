import socketio,json,threading
from PyQt5 import QtCore

class ListenWebsocket(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(str,int,dict)
    def __init__(self, parent=None):
        super(ListenWebsocket, self).__init__(parent)
        self._lock = threading.Lock()
        # self.sio = socketio.Client()
        self.sio = socketio.Client(logger=True, engineio_logger=True)
        try:
            self.sio.connect('https://socketgravesend.tahid.co.uk')
        except socketio.exceptions.ConnectionError as err:
            print("ConnectionError: %s", err)
        @self.sio.event
        def connect():
            print("I'm connected!")
        @self.sio.event
        def connect_error(data):
            print("The connection failed!")
        @self.sio.event
        def disconnect():
            print("I'm disconnected!")

        @self.sio.on('chat message')
        def message(data):
            if isinstance(data, dict):
                # print(json.dumps(data))
                # print(json.dumps(data['msg']))
                self.any_signal.emit(data['msg'],data['type'],data)
            if isinstance(data, str):
                self.any_signal.emit(data,1,data)
        @self.sio.on('*')
        def catch_all(event, data):
            # print(data)
            pass
        print('my sid is', self.sio.sid)
    def sendmsg(self,msg):
        # try:
            self.sio.emit('chat message',msg)
        # except socketio.exceptions.BadNamespaceError as err:
        #     print("BadNamespaceError")
    def _do_before_done(self):
        print('waiting 3 seconds before thread done..')
        for i in range(3, 0, -1):
            print('{0} seconds left...'.format(i))
            self.sleep(1)
        self.sio.disconnect()
        print('ok, thread done.')
    def stop(self):
        print('received stop signal from window.')
        with self._lock:
            self._do_before_done()