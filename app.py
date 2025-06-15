import streamlit as st
import os
import tempfile
import uuid
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- Google Drive Setup ---
DRIVE_FOLDER_ID = "1DSIzYoZ8oTMrj35656bRCXRyqqQWeukU"

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
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# --- UI ---
st.title("📸 Upload Face Photos for Training")
st.write("Take multiple photos with your phone camera, or choose from gallery, then upload them here.")

uploaded_files = st.file_uploader("📤 Upload multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} photo(s) uploaded.")
    uploaded_paths = []

    for file in uploaded_files:
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(tempfile.gettempdir(), filename)
        with open(filepath, "wb") as f:
            f.write(file.read())
        uploaded_paths.append(filepath)
        st.image(filepath, width=200)

    if st.button("Upload to Google Drive"):
        for path in uploaded_paths:
            try:
                file_id = upload_file_to_drive(path, DRIVE_FOLDER_ID)
                st.success(f"Uploaded: {os.path.basename(path)} (ID: {file_id})")
            except Exception as e:
                st.error(f"Failed to upload {os.path.basename(path)}: {e}")
