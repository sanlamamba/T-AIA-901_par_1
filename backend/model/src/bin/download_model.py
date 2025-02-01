import os
import sys

sys.path.append(os.path.join(os.getcwd(), ".."))

from services.azure_bucket import AzureBucket

bucket = AzureBucket()
# bucket.list_blobs()
path_to_model = os.path.join(os.getcwd(), "../../processed/city_nlp/")
bucket.download_locally("NER_model.pth", path_to_model)
bucket.download_locally("model.pth", path_to_model)