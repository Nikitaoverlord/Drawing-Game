from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Ellipse, Line
from kivy.graphics.context_instructions import Color

def on_touch_down(self, touch):
    self.cursor_location = touch.pos
    with self.canvas:
        if not self.erasor_on and self.cursor_type == "paintbrush":
            Color(1, 0, 0)
            #Ellipse(pos=(touch.x - self.radius / 2, touch.y - self.radius / 2), size=(self.radius, self.radius))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.radius)
        elif self.cursor_type != "paintbrush":
            if self.cursor_type == "splash":
                radius = 150
                Color(1, 0, 0)
                Ellipse(pos=(touch.x - radius / 2, touch.y - radius / 2), size=(radius, radius)) #the 10 is the radius
                #Color(1, 0, 0)
                Ellipse(pos=(touch.x - radius / 2, touch.y), size=(90, 90))
                Ellipse(pos=(touch.x - radius/ 4, touch.y - radius / 4), size=(75, 75))
                #Color(0, 1, 0)
                Ellipse(pos=(touch.x, touch.y - radius / 1.8), size=(30, 30))
                Ellipse(pos=(touch.x - radius / 8, touch.y + radius / 6), size=(60, 60))
                #Color(0, 0, 1)
                Ellipse(pos=(touch.x - radius / 1.75, touch.y), size=(30, 30))
                Ellipse(pos=(touch.x + radius / 8, touch.y + radius / 8), size=(75, 75))
                #Color(1, 1, 0)
                #Ellipse(pos=(touch.x + radius / 4, touch.y - radius / 2), size=(25, 25))
                Ellipse(pos=(touch.x + radius / 2.5, touch.y - radius/4), size=(35, 35))
                #Color(0, 0, 0)
                Ellipse(pos=(touch.x - radius / 4, touch.y - radius/1.80), size=(40, 40))

            if self.cursor_type == "paintfall":
                self.paint_fall_action(touch.x)
            if self.cursor_type == "paintballoon":
                self.create_balloon(touch.x, touch.y)
        else:
            Color(255, 255, 255, 1)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.radius)


def on_touch_move(self, touch):
    self.cursor_location = touch.pos
    if not self.erasor_on and self.cursor_type == "paintbrush":
        c = Color(1, 0, 0)
        touch.ud['line'].points += touch.x, touch.y
    elif self.cursor_type != "paintbrush":
        pass
    elif self.cursor_type != "paintfall":
        pass
    elif self.cursor_type != "paintballoon":
        pass
    else:
        Color(255, 255, 255, 1)
        touch.ud['line'].points += touch.x, touch.y
