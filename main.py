
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.vertex_instructions import Quad
from kivy.graphics.vertex_instructions import Triangle
from kivy.core.audio import SoundLoader
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.properties import Clock
from kivy import platform
import random
import ast

class MainWidget(RelativeLayout):
    from user_actions import on_touch_down, on_touch_move

    background_image_number = NumericProperty(2)


    radius = 10

    erasor_on = BooleanProperty(False)

    tools = {"paintbrush": False, "splash": False, "paintfall": False, "paintballoon": True}


    cursor_location = Window.mouse_pos

    cursor_image_x = cursor_location[0]
    cursor_image_y = cursor_location[1]

    cursor_type = ""

    cursor_dp_offset = 0.15


    water_fall_on = False

    water_fall_y = [0]
    water_fall_x = [0]

    water_fall_width = [100]
    water_fall_height = [0]

    water_falls = []


    paint_balloon_on = False

    paint_balloons = []

    paint_balloon_x = []
    paint_balloon_y = []

    paint_balloon_init_y = []

    paint_balloon_time = [] #formula -5t^2 + 15t + y

    tool_bar_set = False

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.cursor_image = Image()
        self.add_widget(self.cursor_image)

        Clock.schedule_interval(self.update, 1/120)

    def create_tool_buttons(self, x, y, size):
        self.button_list = []
        for i in range(5):
            self.button_list.append( Button(pos=(x+i*(size/5), y), size=(size/5, size/5), color=(1,1,1,1), text=f"Button {i+1}") )

            self.add_widget(self.button_list[-1])


    def create_balloon(self, touch_x, touch_y):
        self.paint_balloon_on = True

        self.paint_balloon_x.append(touch_x)
        self.paint_balloon_y.append(touch_y)

        self.paint_balloon_init_y.append(touch_y)

        self.paint_balloon_time.append(0)

        self.paint_balloons.append(Image(source="Tool Images/paintballoon.png", size =((50*self.width/900), 50*(self.height/400))))
        self.paint_balloons[-1].pos = (touch_x, touch_y)
        self.paint_balloons[-1].size_hint = (dp(0.3), dp(0.3))

    def update_balloons(self):

        for balloon in self.paint_balloons: #formula -5t^2 + 15t + y
            time = self.paint_balloon_time[self.paint_balloons.index(balloon)]

            y = self.paint_balloon_y[self.paint_balloons.index(balloon)]
            init_y = self.paint_balloon_init_y[self.paint_balloons.index(balloon)]

            if (-4.9*time**2 + 30*time + init_y) < init_y: #formula finally less than 0
                self.balloon_splat(self.paint_balloon_x[self.paint_balloons.index(balloon)], self.paint_balloon_y[self.paint_balloons.index(balloon)], self.paint_balloons[self.paint_balloons.index(balloon)].size[0])

                self.paint_balloons[self.paint_balloons.index(balloon)].color = (0,0,0,0)#.remove_from_cache()

                self.paint_balloons.pop(0)
                self.paint_balloon_x.pop(0)
                self.paint_balloon_y.pop(0)
                self.paint_balloon_init_y.pop(0)
                self.paint_balloon_time.pop(0)

            else:
                self.paint_balloon_x[self.paint_balloons.index(balloon)] += 6
                self.paint_balloon_y[self.paint_balloons.index(balloon)] = (-4.9*time**2 + 15*time + init_y)

                self.paint_balloons[self.paint_balloons.index(balloon)].pos = (self.paint_balloon_x[self.paint_balloons.index(balloon)], self.paint_balloon_y[self.paint_balloons.index(balloon)])

                self.paint_balloon_time[self.paint_balloons.index(balloon)] += 0.15

    def balloon_splat(self, x, y, size):
        radius = size
        with self.canvas:
            Color(1, 0, 0)
            Ellipse(pos=(x, y), size=(radius, radius))
            #Color(1, 0, 0)
            Ellipse(pos=(x+radius/2, y), size=(30, 30))
            Ellipse(pos=(x-radius/4, y+radius/4), size=(25, 25))
            #Color(0, 1, 0)
            Ellipse(pos=(x+radius/3, y+radius/1.16), size=(10, 10))
            #Color(0, 0, 1)
            Ellipse(pos=(x, y), size=(25, 25))
            #Color(1, 1, 0)
            Ellipse(pos=(x, y), size=(13, 13))

    def paint_fall_action(self, touch_x):
        self.water_fall_on = True

        self.water_fall_y.append(self.height)
        self.water_fall_height.append(0)
        self.water_fall_width.append(100)

        self.water_fall_x.append(touch_x-self.water_fall_width[0]/2)

        #self.water_fall = Line(rectangle=(self.water_fall_x, self.water_fall_y, 0, 0))
        with self.canvas:
            Color(1, 0, 0, 1)
            self.water_falls.append(Rectangle(pos = (self.water_fall_x[-1], self.water_fall_y[-1]), size = (0, 0)))

    def update_waterfall(self):
        #if you want to put an animation for the waterfall, you can do that here later
        #print(self.water_falls)
        for waterfall in self.water_falls:
            if abs(self.water_fall_height[self.water_falls.index(waterfall)]) >= self.height:
                self.water_falls.pop(0)
                self.water_fall_x.pop(0)
                self.water_fall_y.pop(0)
                self.water_fall_width.pop(0)
                self.water_fall_height.pop(0)
            else:
                try:
                    self.water_fall_height[self.water_falls.index(waterfall)] -= 3.5
                    self.water_falls[self.water_falls.index(waterfall)].size = (self.water_fall_width[self.water_falls.index(waterfall)], self.water_fall_height[self.water_falls.index(waterfall)])
                except:
                    pass
                # self.water_fall.points[0] = self.water_fall_x
                # self.water_fall.points[1] = self.water_fall_y
                #
                # self.water_fall.points[2] = self.water_fall_width
                # self.water_fall.points[3] = self.water_fall_height


    def set_cursor(self, cursor_type):

        if cursor_type != None:
            Window.show_cursor = False

            dict_tools = list(self.tools.items())

            if cursor_type == dict_tools[0][0]: self.file_directory = "Tool Images/paintbrush.png"
            elif cursor_type == dict_tools[1][0]: self.file_directory = "Tool Images/splash.png"
            elif cursor_type == dict_tools[2][0]: self.file_directory = "Tool Images/paintfall.png"
            elif cursor_type == dict_tools[3][0]: self.file_directory = "Tool Images/paintballoon.png"

        else:
            Window.show_cursor = True
            self.file_directory = None

    def update_cursor(self, cursor_type):

        self.cursor_image_x = self.cursor_location[0]
        self.cursor_image_y = self.cursor_location[1]

        self.set_cursor(cursor_type)

        self.cursor_image.source = self.file_directory

        self.cursor_image.size_hint = (dp(self.cursor_dp_offset), dp(self.cursor_dp_offset))
        self.cursor_image.pos = (self.cursor_image_x-(self.cursor_dp_offset*225), self.cursor_image_y)

    def tool_assigner(self):
        false_counter = 0

        true_tool = ""
        for tool in self.tools:
            if self.tools[tool] == False:
                false_counter += 1
            else:
                true_tool = tool

        for tool in self.tools:
            if tool != true_tool:
                self.tools[tool] = False

        if false_counter == 0:
            self.tools["paintbrush"] = True

    def bring_cursor_to_front(self):
        self.remove_widget(self.cursor_image)
        self.add_widget(self.cursor_image)

    def update(self, dt):
        time_factor=dt*120

        self.bring_cursor_to_front()

        self.tool_assigner()

        if not self.tool_bar_set:
            self.create_tool_buttons(self.ids.toolbar.pos[0], self.ids.toolbar.pos[1], self.ids.toolbar.size[0])
            self.tool_bar_set = True

        self.cursor_type = ""
        for tool in self.tools:
            if self.tools[tool] == True:
                self.cursor_type = tool

        self.update_cursor(self.cursor_type)

        over_height_waterfalls = 0

        if self.water_fall_on:
            for height in self.water_fall_height:
                if abs(height) > self.height:
                    over_height_waterfalls += 1

        #print(len(self.water_falls), over_height_waterfalls)
        if over_height_waterfalls == len(self.water_falls):
            self.water_fall_on = False
        else:
            self.update_waterfall()
            #print(len(self.water_falls), over_height_waterfalls)

        balloon_back = 0

        if self.paint_balloon_on:
            for balloon in self.paint_balloons:
                time = self.paint_balloon_time[self.paint_balloons.index(balloon)]
                y = self.paint_balloon_y[self.paint_balloons.index(balloon)]
                init_y = self.paint_balloon_init_y[self.paint_balloons.index(balloon)]

                if (-4.9*time**2 + 15*time + init_y) < init_y:
                    balloon_back += 1

        #print(len(self.water_falls), over_height_waterfalls)
        if balloon_back == len(self.paint_balloons):
            self.paint_balloon_on = False
        else:
            self.update_balloons()
            #print(len(self.water_falls), over_height_waterfalls)



class PaintBattleApp(App):
    pass




PaintBattleApp().run()
