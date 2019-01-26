import os
import flickrapi
import urllib
import fnmatch


KEY = "dd31b95032ac547830155e09cb33eea1"
SECRET = "0b32af0505818a2b"

flickr=flickrapi.FlickrAPI(KEY,SECRET,cache=True)
f = open("log.txt", 'r')
urls = [x[:-1] for x in f]
f.close()

def flickr_walk(keyword):
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder+"/"+keyword):
        os.makedirs(folder+"/"+keyword)
    path = folder+"/"+keyword+"/"

    count = len(fnmatch.filter(os.listdir(path), "*.jpeg"))

    i = 1
    photos = flickr.walk(text=keyword, tags=keyword, extras='url_c', per_page=100, sort='relevance')
    f = open("log.txt", "a")
    for photo in photos:
        if i <= number:
            name =  keyword +" "+str(count)
            filePath = path + name+".jpeg"

            try:
                url=photo.get('url_c')

                if url not in urls:
                    f.write(url+"\n")
                    urllib.request.urlretrieve(url, filePath)
                    print("Saving " + keyword + " "+ str(i))
                    i += 1
                    count += 1
                else:
                    continue

            except Exception as e:
                print("ERROR: " + str(e))
        else:
            break
    f.close()

keyWords = input().split(' ')
number = int(input())
folder = input()


for keyWord in keyWords:
    flickr_walk(keyWord)
    print("Downloaded: "+str(number) + " " +keyWord +" Photos Scuccesfully")
