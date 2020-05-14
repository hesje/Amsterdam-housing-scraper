import requests
from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode

urls = [
"http://roomselector.studentexperience.nl/plattegrond.php?pagina=2&begane-grond",
"http://roomselector.studentexperience.nl/plattegrond.php?pagina=2&eerste-verdieping",
"http://roomselector.studentexperience.nl/plattegrond.php?pagina=2&tweede-verdieping",
"http://roomselector.studentexperience.nl/plattegrond.php?pagina=2&derde-verdieping",
"http://roomselector.studentexperience.nl/plattegrond.php?pagina=2&vierde-verdieping",
"http://ravelresidence.studentexperience.nl/plattegrond.php?pagina=2&begane-grond",
"http://ravelresidence.studentexperience.nl/plattegrond.php?pagina=2&eerste-verdieping",
"http://ravelresidence.studentexperience.nl/plattegrond.php?pagina=2&tweede-verdieping",
"http://ravelresidence.studentexperience.nl/plattegrond.php?pagina=2&derde-verdieping",
"http://ravelresidence.studentexperience.nl/plattegrond.php?pagina=2&vierde-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&eerste-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&tweede-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&derde-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&vierde-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&vijfde-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&zesde-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&zevende-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&achtste-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&negende-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&tiende-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&elfde-verdieping",
"http://nautiqueliving.studentexperience.nl/plattegrond.php?pagina=2&twaalfde-verdieping"
]

pushsafer_key = "R0GLRtfhGuP7iTReaF2I"

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri"]
prev_avail_rooms = []

def find_rooms():
    print("searching rooms...")
    avail_rooms = []

    for url in urls:
        print("#", end="")
        response = requests.get(url)
        html = BeautifulSoup(response.text, "html.parser")

        rooms = html.findAll('a')

        for room in rooms:
            if room['href'] == "#":
                if (room['class'][0] != "verhuurd" and room['class'][0] != "option"):
                    avail_rooms.append(url)
    print(" Done")

    return avail_rooms

def push_notif(rooms):

    message = "There are {} rooms available on StudentExperience at the moment".format(len(rooms))

    url = 'https://www.pushsafer.com/api' # Set destination URL here
    post_fields = {                       # Set POST fields here
    	"t" : "New rooms on StudentExperience",
    	"m" : message,
    	"s" : "",
    	"v" : 3,
    	"i" : 81,
    	"c" : "",
    	"d" : "a",
    	"u" : rooms[0],
    	"ut" : "StudentExperience",
    	"k" : pushsafer_key
    	}

    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()
    print(json)


while True:
    t = time.asctime( time.localtime(time.time()) )
    d = (t.split())[0]
    h = int(t.split()[3].split(":")[0])


    if d in weekdays:
        if h > 11 and h < 14:
            rooms = find_rooms()
            if len(rooms) > 0:
                if prev_avail_rooms != rooms:
                    print(rooms)
                    #push_notif(rooms)
                    prev_avail_rooms = rooms

    time.sleep(20)
