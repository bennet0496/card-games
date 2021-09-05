import math
import os
import csv
import sys

from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageStat
from PIL.ExifTags import TAGS
from fpdf import FPDF
from colour import Color

import seaborn
import pathlib


CWD = pathlib.Path(__file__).parent.resolve()

POS_X = 6
TEXT_POS_Y = 6
SUIT_POS_Y = 15

FORMAT = (65, 97)


def format_num_str(num: str):
    s = num
    f = float(num.replace(',', ''))
    if f > pow(10, 9):
        s = '{:,}B'.format(round(f / pow(10, 9), 2))
    elif f > pow(10, 6):
        s = '{:,}M'.format(round(f / pow(10, 6), 2))
    elif f > pow(10, 3):
        s = '{:,}K'.format(round(f / pow(10, 3), 0))

    return s


def parse_all_exif(exifdata):
    # iterating over all EXIF data fields
    edata = dict()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()

        edata[tag] = data
        #print(f"{tag:25}: {data}")
    return edata


def cut_lines(pdf: FPDF):
    c = pdf.draw_color
    pdf.set_draw_color(r=255, g=0, b=0)
    pdf.dashed_line(x1=3.05, y1=3.05, x2=61.95, y2=3.05, dash_length=1, space_length=1)
    pdf.dashed_line(x1=3.05, y1=3.05, x2=3.05, y2=93.95, dash_length=1, space_length=1)
    pdf.dashed_line(x1=61.95, y1=3.05, x2=61.95, y2=93.95, dash_length=1, space_length=1)
    pdf.dashed_line(x1=3.05, y1=93.95, x2=61.95, y2=93.95, dash_length=1, space_length=1)
    pdf.draw_color = c


def safe_lines(pdf: FPDF):
    c = pdf.draw_color
    pdf.set_draw_color(r=0, g=255, b=0)
    pdf.dashed_line(x1=3.05*2, y1=3.05*2, x2=61.95-3.05, y2=3.05*2, dash_length=1, space_length=1)
    pdf.dashed_line(x1=3.05*2, y1=3.05*2, x2=3.05*2, y2=93.95-3.05, dash_length=1, space_length=1)
    pdf.dashed_line(x1=61.95-3.05, y1=3.05*2, x2=61.95-3.05, y2=93.95-3.05, dash_length=1, space_length=1)
    pdf.dashed_line(x1=3.05*2, y1=93.95-3.05, x2=61.95-3.05, y2=93.95-3.05, dash_length=1, space_length=1)
    pdf.draw_color = c


