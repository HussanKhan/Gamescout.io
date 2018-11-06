#!/usr/bin/python3.5
def cut_images(folder):
    from PIL import Image
    import os

    for f in os.listdir('/var/www/VgApp/vgdeals_production/static/images/' + folder + '/.'):
        try:
            i = Image.open("/var/www/VgApp/vgdeals_production/static/images/" + folder + "/" + f)
            fn, fext = os.path.splitext(f)
            i.save('/var/www/VgApp/vgdeals_production/static/images/' + folder + '/{}{}'.format(fn,fext), quality=70)
        except Exception:
            print("Could not convert image")
def delete_images(folder):
    from PIL import Image
    import os

    for f in os.listdir('/var/www/VgApp/vgdeals_production/static/images/' + folder + '/.'):
        try:
            if f != "/var/www/VgApp/vgdeals_production/static/images/" + folder + "/__pycache__":
                os.remove("/var/www/VgApp/vgdeals_production/static/images/" + folder + "/" + f)
        except Exception:
            print("Cannot delete image")

def download_images(title, image_url, folder):
    from PIL import Image
    import os
    import urllib.request
    from urllib.request import Request, urlopen
    from shutil import copyfileobj

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    try:
        req = Request(image_url, headers=header)
        with urlopen(req) as in_stream, open("/var/www/VgApp/vgdeals_production/static/images/" + folder + '/' + title + ".jpg", 'wb') as out_file:
            copyfileobj(in_stream, out_file)

        file_title = title.replace(" ", "%20")

        return "static/images/" + folder + '/' + file_title + ".jpg"

    except Exception:
        print('Error Downloading Image')
