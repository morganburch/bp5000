# grf.py - Graphical code
#
#
from PIL import Image, ImageDraw, ImageFont
import math

# Colour of the lines
lcolor = (255, 195, 155)
FONTPATH = ["DejaVuSans.ttf", "verdana.ttf", "Helvetica.dfont",
            "Helvetica.ttf"]


def getFont(sz, num=0):
    try:
        fnt = ImageFont.truetype(FONTPATH[num], sz)
        return fnt
    except OSError:
        try:
            return getFont(sz, num+1)
        except:
            s = "FATAL: no fonts found. install"
            s2 = " DejaVuSans, verdana or Helvetica"
            print(s+s2)


ckb = None


def getchek():
    global ckb
    if ckb is None:
        data = (b'iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAA'
                b'A71pVKAAABVUlEQVR4nGNgGJKAkRTF7ErsVlxGXCGMHIx8Xw5'
                b'9mU6cZkYGJoFAgS4+F75iBgYGht/Pf1992f3SioWgRiYGZpEE'
                b'kSVcJlwRDAwMDH8//X3xeupr738//n1iIqRXKFJoBkzj/9//v7'
                b'+e/trvz7s/DyHm4gG8TryFPNY8KQwMDAwM/xn+v13wNvbXw1+nE'
                b'Y6CMbiZhAX8BFqEYoTmMjAwMLArsVsKBgl2weQ/bP5Q++38t7XIh'
                b'sP9LBgs2MttwR3PwMDA8P3i9/WCYYKTGJgg8t/Oflv1acenVnSXw'
                b'TX/+/bvPYwtmim6Gcb+/ez35beL3yZi8xbc2T9u/ziILvnvx7/Pr2'
                b'e9Dv7/6/83/Jqv/dj578e/T8iS71e9z/3z6s9tbBpRNP///f/7l4Nf'
                b'psH43y993/j1xNeFuDQyMKAnT0YGJjY5NiOGfwz/fj35dYHhP8M/fJo'
                b'BGuqDl4b7We4AAAAASUVORK5CYII=')
        import base64
        from io import BytesIO
        ckb = Image.open(BytesIO(base64.b64decode(data)))
    return ckb


def drawmatch(match, highlight=False):
    str1 = match.part1.tag if match.part1 else "TBD"
    int1 = match.part1.seed if match.part1 else ""
    str2 = match.part2.tag if match.part2 else "TBD"
    int2 = match.part2.seed if match.part2 else ""
    img = Image.new('RGBA', (200, 80),
                    color=((155, 155, 255) if not highlight else (255,
                                                                  155, 155)))
    d = ImageDraw.Draw(img)
    font = getFont(20)
    d.font = font
    d.rectangle((0, 0, 45, 80), fill=(0, 0, 200))
    d.text((5, 2), str(int1))
    d.text((60, 2), str1)
    if match.winner != 0:
        img.paste(getchek(), (180, 56 if match.winner == 2 else 5), getchek())
    d.text((5, 53), str(int2))
    d.text((60, 53), str2)
    d.rectangle((0, 28, 200, 48), fill=(200, 0, 0))
    wt = (" W:"+match.wlink.getmatchdisp() if match.wlink else "")
    lt = (" L:"+match.llink.getmatchdisp() if match.llink else "")
    font = getFont(18)
    d.font = font
    d.text((0, 28), match.getmatchdisp()+wt+lt)
    return img


def drawspmatch(match, highlight=False):
    str1 = match.part1.tag if match.part1 else "TBD"
    int1 = match.part1.seed if match.part1 else ""
    str2 = match.part2.tag if match.part2 else "TBD"
    int2 = match.part2.seed if match.part2 else ""
    img = Image.new('RGBA', (200, 80),
                    color=((155, 155, 255) if not highlight else (255,
                                                                  155, 155)))
    d = ImageDraw.Draw(img)
    font = getFont(20)
    d.font = font
    d.rectangle((0, 0, 45, 80), fill=(0, 0, 200))
    d.text((5, 2), str(int1))
    d.text((60, 2), str1)
    d.text((180, 2), str(match.upperleft), fill=(0, 170, 0))
    d.text((5, 53), str(int2))
    d.text((60, 53), str2)
    d.text((180, 53), str(match.lowerleft), fill=(0, 170, 0))
    d.rectangle((0, 28, 200, 48), fill=(200, 0, 0))
    wt = (" W:"+match.wlink.getmatchdisp() if match.wlink else "")
    lt = (" L:"+match.llink.getmatchdisp() if match.llink else "")
    font = getFont(18)
    d.font = font
    d.text((0, 28), match.getmatchdisp()+wt+lt)
    return img