if __name__ == "__main__":
    imgs = []
    i = 0
    pdf = FPDF(orientation="P", format=FORMAT, unit="mm")
    pdf.add_font("ArialUnicode", style="", fname="{0}/../fonts/arial-unicode-ms.ttf".format(CWD), uni=True)
    pdf.add_font("CaviarDreams", style="", fname="{0}/../fonts/CaviarDreams.ttf".format(CWD), uni=True)
    pdf.add_font("CaviarDreamsBold", style="", fname="{0}/../fonts/CaviarDreams_Bold.ttf".format(CWD), uni=True)
    pdf.set_image_filter("JPXDecode")

    pdf.add_page()

    # title page

    pdf.set_fill_color(100, 65, 165)
    pdf.set_margin(0)

    pdf.image("{0}/assets/Streamer-1.jpg".format(CWD), x=0, y=7, w=FORMAT[0])

    with pdf.rotation(angle=3, x=FORMAT[0] / 2, y=TEXT_POS_Y):
        pdf.rect(x=-5, y=-15, w=FORMAT[0] + 10, h=30, style='F')
        pdf.set_y(4)
        pdf.set_font("CaviarDreamsBold", '', 12)
        pdf.cell(w=FORMAT[0], h=10, txt="Twitch Streamer", align="C", fill=False, border=0)
        pdf.set_y(11.8)
        pdf.set_font("CaviarDreams", '', 5)
        pdf.cell(w=FORMAT[0], h=10, txt="by Bennet B., create your own at github.com/bennet0496/card-games", align="C", fill=False, border=0)

    pdf.image("{0}/symbols/TwitchGlitchPurple.eps".format(CWD), x=FORMAT[0]/2 - 7, y=25, w=14)
    pdf.set_y(45)
    pdf.set_font("ArialUnicode", '', 8)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(w=FORMAT[0], h=5, txt="● LIVE", align="C", fill=False, border=0)

    pdf.set_text_color(0)
    pdf.set_font("CaviarDreamsBold", '', 10)
    pdf.set_y(52)
    # pdf.cell(w=14)
    pdf.cell(w=FORMAT[0], h=5, txt="Play · Collect · Ruff", align="C", fill=False, border=0)
    pdf.set_y(56)
    pdf.set_font("CaviarDreamsBold", '', 6)
    pdf.cell(w=FORMAT[0], h=5, txt="Designed in Germany", align="C", fill=False, border=0)

    pdf.image("{0}/assets/barcode.gif".format(CWD), x=FORMAT[0] / 2 - 15, y=88, w=30)

    pdf.add_page()

    # rules and info

    pdf.set_fill_color(100, 65, 165)
    pdf.set_margin(0)

    with pdf.rotation(angle=3, x=FORMAT[0] / 2, y=TEXT_POS_Y):
        pdf.rect(x=-5, y=-15, w=FORMAT[0] + 10, h=27, style='F')
        pdf.set_y(4)
        pdf.set_font("CaviarDreamsBold", '', 8)
        pdf.cell(w=FORMAT[0], h=10, txt="Twitch Streamer - Game Info", align="C", fill=False, border=0)

    pdf.set_font("CaviarDreamsBold", '', 5)
    pdf.set_y(10)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="4 year and up, Game for 2 players or more", align="L", fill=False, border=0)

    pdf.set_font("CaviarDreams", '', 5)
    pdf.set_y(12)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="Please, for the love of god, do not try to eat the playing cards", align="L", fill=False, border=0)
    pdf.set_y(14)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="or the cardboard box, you might choke and f**king die. But if", align="L", fill=False, border=0)
    pdf.set_y(16)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="you feel inclined to do it anyway, please don't say I didn't warn", align="L", fill=False, border=0)
    pdf.set_y(18)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="you, and sue me.", align="L", fill=False, border=0)
    pdf.set_y(20)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="With this disclaimer out of the way, this cards may be used to", align="L", fill=False, border=0)
    pdf.set_y(22)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="play games, including but not limited to", align="L", fill=False, border=0)
    pdf.set_font("CaviarDreamsBold", '', 5)
    pdf.set_y(25)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="Quartets:", align="L", fill=False, border=0)
    pdf.set_font("CaviarDreams", '', 5)
    pdf.set_y(27)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="After thoroughly mixing the deck, cards are distributed evenly to", align="L", fill=False, border=0)
    pdf.set_y(29)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="the players. Now each player looks at its cards - in case they", align="L", fill=False, border=0)
    pdf.set_y(31)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="already have one or more Quartets (i.e. have all cards 1-4 of", align="L", fill=False, border=0)
    pdf.set_y(33)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="the same category), they can immediately put them on display", align="L", fill=False, border=0)
    pdf.set_y(35)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="in front of themselves. The game is played clock-wise. The player,", align="L", fill=False, border=0)
    pdf.set_y(37)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="left of the dealer, begins. They now ask any of the other players,", align="L", fill=False, border=0)
    pdf.set_y(39)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="for a specific card, they are missing. Should the player have", align="L", fill=False, border=0)
    pdf.set_y(41)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="the card, asked for, they must give the card to the asking player", align="L", fill=False, border=0)
    pdf.set_y(43)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="and the asking player can continue to ask for cards. Should the", align="L", fill=False, border=0)
    pdf.set_y(45)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="player not have the desired card, the asking player's turn is over,", align="L", fill=False, border=0)
    pdf.set_y(47)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="and the asked player may continue to ask the others for cards", align="L", fill=False, border=0)
    pdf.set_y(49)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="they are missing. In the end, the player with most complete", align="L", fill=False, border=0)
    pdf.set_y(51)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="Quartets wins.", align="L", fill=False, border=0)
    pdf.set_font("CaviarDreamsBold", '', 5)
    pdf.set_y(54)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="Ruff (trump) a.k.a. bigger number, better person:", align="L", fill=False, border=0)
    pdf.set_font("CaviarDreams", '', 5)
    pdf.set_y(56)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="After thoroughly mixing the deck, cards are distributed evenly to", align="L", fill=False, border=0)
    pdf.set_y(58)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="the players. The players hold the cards one after another as a", align="L", fill=False, border=0)
    pdf.set_y(60)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="stack, so they, themselves, only see the top card of the stack", align="L", fill=False, border=0)
    pdf.set_y(62)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="at any given time. One player starts to read the title of the", align="L", fill=False, border=0)
    pdf.set_y(64)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="card, as well as the category and one value of their choice.", align="L", fill=False, border=0)
    pdf.set_y(66)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="The other players compare this value, with the same value on", align="L", fill=False, border=0)
    pdf.set_y(68)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="their own top card - the biggest value, wins. The winner gets the", align="L", fill=False, border=0)
    pdf.set_y(70)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="played cards of the other players and starts the next round.", align="L", fill=False, border=0)
    pdf.set_y(72)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="For equal values, the category coming alphabetically after the", align="L", fill=False, border=0)
    pdf.set_y(74)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="other wins. If the category is equal as well, the higher number", align="L", fill=False, border=0)
    pdf.set_y(76)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="in the corner wins. The Winner of the game is the player with", align="L", fill=False, border=0)
    pdf.set_y(78)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="the most cards in the end.", align="L", fill=False, border=0)

    pdf.set_font("CaviarDreams", '', 4)
    pdf.set_y(81)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="by Bennet Becker, designed in Germany", align="L", fill=False, border=0)
    pdf.set_y(83)
    pdf.set_x(5.5)
    pdf.cell(w=FORMAT[0] - 12, h=10, txt="Layout under CC-BY-SA 4.0, Images © by their respective owners", align="L", fill=False, border=0)
    pdf.set_y(85)
    pdf.set_x(5.5)
    pdf.cell(h=10, txt="github.com/bennet0496/card-games", align="L",fill=False, border=0, link="https://github.com/bennet0496/card-games")
    # pdf.set_x(5.5)
    pdf.cell(h=10, txt="twitter.com/bennet0496", align="L", fill=False, border=0, link="https://twitter.com/bennet0496")

    im = Image.open("{0}/assets/HYPERS.png".format(CWD))
    im2 = Image.new('RGBA', im.size, color=(255, 255, 255, 255))
    im3 = Image.composite(im, im2, im)
    pdf.image(im3, x=51.5, y=83.8, w=7)

    # safe_lines(pdf)
    # cut_lines(pdf)

    # pdf.output("test.pdf")
    # sys.exit(0)

    pdf.add_page()

    #back side

    pdf.set_fill_color(100, 65, 165)
    pdf.rect(x=0, y=0, w=FORMAT[0], h=FORMAT[1], style='F')

    im = Image.open("{0}/assets/TwitchGlitchWhite.png".format(CWD))
    im2 = Image.new('RGBA', im.size, color=(100, 65, 165, 1))
    im3 = Image.composite(im, im2, im)

    pdf.set_y(0)
    pdf.set_x(0)
    pdf.set_margin(0)

    x = 3.05
    y = 3.05
    w = (61.95 - (3.05)) / 8
    h = (93.95 - (3.05)) / 14
    j = 0
    while y < (93.95 - .05):
        j += 1
        while x < (61.95 - .05):
            w1 = w * .7
            if j % 2 == 1:
                pdf.image(im3, x=x + ((w * .41) - (w1/2)), y=y + (h * .05), w=w1)
            else:
                pdf.image(im3.rotate(180), x=x + ((w * .58) - (w1/2)), y=y - (h * .05), w=w1)
            print("{0} {1}".format(x, y))
            x += w
        y += h
        x = 3.05

    pdf.rect(x=FORMAT[0]/2 - 8, y=28.5, w=16, h=26.5, style='F')
    pdf.image(im3, x=FORMAT[0]/2 - 7, y=30.3, w=14)

    pdf.set_y(48)
    pdf.set_font("ArialUnicode", '', 8)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(w=FORMAT[0], h=5, txt="● LIVE", align="C", fill=False, border=0)

    pdf.set_text_color(0)

    # safe_lines(pdf)
    # cut_lines(pdf)
    #
    # pdf.output("test.pdf")
    # sys.exit(0)
    # playing cards
    with open("{0}/Streamer Quartett - Sheet1.csv".format(CWD)) as csvfile:
        cr = list(csv.reader(csvfile,quoting=csv.QUOTE_ALL, skipinitialspace=True))
        groups = set([x[1] for x in cr if x[2] == 4 or x[2] == "4"])
        colors = seaborn.color_palette("husl", len(groups))
        grp_clr_ctr = dict(zip(
            groups,
            [[c, 0] for c in colors]))

        for person in cr:
            if person[2] != 4 and person[2] != "4":
                continue
            pdf.add_page()

            pfn = "{0}/players/{1}.jpg".format(CWD, str(person[0]).lower())
            if not os.path.exists(pfn):
                pfn = "{0}/players/placeholder.jpg".format(CWD)
            layer_player = Image.open(pfn) #.resize((80, 80), resample=Image.BILINEAR)

            imq = min(*layer_player.size)
            imw, imh = layer_player.size

            layer_player = layer_player.crop((math.floor(imw / 2 - imq / 2), math.floor(imh / 2 - imq / 2),
                                              math.floor(imw / 2 + imq / 2), math.floor(imh / 2 + imq / 2)))
            #copyright = parse_all_exif(layer_player.getexif())

            #for card in list(str(x) for x in range(2,11)) + ["S", "Q", "L", "A"]:

            pdf.set_fill_color(*[x * 255 for x in grp_clr_ctr[person[1]][0]])
            #pdf.line(x1=0, y1=0, x2=POS_X, y2=TEXT_POS_Y)


            pdf.set_margin(0)


            with pdf.rotation(angle=-3, x=FORMAT[0]/2, y=TEXT_POS_Y):
                pdf.image(layer_player.crop((0, 0, layer_player.size[0], layer_player.size[1] * .6)), x=-2, y=7,
                          w=FORMAT[0] + 5)

            with pdf.rotation(angle=3, x=FORMAT[0] / 2, y=TEXT_POS_Y):
                pdf.rect(x=-5, y=-15, w=FORMAT[0]+10, h=30, style='F')
                pdf.set_y(4)
                pdf.set_font("CaviarDreamsBold", '', 12)
                pdf.cell(w=FORMAT[0], h=10, txt=person[0], align="C", fill=False, border=0)


            pdf.set_y(4)  # TEXT_POS_Y)
            pdf.set_font("CaviarDreamsBold", '', 16)
            pdf.cell(w=4)
            grp_clr_ctr[person[1]][1] += 1
            pdf.cell(w=10, h=10, txt=str(grp_clr_ctr[person[1]][1]), align="C", fill=False, border=0)

            pdf.set_y(8)  # TEXT_POS_Y)
            pdf.set_font("CaviarDreams", '', 6)
            pdf.cell(w=4)
            pdf.cell(w=10, h=10, txt=person[1], align="C", fill=False, border=0)

            pdf.set_font("CaviarDreams", '', 7)

            pdf.image("{0}/symbols/TwitchGlitchPurple.eps".format(CWD), x=6, y=52, h=7)
            pdf.image("{0}/symbols/yt_icon_cymk.eps".format(CWD), x=35, y=52.5, w=7)
            pdf.image("{0}/symbols/viewer.eps".format(CWD), x=6, y=62.5, h=7)
            pdf.image("{0}/symbols/twitter.eps".format(CWD), x=35, y=63, w=7)
            pdf.image("{0}/symbols/subs.eps".format(CWD), x=5.5, y=72.5, h=7)
            pdf.image("{0}/symbols/office-calendar-desk-line.eps".format(CWD), x=35, y=73, h=7)
            pdf.image("{0}/symbols/money.eps".format(CWD), x=15, y=83, h=7)

            pdf.set_font("CaviarDreamsBold", '', 4)
            pdf.set_y(52)
            pdf.cell(w=14)
            pdf.cell(w=20, h=2, txt="Twitch Followers*", align="L", fill=False, border=0)
            pdf.set_y(52)
            pdf.cell(w=42)
            pdf.cell(w=20, h=2, txt="YouTube Subscribers*", align="L", fill=False, border=0)
            pdf.set_y(63)
            pdf.cell(w=14)
            pdf.cell(w=20, h=2, txt="Peak Concurrent Viewers*", align="L", fill=False, border=0)
            pdf.set_y(63)
            pdf.cell(w=42)
            pdf.cell(w=20, h=2, txt="Twitter Followers*", align="L", fill=False, border=0)
            pdf.set_y(73)
            pdf.cell(w=14)
            pdf.cell(w=20, h=2, txt="Peak Twitch Subscribers*", align="L", fill=False, border=0)
            pdf.set_y(73)
            pdf.cell(w=42)
            pdf.cell(w=20, h=2, txt="Year of Birth", align="L", fill=False, border=0)
            pdf.set_y(83)
            pdf.cell(w=21)
            pdf.cell(w=20, h=2, txt="Totally realistic Net Worth (according to Google)", align="L", fill=False, border=0)


            pdf.set_font("CaviarDreams", '', 10)
            pdf.set_y(54)
            pdf.cell(w=14)
            pdf.cell(w=20, h=5, txt=format_num_str(person[3]), align="L", fill=False, border=0)
            pdf.set_y(54)
            pdf.cell(w=42)
            pdf.cell(w=20, h=5, txt=format_num_str(person[7]), align="L", fill=False, border=0)
            pdf.set_y(65)
            pdf.cell(w=14)
            pdf.cell(w=20, h=5, txt=person[9], align="L", fill=False, border=0)
            pdf.set_y(65)
            pdf.cell(w=42)
            pdf.cell(w=20, h=5, txt=format_num_str(person[5]), align="L", fill=False, border=0)
            pdf.set_y(75)
            pdf.cell(w=14)
            pdf.cell(w=20, h=5, txt=person[8], align="L", fill=False, border=0)
            pdf.set_y(75)
            pdf.cell(w=42)
            pdf.cell(w=20, h=5, txt=person[14].replace('*', '‡'), align="L", fill=False, border=0)
            pdf.set_y(85)
            pdf.cell(w=21)
            pdf.cell(w=20, h=5, txt=person[15], align="L", fill=False, border=0)

            pdf.set_font("CaviarDreams", '', 4)
            pdf.set_y(92)
            pdf.set_x(5)
            pdf.cell(txt="* as of August 2021", align="L", fill=False, border=0)
            if '*' in person[14]:
                pdf.set_y(92)
                pdf.set_x(20)
                pdf.cell(txt="‡ Estimated, as the real value is (or seams) not publicly known", align="L", fill=False, border=0)


            # canvas.paste(layer_suit_c, (POS_X, SUIT_POS_Y), mask=layer_suit)
            # canvas.paste(layer_suit_c.rotate(180),
            #              (canvas.size[0] - POS_X - layer_suit.size[0],
            #               canvas.size[1] - SUIT_POS_Y - layer_suit.size[1]), mask=layer_suit.rotate(180))

            im = layer_player.crop((layer_player.size[0] * .85, 0, layer_player.size[0] * .95, layer_player.size[1] * .6)).convert('L')
            #im.show()
            stat = ImageStat.Stat(im)
            print("{0:25}: {1} {2}".format(person[0], stat.mean[0], stat.median[0]))
            if stat.median[0] > 180:
                pdf.set_text_color(0)
            else:
                pdf.set_text_color(255)

            pdf.set_y(50)
            pdf.set_x(60)
            with pdf.rotation(angle=90):
                pdf.set_font("helvetica", '', 4)
                #pdf.set_text_color(255)
                c = "Public Domain"
                if person[16]:
                    c = person[16]
                pdf.cell(txt="© " + c, align="L", fill=False, border=0)

            pdf.set_text_color(0)
            # cut_lines(pdf)

    pdf.output("{0}/quartett.pdf".format(CWD))
