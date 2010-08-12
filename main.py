#!/usr/bin/env python
#coding:utf-8

#Need PIL.
import Image
import os
import optparse

R,G,B = 0,1,2
CURRENT_DIR = os.path.dirname(__file__)
POINT_PICTURE = os.path.join(CURRENT_DIR,u"point.png")

#color_list is (r,g,b) or (r,g,b,a)
def comp(color_list):
    r = color_list[0]
    g = color_list[1]
    b = color_list[2]

    MAX = max(r,g,b)
    MIN = min(r,g,b)
    rR = MAX - r + MIN
    rG = MAX - g + MIN
    rB = MAX - b + MIN
    return (rR,rG,rB)


def translate(picture,point=True,anime=False,quiet=False):
    if not os.path.exists(picture):
        print u"Error:NotFound %s"%picture
        return 0
    inImage = Image.open(picture)

    outImageName = os.path.join(os.path.dirname(picture),u"out" + os.path.basename(picture))
    monoImageName = os.path.join(os.path.dirname(picture),u"mono" + os.path.basename(picture))
    if not quiet:
        print u"Input Image  = %s"%picture
        print u"Output Image = %s"%outImageName
        print u"Mono Image   = %s"%monoImageName
        print u"Point:\t%s"%point
        print u"Anime:\t%s\n"%anime
        print u"Start Translating..."

    size = inImage.size
    width = size[0]
    height = size[1]
    outImage = inImage.copy()
    mono = inImage.convert("L")
    pix = inImage.load()

    for w in range(width):
        for h in range(height):
            outImage.putpixel((w,h),comp(pix[w,h]))

    if point:
        pointImage = Image.open(POINT_PICTURE).convert("RGBA")
        pwidth = pointImage.size[0]
        pheight = pointImage.size[1]
        pw = width/2 - pwidth/2
        ph = height/2 - pheight/2
        outImage.paste(pointImage,(pw,ph),pointImage)

    outImage.save(outImageName)
    mono.save(monoImageName)
    if not quiet:
        print u"OutputImage and MonoImage done."

    if anime:
        animeImageName = os.path.join(os.path.dirname(picture),u"anime" + os.path.splitext(os.path.basename(picture))[0] + u".gif")
        if not quiet:
            print u"Start making Anime..."
            print u"Anime Image = %s"%animeImageName
        makeAnimeCommand = u"convert -delay 2000 -loop 0 %s %s %s"%(outImageName,monoImageName,animeImageName)
        os.system(makeAnimeCommand)
        if not quiet:
            print u"Anime making done."
    if not quiet:
        print u"\nDone\n"


def main():
    usage = u"python %prog [options] arg1 arg2"
    parser = optparse.OptionParser(usage)
    parser.enable_interspersed_args()
    parser.add_option("-q","--quiet",action="store_true",dest="quiet",
                      help="don't print status message to stdout")
    parser.add_option("-a","--anime",action="store_true",dest="anime",
                      help="use Imagemagick and make gif animation")
    parser.add_option("-p","--point",action="store_true",dest="point",
                      help="point centor of outputImage")

    parser.set_defaults(quiet=False)
    parser.set_defaults(anime=False)
    parser.set_defaults(point=False)

    (options,args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        exit()

    quiet = options.quiet
    anime = options.anime
    point = options.point
    for pic in args:
        translate(pic,point,anime,quiet)

if __name__ == "__main__":
    main()
