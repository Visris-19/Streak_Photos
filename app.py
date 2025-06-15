from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import streamlit as st
import cv2
import uuid
import os
import zipfile

# Setup folder
IMAGES_PATH = 'collected_images'
ZIP_NAME = 'photos.zip'
os.makedirs(IMAGES_PATH, exist_ok=True)

st.title("📸 Face Photo Collector")
st.write("Click 'Take Photo' to capture from webcam. Then 'Upload to Drive'.")

# Interactive login
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Opens a browser for user to log in
drive = GoogleDrive(gauth)

# Take photo
if st.button("📷 Take Photo"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(IMAGES_PATH, filename)
        cv2.imwrite(filepath, frame)
        st.image(frame, caption="Captured Image", channels="BGR")
        st.success(f"Saved {filename}")
    else:
        st.error("Failed to capture image.")

# Upload
if st.button("☁️ Upload to Google Drive"):
    images = os.listdir(IMAGES_PATH)
    with zipfile.ZipFile(ZIP_NAME, 'w') as zipf:
        for img in images:
            zipf.write(os.path.join(IMAGES_PATH, img), img)
    file_drive = drive.CreateFile({'title': ZIP_NAME})
    file_drive.SetContentFile(ZIP_NAME)
    file_drive.Upload()
    st.success("✅ Uploaded to your Google Drive!")
