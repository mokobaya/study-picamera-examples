from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import Response
import os
#from processor.simple_streamer import SimpleStreamer as VideoCamera
# from processor.pedestrian_detector import PedestrianDetector as VideoCamera
from processor.motion_detector import MotionDetector as VideoCamera
import time
import threading

video_camera = VideoCamera(flip=False)


app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'pass1234' and request.form['username'] == 'kanri':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=False, threaded=True)
