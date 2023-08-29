from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)


edge_detection_active = False

def generate_frames():
    camera = cv2.VideoCapture(0)
    global edge_detection_active

    while True:
        ret, frame = camera.read()
        frame=cv2.flip(frame,1)
        if not ret:
            break

        if edge_detection_active:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur=cv2.GaussianBlur(gray,(5,5),5)

            canny = cv2.Canny(blur, 30, 100)
            frame = canny

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/toggle_edge_detection")
def toggle_edge_detection():
    global edge_detection_active
    edge_detection_active = not edge_detection_active
    return "Edge Detection Enabled" if edge_detection_active else "Edge Detection Disabled"

@app.route("/camera_feed")
def camera_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
