from PIL import Image
from StringIO import StringIO
import shopify
import requests
import base64
from datetime import datetime

#From: https://gist.github.com/fabeat/6621507
def scale(image, max_size, method=Image.ANTIALIAS):
    """
    resize 'image' to 'max_size' keeping the aspect ratio
    and place it in center of white 'max_size' image
    """
    im_aspect = float(image.size[0])/float(image.size[1])
    out_aspect = float(max_size[0])/float(max_size[1])
    if im_aspect >= out_aspect:
        scaled = image.resize((max_size[0], int((float(max_size[0])/im_aspect) + 0.5)), method)
    else:
        scaled = image.resize((int((float(max_size[1])*im_aspect) + 0.5), max_size[1]), method)

    offset = (((max_size[0] - scaled.size[0]) / 2), ((max_size[1] - scaled.size[1]) / 2))
    back = Image.new("RGB", max_size, "white")
    back.paste(scaled, offset)
    return back

def image_size_url(image_url, size="medium"):
    image_url_pre = image_url[:image_url.rfind(".")]
    image_url_end = image_url[image_url.rfind("."):]
    return "%s_%s%s" % (image_url_pre, size, image_url_end)

SHOP_NAME = raw_input("Enter in your Shopify URL (don't include the http://): ")
API_KEY = raw_input("Enter in your Shopify Private App API Key: ")
API_PASSWORD = raw_input("Enter in your Shopify Private App Password: ")

session = shopify.Session(SHOP_NAME)
session.protocol = "https"
session.api_key = API_KEY
session.token = API_PASSWORD
shopify.ShopifyResource.activate_session(session)
products = shopify.Product.find()

for p in products:
    if len(p.images) > 0:
        image = p.image
        r = requests.get(image_size_url(image.attributes['src'], "small"))
        i = Image.open(StringIO(r.content))

        print "Processing '%s'" % (p.title)

        max_size = i.size[1]
        if i.size[0] == i.size[1]:
            continue
        elif i.size[0] > i.size[1]:
            max_size = i.size[0]

        output = StringIO()
        back.save(output, format="PNG")
        contents = output.getvalue()
        output.close()
        p.image.attach_image(contents, "%s.png" % image.id)
        p.image.save()
        p.save()
