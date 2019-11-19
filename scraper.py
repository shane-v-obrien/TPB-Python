import sys
from requests import get
from bs4 import BeautifulSoup
import webbrowser

tpb_url = 'https://piratebay.surf/search/'
tpb_url_end = "/0/99/0"


def print_logo():
    print(" ██████╗ ███████╗████████╗    ████████╗ ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗████████╗███████╗")
    print("██╔════╝ ██╔════╝╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔════╝")
    print("██║  ███╗█████╗     ██║          ██║   ██║   ██║██████╔╝██████╔╝█████╗  ██╔██╗ ██║   ██║   ███████╗")
    print("██║   ██║██╔══╝     ██║          ██║   ██║   ██║██╔══██╗██╔══██╗██╔══╝  ██║╚██╗██║   ██║   ╚════██║")
    print("╚██████╔╝███████╗   ██║          ██║   ╚██████╔╝██║  ██║██║  ██║███████╗██║ ╚████║   ██║   ███████║")
    print(" ╚═════╝ ╚══════╝   ╚═╝          ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝")
    print("                                                                                                   ")

def build_url(site, search):
    if site=="tpb":
        return tpb_url + search + tpb_url_end

def parse_tpb(contents):
    # empty result array
    result = []

    torrent_containers = contents.find_all('div', class_ = 'detName')

    # only return first 3 results
    for torrent in torrent_containers[0:5]:
        title = torrent.text
        parentDiv = torrent.parent
        magnetLink = parentDiv.find('a', title="Download this torrent using magnet")['href']
        details = parentDiv.find('font', class_ ='detDesc').text
        seeders = parentDiv.parent.find('td', align="right").text
        result.append({"title": title, "magnet": magnetLink, "details": details, "seeders": seeders})
    return result

def search_for_torrent(site, name):
    #build search url
    codified_name = name.replace(" ", "%20")
    full_url = build_url(site, codified_name)

    #search
    response = get(full_url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    return parse_tpb(html_soup)

def main():

    print_logo()
    movie = input("What would you like to download? ")

    print("Searching The Pirate Bay for " + movie)
    torrents = search_for_torrent("tpb", movie)

    print("  | Title" + " "*54 + "| Seeders")
    for i, torrent in enumerate(torrents, start=1):
        print(str(i) + ") " + torrent['title'].rstrip("\n") + " "*(60-len(torrent['title'].rstrip("\n"))) + "| " + torrent['seeders'])
    selection = input("Choose which item to download: ")
    print("Downloading: " + torrents[int(selection)-1]['title'])
    webbrowser.open_new(torrents[int(selection)-1]['magnet'])

if __name__ == "__main__":
    main()
