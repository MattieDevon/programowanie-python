import os
import datetime
import time
import re
import json


WEEK = 604800
records = []


#wpis
class Record:
    def __init__(self, date, hasDuration, duration, highPriority, text):
        self.date = float(date)
        self.hasDuration = bool(hasDuration)
        self.duration = float(duration)
        self.highPriority = bool(highPriority)
        self.text = str(text)

    def toDict(self):
        return {
            'date': self.date,
            'hasDuration': self.hasDuration,
            'duration': self.duration,
            'highPriority': self.highPriority,
            'text': self.text
        }

    #def __eq__(self, other):
    #    return (self.date == other.date)
    def __lt__(self, other):
        return (self.date < other.date)
    def __le__(self, other):
        return (self.date <= other.date)
    def __gt__(self, other):
        return (self.date > other.date)
    def __ge__(self, other):
        return (self.date <= other.date)

    def __str__(self):
        if self.highPriority:
            temp=" !!! "
        else:
            temp=""
        if self.hasDuration:
            return temp + epoch2Hour(self.date) + "-" + epoch2Hour(self.date+self.duration) + temp + "\n" + self.text
        else:
            return temp + epoch2Hour(self.date) + temp + "\n" + self.text





#data na epoch
def stripEpoch(epoch): #to jest niepoprawne, poprawić później
    hour = int(datetime.datetime.fromtimestamp(epoch).strftime('%H'))
    minute = int(datetime.datetime.fromtimestamp(epoch).strftime('%M'))
    second = int(datetime.datetime.fromtimestamp(epoch).strftime('%S'))
    x = second + (minute * 60) + (hour * 3600)
    strippedEpoch = float(epoch - x).__floor__()
    return strippedEpoch


