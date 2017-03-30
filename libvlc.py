"""
This module allows control of VLC via its remote console.
"""

import socket


class VLC:
    """Connect to local VLC remote console on port 8888"""
    def __init__(self):
        self.SCREEN_NAME = 'vlc'
        self.HOST = 'localhost'
        self.PORT = 8888
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCK.connect((self.HOST, self.PORT))


    def x(self, cmd):
        """Prepare a command and send it to VLC"""
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)
        return self.SOCK.recv(4096)


    def pause(self):
        """Pause playing"""
        self.x('pause')


    def play(self):
        """Start playing"""
        self.x('play')


    def stop(self):
        """Stop playing"""
        self.x('stop')


    def prev(self):
        """Play previous item"""
        self.x('prev')


    def next(self):
        """Play next item"""
        self.x('next')


    def add(self, path):
        """Add item to playlist"""
        self.x('add %s' % (path,))


    def enqueue(self, path):
        """Enqueue item in playlist"""
        self.x('enqueue %s' % (path,))


    def clear(self):
        """Clear playlist"""
        self.x('clear')


    def shutdown(self):
        """Shutdown VLC"""
        self.x('shutdown')


    def volup(self):
        """Increase volume by 5%"""
        self.x('volup')


    def voldown(self):
        """Decrease volume by 5%"""
        self.x('voldown')


    def volume(self, volume):
        """Set volume to given value"""
        self.x('volume %s' % (volume,))


    def status(self):
        """Return VLC status"""
        return self.x('status')


    def get_title(self):
        """Return current playing item title"""
        status = self.x('status')
        tmp = 'state playing'
        if tmp.encode() in status:
            token = 'new input: '
            title = status.split(token.encode())
            while len(title) != 2:
                status = self.x('status')
                title = status.split(token.encode())
            title = title[1]
            token = ' )\r\n'
            title = title.split(token.encode())
            if len(title) > 1:
                title = title[0]
            else:
                title = ''
        else:
            title = ''
        return str(title)


    def get_volume(self):
        """Return current audio volume (in %)"""
        status = self.x('status')
        token = 'audio volume: '
        volume = status.split(token.encode())
        while len(volume) != 2:
            status = self.x('status')
            volume = status.split(token.encode())
        volume = volume[1]
        token = ' )\r\n'
        volume = volume.split(token.encode())
        if len(volume) > 1:
            volume = float(volume[0])
        else:
            volume = 0
        volume = str(round(volume / 256 * 100, 0)) + '%'
        return volume
