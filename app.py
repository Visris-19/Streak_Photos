import streamlit as st
import cv2
import uuid
import os
import time
import tempfile
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- SET YOUR GOOGLE DRIVE FOLDER ID ---
DRIVE_FOLDER_ID = "1DSIzYoZ8oTMrj35656bRCXRyqqQWeukU"  # Replace with your folder ID

# --- Google Drive service using service account ---
@st.cache_resource
def get_drive_service():
    service_account_info = json.loads(st.secrets["google_service_account"]["json"])
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(file_path, folder_id):
    service = get_drive_service()
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')

# --- Streamlit UI ---
st.title("📸 Face Dataset Collector")
st.write("Capture multiple photos in a streak for training data.")

num_images = st.number_input("How many photos to capture?", min_value=1, max_value=50, value=10, step=1)
capture_btn = st.button("Capture Multiple Photos")
upload_btn = st.button("Upload to Google Drive")

# Store image paths
if "images" not in st.session_state:
    st.session_state.images = []

# --- Capture Multiple Photos ---
if capture_btn:
    st.session_state.images.clear()
    cap = cv2.VideoCapture(0)
    st.info("Capturing photos...")
    for i in range(num_images):
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to read from camera.")
            break
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(tempfile.gettempdir(), filename)
        cv2.imwrite(filepath, frame)
        st.session_state.images.append(filepath)
        st.image(frame, caption=f"Photo {i+1}", channels="BGR", width=150)
        time.sleep(0.3)  # small delay between shots
    cap.release()
    st.success(f"Captured {len(st.session_state.images)} photos.")

# --- Upload to Drive ---
if upload_btn:
    if not st.session_state.images:
        st.warning("No photos to upload.")
    else:
        for path in st.session_state.images:
            try:
                file_id = upload_file_to_drive(path, DRIVE_FOLDER_ID)
                st.success(f"Uploaded: {os.path.basename(path)} (ID: {file_id})")
            except Exception as e:
                st.error(f"Failed to upload {path}: {e}")
