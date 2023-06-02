from urllib.request import urlopen
import time
import os

from bs4 import BeautifulSoup

from roselia_songs import roselia_dict


def main():
    for composer, dict_ in roselia_dict.items():
        if not os.path.isdir("./{}".format(composer)):
            os.mkdir("./{}".format(composer))

        for song, html in dict_.items():
            print(composer, song)
            time.sleep(3)
            html = urlopen(html)
            bs = BeautifulSoup(html, "html.parser")

            chord = bs.find_all("span",class_="cd_fontpos")
            chord = [c.text for c in chord if c.text != "N.C."]
            print(chord, len(chord))

            PATH = "./{}/{}.txt".format(composer, song)
            with open(PATH, mode="w") as f:
                f.write('\n'.join(chord))

if __name__ == "__main__":
    main()
