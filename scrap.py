import os
import flickrapi
import urllib
import fnmatch
import json
import argparse




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


def set_key_secret():
    key = input("KEY: ")
    secret = input("SECRET: ")
    with open(".secret", "w") as file:
        cred = {'Key': key, 'Secret': secret}
        json.dump(cred, file)

def get_key_secret():
    with open(".secret", "r") as file:
        data = file.read()
        creds = json.loads(data)
        key = creds['Key']
        secret = creds['Secret']
        return [key, secret]

def check_key_secret():
    creds = get_key_secret()
    key = creds[0]
    secret = creds[1]

    if key and secret:
        return [key, secret]
    else:
        False

def check_path(location, keyword):
    if not os.path.exists(location):
        os.makedirs(location)
    if not os.path.exists(location+"/"+keyword):
        os.makedirs(location+"/"+keyword)
    path = location+"/"+keyword+"/"
    return path

def get_images(flickr, keyword, path, count):
    # with open('log.json', 'r') as file:
    #     data = file.read()
    #     downloaded_images = json.loads(data)


    URLS = flickr.walk(text=keyword, tags=keyword, extras='url_c', per_page=100, sort='relevance')
    photo_id = len(fnmatch.filter(os.listdir(path), "*.jpeg"))
    for url in URLS:
        if count > 0:
            name =  keyword +" "+str(photo_id)
            filePath = path + name+".jpeg"

            try:
                image = url.get('url_c')

                if image != None:
                    urllib.request.urlretrieve(image, filePath)
                    print("Saving " + keyword + " "+ str(photo_id))
                    count -=1
                    photo_id +=1
                else:
                    continue

            except Exception as e:
                print("ERROR: " + str(e))
        else:
            break


def main():
    parser = argparse.ArgumentParser(description="Flickr")
    sub_commands = parser.add_subparsers(help='Choose what command to run',dest='choice')

    parser_auth = sub_commands.add_parser('auth', help='Add or Update the Authentication Credentials')
    parser_auth.add_argument('-key', dest='key', help='API KEY', required = True)
    parser_auth.add_argument('-secret', dest='secret', help='API Secret', required = True)

    parser_scrap = sub_commands.add_parser('fetch', help='Download pictures with a keyword')
    parser_scrap.add_argument('-keyword', dest='keyword', help='the keyword to look for', required=True)
    parser_scrap.add_argument('-path', dest='path', help='the location to save the pictures', required=True)
    parser_scrap.add_argument('-count', dest='count', help='the number of pictures to download', type = int ,required=True)

    arguments = parser.parse_args()
    choice = arguments.choice

    if choice == 'auth':
        key = arguments.key
        secret = arguments.secret
        set_key_secret(key, secret)
    else:
        keyword = arguments.keyword
        location = arguments.path
        count = arguments.count

        key, secret = check_key_secret()
        if key and secret:
            flickr = flickrapi.FlickrAPI(key,secret,cache=True)
            path = check_path(location, keyword)
            get_images(flickr, keyword, path, count)

        else:
            print("Wrong / NO API Authentication details were Found, To Update / Set Your API Authentication details")
            print("run 'scrap.py auth -key <API key> -secret <API secret>'")

if __name__ == '__main__':
    main()
