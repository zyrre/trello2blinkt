from trello import TrelloClient
import datetime, time, math
from blinkt import set_brightness, set_pixel, show


trelloClient = TrelloClient(
    api_key='trello_api_key',
    api_secret='trello_api_secret'
)

while True:
    # get todays list
    all_boards = trelloClient.list_boards()
    weekBoard = ''
    for board in all_boards:
        if board.name == 'Week':
            weekBoard = board
    lists = weekBoard.list_lists()
    currentDayList = lists[datetime.datetime.today().weekday()]

    # get time difference of the next scheduled card
    secondsToNext = 0
    if currentDayList.list_cards():
        # TODO add null check if there is no due date set on card
        for card in currentDayList.list_cards():
            if card.due_date.timestamp() > time.time():
                temp = int(card.due_date.timestamp()) - int(time.time())
                if temp < secondsToNext or secondsToNext == 0:
                    secondsToNext = temp
    else:
        secondsToNext = 0


    def timeToRGB(timeToNext):
        """takes time left until next task in seconds and outputs array of 8 LED RGB values"""
        minuteColor = [10, 10, 10]
        hourColor = [0, 0, 10]
        doneColor = [0, 10, 0]
        hourPixels = 0
        minutePixels = 0
        RGBarray = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        if timeToNext == 0:
            for x in range(0, 8):
                RGBarray[x] = doneColor
            return RGBarray

        # convert to hours + minutes
        minutesToNext = int(timeToNext / 60)
        hoursToNext, minutesToNext = divmod(minutesToNext, 60)

        # assign diff colors to RGBarray
        hourPixels = hoursToNext
        if hourPixels >= 8:
            hourPixels = 8
        else:
            minutePixels = int(math.ceil(minutesToNext / 10))
            if hourPixels + minutePixels > 8:
                minutePixels = 8 - hourPixels
        for x in range(0, hourPixels):
            RGBarray[x] = hourColor
        for x in range(hourPixels, hourPixels + minutePixels):
            RGBarray[x] = minuteColor
        print("hourPixels: " + str(hourPixels))
        print("minutePixels: " + str(minutePixels))
        print(RGBarray)
        return RGBarray

    def setPixels(arrayRGB):
        for x in range(0, 8):
            set_pixel(x, arrayRGB[x][0], arrayRGB[x][1], arrayRGB[x][2])


    RGB = timeToRGB(secondsToNext)
    setPixels(RGB)
    set_brightness(0.1)
    show()
    time.sleep(15)
