import cv2
import os
from datetime import datetime

print("========== TROPAMILYA ATTENDANCE SYSTEM ==========")
# Prompt user for their name
user_name = input("Enter your name: ")

# Create a directory to save the images named with the current date
current_date = datetime.now().strftime('%Y-%m-%d')
output_dir = os.path.join(current_date, user_name)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
image_count = 0
image_size = (256, 256)
font = cv2.FONT_HERSHEY_SIMPLEX
logged_in = False  # Flag to track login status
current_time = ""  # Store time-in value

while True:
    ret, frame = cap.read()

    if not ret:
        print("CAMERA IS FAILED CANT CAPTURE")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))  # Adjust the minSize for larger bounding box

    for (x, y, w, h) in faces:
        face = cv2.resize(gray[y:y + h, x:x + w], image_size)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)  # Increase rectangle thickness to make it more visible

        if logged_in:  # If user is logged in, display Time In above the bounding box
            cv2.putText(frame, f"TIME IN: {current_time}", (x, y - 20), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"NAME: {user_name}", (x, y + h + 30), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    if not logged_in:  # Display options on the video feed only if not logged in
        cv2.putText(frame, "1. Log-in", (20, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Change font color to green
        cv2.putText(frame, "2. Exit", (20, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Change font color to green
    else:  # Display Exit option if user is logged in
        cv2.putText(frame, "2. Exit", (20, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Change font color to green

    key = cv2.waitKey(1)
    if key & 0xFF == ord('1') and not logged_in:  # User login - capturing the image
        image_count += 1
        image_name = os.path.join(output_dir, f"{user_name}_{image_count}.png")  # Image name includes user's name
        cv2.imwrite(image_name, face)  # Save as PNG format

        # Display "Time In" on the video feed
        current_time = datetime.now().strftime('%H:%M:%S')
        logged_in = True
        print(f"Logged in: {user_name} at {current_time}")

    elif key & 0xFF == ord('2'):  # Exiting the loop
        break

    cv2.imshow('Tropamilya Attendance System', frame)

cap.release()
cv2.destroyAllWindows()
