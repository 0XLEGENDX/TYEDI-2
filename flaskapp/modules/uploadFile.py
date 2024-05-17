import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime
# import opencv



# Initialize Firebase Admin SDK
cred = credentials.Certificate("modules\secrets.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'learning-storage-anurag.appspot.com'
})

bucket = storage.bucket()

# Function to upload a file to Firebase Storage
def upload_file(file, destination_blob_name):
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file , content_type='image/jpg')
    return destination_blob_name

def download_file(destination_file_path, source_blob_name):
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_path)
    print(f"File downloaded from {source_blob_name} to {destination_file_path}.")


def upload(img):

    # _ , image_bytes = cv2.imencode('.jpg', image_array)
    # image_byte_stream = BytesIO(image_bytes)

    return upload_file(img , "images/output" + str(datetime.now())  + ".jpg")