def mouse_ev(xm, ym, bracket, retm=False):
    if isinstance(bracket[0], list):
        return mouse_ev_finals(xm, ym, bracket, retm)
    br = bracket
    x = 30
    ymult = 1
    while(br[0] is not None):
        nb = []
        y = 30 + (ymult-1)*60
        for ma in br:
            rect = (x, y, 200, 80)
            if intersect((xm, ym), rect) and (not ma.isspecial()):
                return ma if retm else (drawmatch(ma, True), x, y)
            y += 120*ymult
            if not (ma.wlink in nb):
                nb.append(ma.wlink)
        x += 220
        ymult = ymult*int(len(br)/len(nb))
        br = nb
    return None


def mouse_ev_finals(xm, ym, brackets, retm):
    gfs = [firstgf(brackets[r][0]) for r in range(len(brackets)-2, -1, -1)]
    xpos = 20
    for gf in gfs:
        rect = (xpos, 20, 200, 80)
        if intersect((xm, ym), rect):
            return gf if retm else (drawspmatch(gf, True), xpos, 20)
        xpos += 220
    return None


def intersect(pt, rect):
    cond1 = (rect[0] <= pt[0] <= rect[0]+rect[2])
    cond2 = (rect[1] <= pt[1] <= rect[1]+rect[3])
    return cond1 and cond2


def drawbracket(bracket):
    br = bracket
    tm = br[0]
    rounds = 0
    while(tm.wlink is not None and not tm.wlink.isspecial()):
        tm = tm.wlink
        rounds += 1
    img = Image.new('RGBA', (250+int(220*rounds),
                             len(br)*120), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 30
    ymult = 1
    rdc = len(br)
    dbar = False
    while(br[0] is not None):
        dbar = (rdc != len(br))
        nb = []
        y = 30 + (ymult-1)*60
        fakey = (30+(((ymult/2)-1)*60))
        for ma in br:
            im = drawmatch(ma)
            if(dbar):
                # y mult /2
                ny = fakey + (120*ymult/2)
                d.rectangle((x+100, fakey+36, x+104, ny+40), fill=lcolor)
                fakey = ny + (120*ymult/2)

            img.paste(im, (x, y))
            if ma.wlink is not None and not ma.wlink.isspecial():
                d.rectangle((x+200, y+36, x+320, y+40), fill=lcolor)
            y += 120*ymult
            if not (ma.wlink in nb):
                nb.append(ma.wlink)
        x += 220
        ymult = ymult*int(len(br)/len(nb))
        rdc = len(br)
        br = nb
    return img


def firstgf(match):
    m = match
    while not m.isspecial():
        m = m.wlink
    return m


def drawfinals(brackets):
    gfs = [firstgf(brackets[r][0]) for r in range(len(brackets)-2, -1, -1)]
    img = Image.new('RGBA', (30+(len(gfs)*250), 120), color=(0, 0, 0))
    xpos = 20
    for gf in gfs:
        im = drawspmatch(gf)
        img.paste(im, (xpos, 20))
        xpos += 220
    return img

if __name__ == '__main__':
    import data
    i = 32
    plist = (['player %s ' % x for x in range(0, i)])
    b = data.genm(plist)
    l = data.genl(b)
    l2 = data.genl(l)
    data.fbracket([b, l, l2])
    import bracketfuncs
    bracketfuncs.projected([b, l, l2])
    img = drawbracket(b)
    im2g = drawbracket(l)
    im3g = drawbracket(l2)
    imfg = drawfinals([b, l, l2])
    img.show()


"""
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGBA', (15, 15))
draw = ImageDraw.Draw(img)
draw.font = ImageFont.truetype("DejaVuSans.ttf", 20)
draw.text((0, -3), u'\u2714', fill=(30, 150, 30))
## convert to base64

b'iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAABVUlEQVR4nGNgGJKAkRTF7ErsVlxGXCGMHIx8Xw59mU6cZkYGJoFAgS4+F75iBgYGht/Pf1992f3SioWgRiYGZpEEkSVcJlwRDAwMDH8//X3xeupr738//n1iIqRXKFJoBkzj/9//v7+e/trvz7s/DyHm4gG8TryFPNY8KQwMDAwM/xn+v13wNvbXw1+nEY6CMbiZhAX8BFqEYoTmMjAwMLArsVsKBgl2weQ/bP5Q++38t7XIhsP9LBgs2MttwR3PwMDA8P3i9/WCYYKTGJgg8t/Oflv1acenVnSXwTX/+/bvPYwtmim6Gcb+/ez35beL3yZi8xbc2T9u/ziILvnvx7/Pr2e9Dv7/6/83/Jqv/dj578e/T8iS71e9z/3z6s9tbBpRNP///f/7l4NfpsH43y993/j1xNeFuDQyMKAnT0YGJjY5NiOGfwz/fj35dYHhP8M/fJoBGuqDl4b7We4AAAAASUVORK5CYII='
"""
