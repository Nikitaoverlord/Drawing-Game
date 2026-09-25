## DrawBattle (Multiplayer Game) (2022-23)

A cross-device multiplayer mobile battle game using the Pygame Kivy library and sockets. 
Originially made for my APCSP Portfolio project along with a writeup.
Using the Kivy library in Python to handle the GUI and allow mobile device access, and the python socket library to create different sockets to manage users from across platforms that are on the same wifi network. Started out as a project for the APCSP exam, then turned into a nearly finished personal project but with some remaining bugs. The game functions as 2 players try to "battle" to conver the entire canvas in their assigned paint color. You can draw, throw paint balloons, erase, and other features during the battel for domination.
<div align="center"><img width="800" height="375" alt="gameStart" src="https://github.com/user-attachments/assets/bd4ad224-3db6-4790-a552-8509c1aa1ab4" /></div>

## Demo
https://github.com/user-attachments/assets/f32ce9b6-52d1-43e5-bc4c-494919088ccf

## Features
 - Start screen to connect to local server with IP Adress (and player customization)
<div align="center"><img width="800" height="375" alt="connectPage" src="https://github.com/user-attachments/assets/39a41bca-21d3-4b0c-bd51-599e2441c118" /></div>
- Play against 1 other user in real time: draw, shoot balloons, waterfalls --> get to the other side)
<div align="center"><img width="800" height="375" alt="gamePlay" src="https://github.com/user-attachments/assets/565a3c00-a587-4433-b72d-407031436400" /></div>
<div align="center"><img width="800" height="375" alt="gamePlayVs" src="https://github.com/user-attachments/assets/d16f249d-0655-43a8-9ac8-03f78c329693" /></div>
- Win try again
<div align="center"><img width="800" height="375" alt="winScreen" src="https://github.com/user-attachments/assets/0ceea534-cce1-4c52-a6df-83de7864ffee" /></div>
<div align="center"><img width="800" height="375" alt="winner" src="https://github.com/user-attachments/assets/74e6274a-a2c7-4f9d-8ba3-3baa84c9cb1c" /></div>
- Live updates with python sockets and client ip address handling
- Can be distributed on mobile devices using the Kivy library

## Languages and Tools
- Python
- Kivy
- Socket
- Pickle
- All handrawn images
