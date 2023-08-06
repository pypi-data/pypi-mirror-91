import requests

class APIClient:
    def __init__(self, apikey):
        self.apikey = apikey

    def getFoxImage(self, filename):
        if not filename.endswith(".jpg"):
            raise Exception("The API gives JPG images. Please, change the filename from {} to {}.jpg".format(filename, filename.split(".")[0]))
        else:
            r = requests.post("https://vdevapi.vertexxdev.repl.co/get/fox", data={"apikey": self.apikey})
            text = r.text
            if "Invalid API key!" in text:
                raise Exception("Invalid API key!")
            elif "Please, use POST not GET" in text:
                raise Exception("Please, use POST not GET. [LIB ERROR, CONTACT DEVELOPER]")

            f = open(filename, "wb")
            f.write(r.content)
            f.close()