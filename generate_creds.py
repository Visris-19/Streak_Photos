from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Will open a browser for Google login
gauth.SaveCredentialsFile("mycreds.txt")
print("Credentials saved to mycreds.txt. You can now run the app.")