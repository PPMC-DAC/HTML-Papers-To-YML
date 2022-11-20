import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
URL = "file://AsenjoPapers.html"
page = requests.get(URL)

print(page.text)