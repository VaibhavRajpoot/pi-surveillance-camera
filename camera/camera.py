import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, request
import time

video = cv2.VideoCapture(0)
app = Flask('__name__',template_folder='template')


def video_stream():
    while True:
        framec=0
        ret, frame = video.read()
        stime=time.time()
        if not ret:
            break
        elif(int(time.time()%15)== 0):              #if the time is a multiple of 3600 seconds
            path=time.ctime(stime)
            out = cv2.VideoWriter(path+'.avi',cv2.VideoWriter_fourcc(*'XVID'), 2.0, (640, 480))
            ftime=int(stime)+5
            while(int(time.time())<=ftime):
                print("entered inside loop",time.ctime(time.time()))
                ret1, frame1 = video.read() 
                ret1, buffer1 = cv2.imencode('.jpeg',frame1)
                frame2 = buffer1.tobytes()
                out.write(frame1)
                cv2.waitKey(1)
                framec=framec+1
                yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame2 +b'\r\n')
                
            out.release()

        else:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')
        print("entered outside loop",time.ctime(time.time()),"framec",framec)


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port='5000', debug=False)
