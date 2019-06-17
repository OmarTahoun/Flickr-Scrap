import os
import flickrapi
import urllib
import fnmatch
import json
import argparse



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
    images = flickr.walk(text=keyword, tags=keyword, extras='url_c', per_page=100, sort='relevance')
    urls = []

    for image in images:
        if len(urls) >= count: break
        try:
            url = image.get('url_c')
            if url != None:
                urls.append(url)
        except Exception as e:
            print("ERROR: "+ str(e))

    photo_id = len(fnmatch.filter(os.listdir(path), "*.jpg"))

    for url in urls:
        photo_id += 1
        name =  keyword +" "+str(photo_id)
        file_path = path + name + ".jpg"
        try:
            urllib.request.urlretrieve(url, file_path)
            print("Saving " + keyword + " "+ str(photo_id))
        except Exception as e:
            print("ERROR: " + str(e))


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
