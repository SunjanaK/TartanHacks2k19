

from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials

# pip install Pillow
from PIL import Image
import requests
from io import BytesIO


subscription_key = "768fb70aaef144a4bbdcd344c8b80c8a"
search_term = "hamburger"

client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
image_results = client.images.search(query=search_term)

if image_results.value:
    first_image_result = image_results.value[0]
    print("Total number of images returned: {}".format(len(image_results.value)))
    print("First image thumbnail url: {}".format(first_image_result.thumbnail_url))
    print("First image content url: {}".format(first_image_result.content_url))

    # Display using Pillow
    response = requests.get(first_image_result.thumbnail_url)
    img = Image.open(BytesIO(response.content))
    img.show()

else:
    print("No image results returned!")


