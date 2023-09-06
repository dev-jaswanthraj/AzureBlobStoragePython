from flask import Flask, render_template, request, redirect
from azure.storage.blob import BlobServiceClient
import os

# Creating a app
app = Flask(__name__)

# retrieve  the connection string from the environment variable
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
# container name in which images be store in the storage account
container_name = "images"

# Create Blob Service Clinet to interact with the storage account
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)

try:
    # get container client to interact with thecontainter in which images will be stored
    container_client = blob_service_client.get_container_client(container=container_name)
    # get container properties to the container fource exception to be raised if container does not exist
    container_client.get_container_properties()
except:
    # create a container in the storage account if it does not exits
    container_client = blob_service_client.create_container(container_name)

@app.route("/")
def view_photo():
    """
    This function is used to upload HTML form to upload the Picture.
    """
    # list all the blobs in the container
    blob_items = container_client.list_blobs()
    urls = []
    for blob in blob_items:
        # get blob clinet to interact with the blob and ge the blob url
        blob_client = container_client.get_blob_client(blob=blob.name)
        # get the blog url
        urls.append(blob_client.url)
    return render_template("upload_photo.html", urls=urls)
    
# endpoint to upload photos
@app.route("/upload-photos", methods = ["POST"])
def upload_photo():
    filenames = ""
    for file in request.files.getlist("photos"):
        try:
            # upload the file to the container using the filename as a blob name
            container_client.upload_blob(file.filename, file)
            filenames += file.filename + " "
        except Exception as e:
            print(e)
            print("Ingroging th dulicate filenames")

    
    return redirect('/')  