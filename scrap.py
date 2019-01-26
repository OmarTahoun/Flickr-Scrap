import flickrapi
import urllib


KEY = "dd31b95032ac547830155e09cb33eea1"
SECRET = "0b32af0505818a2b"

path = "test/"

flickr=flickrapi.FlickrAPI(KEY,SECRET,cache=True)

def flickr_walk(keyward):
    photos = flickr.walk(text=keyward, tags=keyward, extras='url_c', per_page=100, sort='relevance')

    i = 1
    for photo in photos:
        name =  keyward +str(i)
        filePath = path + name
        try:
            url=photo.get('url_c')
            urllib.request.urlretrieve(url, filePath)
            print("Saving "+ name)
            i += 1
        except Exception as e:
            print("ERROR: " + str(e))

flickr_walk("dogs ")