#epoch na date
def epoch2Date(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%d-%m-%Y')

#epoch na godzinę
def epoch2Hour(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%H:%M')

#epoch na dzień tygodnia
def epoch2Weekday(epoch):
    return num2Weekday(datetime.datetime.fromtimestamp(epoch).weekday())

def num2Weekday(num):
    if num == 0:
        return "Poniedziałek"
    elif num == 1:
        return "Wtorek"
    elif num == 2:
        return "Środa"
    elif num == 3:
        return "Czwartek"
    elif num == 4:
        return "Piątek"
    elif num == 5:
        return "Sobota"
    elif num == 6:
        return "Niedziela"
    else:
        return "ERROR"


#dodaje nową notatkę
def addNewRecord():

    regexPattern = re.compile( "([0-9]*):([0-9]*)" )

    #data
    inputString = input("Podaj datę (DD-MM-YYYY): ")
    while True:
        try:
            date = datetime.datetime.strptime(inputString,"%d-%m-%Y")
            date = date.timestamp()
            break
        except:
            inputString = input("Podaj poprawną datę (DD-MM-YYYY): ")
    #godzina
    while True:
        inputString = input("Podaj godzinę rozpoczęcia wydarzenia (HH:MM): ")
        match = regexPattern.match(inputString)
        try:
            if int(match.group(1)) < 24 and int(match.group(2)) < 60:
                czas = int(match.group(1)) * 3600 + int(match.group(2)) * 60
                date = date + czas
                break
            else:
                print("Podana godzina nie istnieje.")
        except TypeError:
            print("błąd")


    # godzina zakończenia

    while True:
        question = input("Czy chcesz określić godzinę zakończenia wydarzenia?[T/N]: ")
        if question == "T" or question == "t":
            hasDuration = True
            break
        elif question == "N" or question == "n":
            hasDuration = False
            break

    if hasDuration == True:
        while True:
            inputString = input("Podaj czas trwania wydarzenia (HH:MM): ")
            match = regexPattern.match(inputString)
            try:
                duration = int(match.group(1)) * 3600 + int(match.group(2)) * 60
                break
            except:
                print("błąd")
    else:
        duration = 0

    #określ priorytet

    while True:
        inputString = input("określ priorytet (0 = normlany, 1 = wysoki): ")
        try:
            if inputString == "1":
                highPriority = True
                break
            elif inputString == "0":
                highPriority = False
                break
        except:
            print("Błąd")
    #w końcu notatka
    text = input("Podaj tekst: ")
    #dodawanie do listy
    records.append(Record(date,hasDuration,duration,highPriority,text))
    #sortowanie listy
    records.sort()
    print("Wpis dodany.")


#usuwa po numerze w liście
def deleteByID():
    id = input("Podaj ID notatki którą chcesz usunąć: ")
    try:
        id = int(id)
        print(epoch2Date(records[id].date))
        print(records[id])
    except:
        print("Notatka o podanym numerze nie istnieje")
        return
    while True:
        question = input("Czy na pewno chcesz usunąć powyższy wpis[T/N]: ")
        if question == "T" or question == "t":
            records.pop(id)
            print("Notatka usunięta")
            break
        elif question == "N" or question == "n":
            print("Operacja anulowana")
            break

#usuwa stare wydarzenia
def clearPast():
    while True:
        question = input("Czy na pewno chcesz usunąć przeszłe wydarzenia [T/N]: ")
        if question == "T" or question == "t":
            today = time.time()
            while len(records) > 0:
                if records[0].date < today:
                    records.pop(0)
                else:
                    break
            break
        elif question == "N" or question == "n":
            break


#wyświetla wydarzenia w podanym zakresie
def display(start=0, stop=None, showID = False): #start in epoch, stop in epoch, showID bool
    lastDay = "eh"
    for id, record in enumerate(records):
        if start > stripEpoch(record.date): #szukanie rozpoczęcia
            continue
        if stop is not None: # BROKENBROKENBROKENBROKENBROKENBROKENBROKENBROKENBROKENBROKENBROKENBROKENBROKENBROKEN
            if stop < stripEpoch(record.date): #wczesne przerywanie jeżeli warunek końcowy został spełniony
                break

        if lastDay != epoch2Date(record.date): #wyświetlanide daty jeżeli notatka jest wpisana w kolejny dzień
            lastDay = epoch2Date(record.date)
            print(lastDay + ", " + num2Weekday((datetime.datetime.strptime(lastDay,"%d-%m-%Y").weekday())))

        if showID:
            print("ID: " + str(id))

        print(record)


def closeEvents():
    start = stripEpoch(time.time())
    stop = start + WEEK
    count = 0
    hpCounter = 0
    for note in records:
        if start <= note.date < stop:
            count = count + 1
            if note.highPriority:
                hpCounter = hpCounter + 1
    display(start, stop, False)
    print("W przyszłym tygodniu masz zapisanych " + str(count) + " wydarzeń, w tym " + str(hpCounter) + " określonych jako wysoki priorytet")


def save():
    jsonstr = json.dumps([ob.toDict() for ob in records])
    if os.path.isfile("./notatki/save_file.json"):
        if os.path.isfile("./notatki/save_file.json.backup"):
            print("Usuwanie starego backupu!")
            os.remove("./notatki/save_file.json.backup")
        os.rename("./notatki/save_file.json", "./notatki/save_file.json.backup")
        print("Utworzono backup!")
    try:
        with open("./notatki/save_file.json", "w") as file:
            file.write(jsonstr)
        print("zapis zakończony sukcesem!")
    except:
        pass


def load(): #wczytuje zapisane notatki do listy
    global records
    if os.path.isfile("./notatki/save_file.json") == False:
        print("Plik z zapisem nie istnieje")
    else:
        try:
            with open ("./notatki/save_file.json", "r") as file:
                jsstrings = json.load(file)
                records = []
                for eh in jsstrings:
                    records.append(Record(**eh))
                print("Odczyt pliku zakończony sukcesem")
        except:
            print("Odczyt pliku zakończony niepowodzeniem")


def initialize():
    print("Sprawdzanie czy folder z notatkami istnieje...")
    if os.path.exists("notatki") == False:
        print("Folder nie istnieje")
        try:
            os.mkdir("notatki")
            print("Folder został utworzony")
        except OSError as error:
            print(error)
    else:
        print("Folder istnieje...")

def printHelp():
    print("Zapisz - \"s\"")
    print("Wczytaj - \"l\"")
    print("Wyświetl wszystko - \"a\"")
    print("Wyświetl nadchodzące wydarzenia - \"c\"")
    print("Dodaj nowy wpis - \"n\"")
    print("Usuń wpis po ID - \"x\"")
    print("Usuń przeszłe wydarzenia - \"X\"")
    print("Wyjdź z programu - \"q\"")


def menu():

    query = input("> ")

    if query == "S" or query == "s":
        save()
    elif query == "l":
        load()
    elif query == "a":
        display()
    elif query == "A":
        display(showID=True)
    elif query == "c" or query == "C":
        closeEvents()
    elif query == "N" or query == "n":
        addNewRecord()
    elif query == "x":
        deleteByID()
    elif query == "X":
        clearPast()
    elif query == "h" or query == "H":
        printHelp()

    if query == "q" or query == "Q":
        while True:
            question = input("Czy chcesz zapisać zmiany przed wyjściem? [T/N]: ")
            if question == "T" or question == "t":
                save()
                break
            if question == "N" or question == "n":
                break
        print("Do widzenia.")
        return False
    else:
        return True


def test():
    today = time.time()
    print(datetime.datetime.fromtimestamp(today))
    print(datetime.datetime.fromtimestamp(stripEpoch(today)))


def powitanie():
    today = time.time()
    print("Dzień dobry, dzisiaj jest " + epoch2Date(today) + ", " + epoch2Weekday(today))
    print("Wpisz \"h\" aby uzyskać listę dostępnych poleceń")

def main():
    initialize()
    powitanie()
    #load()
    loop = True
    while loop:
        loop = menu()

if __name__ == '__main__':
    #test()
    main()


