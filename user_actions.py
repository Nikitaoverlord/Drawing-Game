# THIS IS user_actions.py FILE (NEW FILE)
import math
from kivy.graphics import Ellipse, Line
from kivy.graphics.context_instructions import Color
from kivy.uix.widget import Widget
#import main

sWidth = 1800 #675#1800
sHeight = 800 #300#800


def on_touch_down(self, touch):
    # if self.my_id % 2 == 0:
    # if touch.x < sWidth and touch.x > (sWidth - self.app.button_size * len(self.cursor_types)):
    # if touch.y < self.app.button_size and touch.y > 0:
    # print("yo")
    # return super(Widget, self).on_touch_down(touch)
    # else:
    # if touch.x < (self.app.button_size * len(self.cursor_types)) and touch.x > 0:
    # if touch.y < self.app.button_size and touch.y > 0:
    # print("yo")
    # return super(RelativeLayout, self).on_touch_down(touch)
    if self.win[0] == None:
        if self.cursor_type == "paintbrush":
            touch.ud['start_pos'] = (
                touch.x, touch.y
            ) # https://stackoverflow.com/questions/51841557/kivy-what-does-touch-ud-means
        #touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.paint_radius) # from
        #https://kivy.org/doc/stable/tutorials/firstwidget.html
        #self.lines.append([(touch.x, touch.y)]) # for server grade
        self.request_pixel = (round(touch.y), round(touch.x))

def on_touch_move(self, touch):
    if self.win[0] == None:
        if self.cursor_type == "paintbrush":
            self.request_pixel = (round(touch.y), round(touch.x))
            if (round(touch.y), round(touch.x)) == self.allowed_pixel:
                if 'start_pos' in touch.ud:
                    x_dist, y_dist = touch.x - touch.ud['start_pos'][0], touch.y - touch.ud['start_pos'][1]
                    dist = math.sqrt(x_dist**2 + y_dist**2)
                    angle = math.atan2(
                    y_dist, x_dist
                    ) # https://stackoverflow.com/questions/283406/what-is-the-difference-between-atanand-atan2-in-c

                    x_step = math.cos(
                    angle
                    ) * self.paint_radius # if dist>self.paint_radius else math.cos(angle)
                    y_step = math.sin(
                    angle
                    ) * self.paint_radius # if dist>self.paint_radius else math.sin(angle) # the*radius is for optimization

                    for i in range(
                        round(dist / self.paint_radius if dist > self.paint_radius else 1)):
                        x_pos = round(touch.ud['start_pos'][0] + i * x_step -
                            self.paint_radius) if x_dist != 0 else round(
                            touch.ud['start_pos'][0]) - self.paint_radius
                        y_pos = round(touch.ud['start_pos'][1] + i * y_step -
                            self.paint_radius) if y_dist != 0 else round(
                            touch.ud['start_pos'][1]) - self.paint_radius
                        with self.canvas:
                            r, g, b = self.color
                            Color(r, g, b)
                            Ellipse(pos=(x_pos, y_pos),
                                size=(self.paint_radius * 2, self.paint_radius * 2))

                            self.data[0].append([
                                round(x_pos + self.paint_radius),
                                round(y_pos + self.paint_radius), self.paint_radius
                            ])

                    touch.ud['start_pos'] = (
                        touch.x, touch.y
                    ) # new start point is at the end of the final ellipse

                    #touch.ud['line'].points += [touch.x, touch.y]
                    #self.lines[-1].append((touch.x, touch.y)) # for server code
                    #print(self.lines)