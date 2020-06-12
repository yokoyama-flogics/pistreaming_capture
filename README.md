# OpenCV Video Capturing for 'pistreaming'

This is a trivial but helpful (I believe) framework for [pistreaming](https://github.com/waveform80/pistreaming) users, which runs Linux.
Hopefully, runs on Raspberry Pi too.

Simply connect to pistreaming server by websocket, synchronize to MPEG stream boundary, and pipe to OpenCV VideoCapture().

You can write your own great image processing or intruder detection algorithm on it.

## Requirements

You need Python3 and also following software.

- [websocket_client](https://pypi.org/project/websocket_client/)
- [OpenCV](https://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html)

## Usage

Please edit 'capture.py' and find line starting "STREAM".
If your pistreaming server is 'foo.bar.com', the line should be

```python
STREAM = "ws://foo.bar.com:8084"
```

If you changed ```WS_PORT = 8084``` in server.py, you also need to change the port number.

Atsushi Yokoyama, Firmlogics
