import streamlit as st
import cv2
import os

# Ensure the directory exists for storing images
if not os.path.exists("TrainingImage"):
    os.makedirs("TrainingImage")

# Streamlit Title
st.title("Simple Attendance System")

# Input fields
enrollment = st.text_input("Enter Enrollment:", "")
name = st.text_input("Enter Name:", "")

# Notification message placeholder
notification = st.empty()

# Function to capture and save images
def take_img(enrollment, name):
    if enrollment == "" or name == "":
        notification.error("Enrollment & Name are required!")
        return

    # Open webcam
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    sampleNum = 0
    
    st.write("Press 'q' to stop capturing images.")
    while True:
        ret, img = cam.read()
        if not ret:
            st.error("Failed to open camera!")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum += 1
            # Save the captured face image
            cv2.imwrite(f"TrainingImage/{name}.{enrollment}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Display the camera feed
        st.image(img, channels="BGR", caption="Capturing Images...")
        
        # Stop when 'q' is pressed or 10 images are captured
        if cv2.waitKey(1) & 0xFF == ord('q') or sampleNum >= 10:
            break

    cam.release()
    cv2.destroyAllWindows()
    notification.success(f"Images captured and saved for Enrollment: {enrollment}, Name: {name}")

# Button to trigger image capture
if st.button("Capture Images"):
    take_img(enrollment, name)
