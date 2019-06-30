# pip install azure-cognitiveservices-search-imagesearch
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials

# pip install Pillow
from PIL import Image, ImageTk
import requests
from io import BytesIO

import tkinter as tk

def openImage(search_term, time_span=2000):
    subscription_key = "768fb70aaef144a4bbdcd344c8b80c8a"

    # Search using Azure Bing Image Search
    client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
    image_results = client.images.search(query=search_term)

    if image_results.value: # Check if result found
        first_image_result = image_results.value[0]

        # Display using Pillow
        response = requests.get(first_image_result.thumbnail_url)
        img = Image.open(BytesIO(response.content))

        # Open Image using tkinter
        root = tk.Tk()
        tkimage = ImageTk.PhotoImage(img)
        tk.Label(root, image=tkimage).pack()
        root.after(time_span, lambda: root.destroy())  # Destroy the widget after time_span ms
        root.mainloop()
    else:
        print("No image results returned!")

# Sample Usage
# openImage("Swimming", 1800)
