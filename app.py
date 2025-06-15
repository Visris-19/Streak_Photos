import streamlit as st
import uuid
import os
import tempfile
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- SET YOUR GOOGLE DRIVE FOLDER ID ---
DRIVE_FOLDER_ID = "1DSIzYoZ8oTMrj35656bRCXRyqqQWeukU"

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
st.write("Take photos using your camera and upload them to Google Drive.")

# Session state to store captured images
if "images" not in st.session_state:
    st.session_state.images = []

num_photos = st.number_input("How many photos do you want to capture?", min_value=1, max_value=20, value=5)
capture_btn = st.button("Start Capturing")

# Photo capturing loop
if capture_btn:
    st.session_state.images.clear()
    for i in range(num_photos):
        st.write(f"📷 Capture Photo {i+1} of {num_photos}")
        img = st.camera_input(f"Take photo {i+1}")
        if img:
            filename = f"{uuid.uuid4()}.jpg"
            filepath = os.path.join(tempfile.gettempdir(), filename)
            with open(filepath, "wb") as f:
                f.write(img.getbuffer())
            st.session_state.images.append(filepath)
            st.success(f"Captured photo {i+1}")

# Show all captured photos
if st.session_state.images:
    st.subheader("🖼️ Captured Photos")
    for path in st.session_state.images:
        st.image(path, width=200)

# Upload to Drive
if st.button("Upload to Google Drive"):
    if not st.session_state.images:
        st.warning("No photos to upload.")
    else:
        for path in st.session_state.images:
            try:
                file_id = upload_file_to_drive(path, DRIVE_FOLDER_ID)
                st.success(f"Uploaded: {os.path.basename(path)} (ID: {file_id})")
            except Exception as e:
                st.error(f"Failed to upload {os.path.basename(path)}: {e}")
