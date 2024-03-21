from flask import Flask, Response
import cv2

app = Flask(__name__)

ID = 4

def generate_frames():
    camera = cv2.VideoCapture(ID)  # Use 0 for the primary camera

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 640);
    # Set the format to MJPG
    #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

