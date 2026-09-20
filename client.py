# THIS IS server.py FILE
import socket #https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
import _pickle as pickle
from _thread import *
import math, time

HOST = "192.168.1.23"#"10.10.108.64" #"192.168.1.23" #socket.gethostname()#HOST =
#"192.168.56.1" # Standard loopback interface address (localhost)
PORT = 12345 # Port to listen on (non-privileged ports are > 1023)

print(HOST)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((HOST, PORT))
except socket.error as problem:
    print(str(problem))
    quit()

# GAME VARS
sWidth = 1800 #675#1800
sHeight = 800 #300#800

winner = None

pixel_list = []

time_add = 0.1 # seconds
timer = 0 + time_add
timer_stop = False

def reset_pixel_list():
    global pixel_list
    pixel_list = []
    for i in range(sHeight):
        pixel_list.append([])
        for x in range(sWidth):
            pixel_list[-1].append(None) # None-empty, or (r,g,b)


reset_pixel_list()


# THIS IS PROBABLY THE FUNCTION TO USE AS PROCEDURE AND THE PIXEL_LIST IS THE MAIN_LIST
def update_pixel_list(x,y,radius,color,circle=True): # remember since pixel_list contains every pixel the x and y will correspond to indexvalues
    global pixel_list

    for x_count in range(radius * 2 + 1): # plus 1 because the range(goes from 0 to radius*2-1)
        for y_count in range(radius * 2 + 1):
            x_index = x - (radius - x_count)
            y_index = y - (radius - y_count) # without the if, it would just assign pixels in a square not a circle

            if circle:
                if math.sqrt((radius-x_count)**2 + (radius-y_count)**2) <= radius \
                and x_index >= 0 and y_index >= 0 and x_index < sWidth and y_index < sHeight: #sHeight is len(pixel_list)-1
                    pixel_list[y_index][x_index] = color
            else:
                if x_index >= 0 and y_index >= 0 and x_index < sWidth and y_index < sHeight:
                    pixel_list[y_index][x_index] = color


def initial_pixel_setup(id, color):
    radius = round(sHeight / 4)
    if id % 2 == 0:
        x = sWidth
        y = round(sHeight / 2)
        update_pixel_list(x, y, radius, color, circle=False)
    else:
        x = 0
        y = round(sHeight / 2)
        update_pixel_list(x, y, radius, color, circle=False)

    for player in id_to_shapes:
        if player != id:
            id_to_shapes[player].append([x, y, radius, color, True])
def getTotalArea(color):
    area = 0
    for i in range(sHeight):
        for x in range(sWidth):
            if pixel_list[i][x] == color:
                area += 1
    return area


def check_for_winner(id, color):
    global winner
    if id % 2 == 0:
        for row in pixel_list:
            if row[0] == color:
                winner = id
    else:
        for row in pixel_list:
            if row[-1] == color:
                winner = id


def server_thread(*args):
    global timer
    global timer_stop

    while True:
        if winner != None:
            timer_stop = True

        if not timer_stop:
            timer = round(timer + time_add, 1)
            time.sleep(time_add)


def client_thread(user, id):
    global clients, winner

    data = user.recv(64)
    data = data.decode("utf-8").split(" ")

    name, color_string = data
    color = color_string.split(",")

    user.send(str(id).encode())

    initial_pixel_setup(id, color)

    weapons = {"paintbrush": 100, "paintballoon": 2, "paintfall": 2}
    paint_radius = round(sWidth / 180)
    balloon_size = round(sWidth / 36)
    paintfall_width = round(sWidth / 72)
    paint_time = 1
    balloon_time = 20
    fall_time = 25

    last_timer = timer

    while True:
        try:
            data = user.recv(2048 * 4) # list of lists

            if not data: # if no data is being recieved, user has disconnected from server
                break

            reply = pickle.loads(data)

            if winner == None:
                update_list = reply[0]
                for item in update_list:
                    x,y,radius = item[0], item[1], item[2]
                    update_pixel_list(x, y, radius, color, circle=True)

                # if item[2] == paint_radius:
                # weapons["paintbrush"] -= 1
                # elif item[2] == balloon_size:
                # weapons["paintballoon"] -= 1
                # elif item[2] == paintfall_width:
                # weapons["paintfall"] -= 1

                for player in id_to_shapes:
                    if player != id:
                        id_to_shapes[player].append([item[0], item[1], item[2], color])

                allowed_pixel = None
                test_pixel = reply[1]
                weapon = reply[2]
                if test_pixel != None:
                    if pixel_list[test_pixel[0] - 1][test_pixel[1] - 1] == color:
                        if weapons[weapon] > 0:
                            allowed_pixel = test_pixel[1], test_pixel[0]
                            weapons[weapon] -= 1

                        if weapon == "paintfall":
                            weapons["paintbrush"] += 15

                check_for_winner(id, color)

                missing_shapes = None
                id_shapes_length = len(id_to_shapes[id])
                if id_to_shapes[id] != []:
                    missing_shapes = id_to_shapes[id]
                    id_to_shapes[id] = id_to_shapes[id][id_shapes_length - 1:-1]
            else:
                allowed_pixel = None
                missing_shapes = None

            # timer:
            if last_timer != timer:
                if timer % paint_time == 0 and weapons["paintbrush"] < 200:
                    weapons["paintbrush"] += 5
                if timer % balloon_time == 0 and weapons["paintballoon"] < 4:
                    weapons["paintballoon"] += 1
                if timer % fall_time == 0 and weapons["paintfall"] < 5:
                    weapons["paintfall"] += 1
                last_timer = timer

            area = None
            if winner != None and area == None:
                area = getTotalArea(color)

            win_info = (winner, area)

            relay_data = pickle.dumps(
                (allowed_pixel, missing_shapes, win_info, weapons, timer))

            user.send(relay_data)

        except Exception as error:
            print("Error:", error)
            break

    del clients[id]
    del id_to_shapes[id]
    user.close()
    print(f"USER CLOSED [id #{id}]")


def reset_game():
    global timer, winner, timer_stop

    reset_pixel_list()
    timer = 0
    winner = None
    timer_stop = False

server.listen()

clients = {} #{1:"127.0.0.1"} # id to ip

global_id = 1
id_to_user = {} #1:"name"

id_to_shapes = {} # 1:[["x, y, radius, color]]

first_player = None # socket, id
while True:

    user_socket, address = server.accept()
    print(address[0] + " connected")

    clients[global_id] = address
    id_to_shapes[global_id] = []

    if global_id % 2 == 0:
        reset_game()

        start_new_thread(client_thread, (first_player[0], first_player[1]))
        start_new_thread(
            client_thread, (user_socket, global_id)
        ) # system of threading to handle individual clients inspired from https://github.com/techwithtim/Agar-IO

        start_new_thread(server_thread, (None, None))
        first_player = None
    else:
        first_player = user_socket, global_id
        global_id += 1