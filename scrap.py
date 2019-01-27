import os
import flickrapi
import urllib
import fnmatch




def flickr_walk(keyword):
    i = 1
    f = open("log.txt", "a")
    photos = flickr.walk(text=keyword, tags=keyword, extras='url_c', per_page=100, sort='relevance')

    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder+"/"+keyword):
        os.makedirs(folder+"/"+keyword)
    path = folder+"/"+keyword+"/"

    count = len(fnmatch.filter(os.listdir(path), "*.jpeg"))
    for photo in photos:
        if i <= number:
            name =  keyword +" "+str(count)
            filePath = path + name+".jpeg"

            try:
                url=photo.get('url_c')

                if url not in urls and url != None:
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


print()
print("Enter Your API key: ", end='')
KEY = input().strip()


print("Enter Your API Secret: ", end='')
SECRET = input().strip()
flickr=flickrapi.FlickrAPI(KEY,SECRET,cache=True)



print()
print("Enter the directory to save the photos in: ", end='')
folder = input()

print("Enter photos tags to download: ", end='')
keyWords = input().strip().split(' ')


print("Enter how many photos do you want to download: ", end='')
number = int(input())
print()


f = open("log.txt", 'r')
urls = [x[:-1] for x in f]
f.close()


for keyWord in keyWords:
    flickr_walk(keyWord)
    print("Downloaded: "+str(number) + " " +keyWord +" Photos Scuccesfully")
