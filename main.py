# Import modules
import os
import sys
import yaml
import turtle
from math import pi

turtle.tracer(False)

# Define the class circle
class Circle:
    # Basic attributes
    def __init__(self, radius, fill='red', stroke='black', at =(0, 0)):
        self._radius = radius #private/protected
        self._fill = fill
        self._stroke = stroke
        self._at = at

    # Make the private properties "._" public
    @property
    def radius(self): # make public access for _radius: read-only. Once a circle is created its radius cant be changed
        return self.radius # reflecting the private as a public

    # Calculate the area
    def calculate_area(self):
        """Calculates the area"""
        return pi * self._radius ** 2

    # Calculate the length (perimeter) note in the main function, can specify len(circle - when circle defined)
    def __len__(self):
        return int(2 * pi * self.radius)

    def __call__(self):
        return "I am a circle"

    def __str__(self):
        return f"Instance of {self.__class__.__qualname__}"

    def __repr__(self):
        return(f"Circle({self._radius}, fill= {self._fill}, stroke={self._stroke}, at={0, 0}")

    def __str__(self):
        string = yaml.dump({
            "circle" : {
                "radius" : self._radius,
                "fill" : self._fill,
                "stroke" : self._stroke,
                "at" : self._at
            }
        })
        return string

    def draw(self, pen):
        """Draw a circle"""
        if pen.isdown():
            pen.up()
        pen.goto(*self._at)
        pen.down()
        pen.begin_fill()
        pen.pencolor(self._stroke)
        pen.fillcolor(self._fill)
        pen.circle(self._radius)
        pen.end_fill()
        pen.up()

    @classmethod
    def from_yaml(cls, string): # class method will return an instance
        """Create a circle from a yaml string"""
        circle_dict = yaml.load(string, Loader=yaml.Loader)
        print(circle_dict) # Need to check the dictionary when stantiate

        # Here instantiate the circle via deserialisation
        obj = cls(circle_dict["radius"], fill=circle_dict["fill"], stroke=circle_dict["stroke"], at=circle_dict["at"])
        return obj


class Quadrilateral:
    def __init__(self, width, height, fill="blue", stroke = "red", at=(0,0)):
        self._width = width
        self._height = height
        self._fill = fill
        self._stroke = stroke
        self._at = at

    @property
    def left(self):
        return self._at[0] - self._width / 2

    @property
    def top(self):
        return self._at[1] + self._height / 2

    @property
    def right(self):
        return self._at[0] + self._width / 2

    @property
    def bottom(self):
        return self._at[1] - self._width / 2

    @property
    def vertices(self):
        """start from top left and go counter clockwise"""
        return [
            (self.left, self.top),
            (self.left, self.bottom),
            (self.right, self.bottom),
            (self.right, self.top),
        ]


    def draw(self, pen, *args, **kwargs):
        pen.begin_fill()
        pen.pencolor(self._stroke)
        pen.fillcolor(self._fill)
        pen.up()
        pen.goto(self.left, self.top)
        pen.down()
        pen.goto(self.left,self.bottom)
        pen.goto(self.right, self.bottom)
        pen.goto(self.right, self.top)
        pen.goto(self.left, self.top)
        pen.up()
        pen.end_fill()



    def calculate_area2(self):
        """Calculates the area of quadrilateral"""
        return self._width * self._height

    def __len__(self):
        return int(self._width + self._height + self._width + self._height)


class Canvas(turtle.TurtleScreen):
    def __init__(self, height, width, bg="lightgrey"):
        self._cv = turtle.getcanvas()
        super().__init__(self._cv) # super is a special function to refer to the title class (Canvas)
        self.screensize(width, height, bg=bg)
        self._height = height
        self._width = width
        self._bg = bg
        self._pen = turtle.Turtle()
        self._pen.hideturtle()
        self._gb = bg

    def draw_axes(self):
        self._pen.up()
        self._pen.goto(0, self._height / 2)
        self._pen.down()
        self._pen.goto(0, -self._height / 2)
        self._pen.up()
        self._pen.goto(-self._width / 2, 0)
        self._pen.down()
        self._pen.goto(self._width / 2, 0)
        self._pen.up()
        self._pen.goto(-self._width / 2, -self._height / 2)

    def draw_grid(self, colour='#dddddd', hstep=50, vstep=50):
        # self._pen.speed(0)
        original_pen_colour = self._pen.pencolor()
        self._pen.color(colour)
        # vertical grids
        self._pen.up()
        for hpos in range(-500, 500 + hstep, hstep):
            self._pen.goto(hpos, 350)
            self._pen.down()
            self._pen.goto(hpos, -350)
            self._pen.up()
        # horizontal grids
        for vpos in range(-350, 350 + vstep, vstep):
            self._pen.goto(-500, vpos)
            self._pen.down()
            self._pen.goto(500, vpos)
            self._pen.up()
        # reset
        self._pen.pencolor(original_pen_colour)

    def draw(self, shape):
        """shape specified"""
        shape.draw(self._pen)

    def write(self, text, *args, **kwargs):
        text.write(self._pen, *args, **kwargs)



class Text:
    def __init__(self, text, at=(0,0), color = "black"):
        self._text = text
        self._at = at
        self._color = color

    def write(self, pen, *args, **kwargs):
        pen.pencolor(self._color)
        pen.up()
        pen.goto(self._at)
        pen.down()
        pen.write(self._text, *args, **kwargs)
        pen.up()

def main():
    circle = Circle(20.0, fill="orange", stroke="red")
    quadrilateral = Quadrilateral(5.0, 8.0, fill="orange", stroke="red")
    print(f"Area = {Circle.calculate_area(circle)}")
    print(f"Circumference of circle is {len(circle())}")
    print(circle())
    print(str(circle))
    print(repr(circle))
    print(f"Area of quadrilateral = {Quadrilateral.calculate_area2(quadrilateral)}")

    my_dict = {
        "key" : {
            "inside_dict": [5, 6, 7, 8]
        }
    }
    my_yaml = yaml.dump(my_dict)
    print(my_yaml)

    # Work on class to produce an instance
    yaml_circle = """\
circle:
at: !!python/tuple
- 0
- 0
fill: orange
radius: 5.0
stroke: red"""
    my_circle = Circle.from_yaml(yaml_circle) # use classmethod to load the circle described above in yaml syntax
    pen = turtle.Turtle() # draw with a turtle
    text = Text("This was written by a turtle!")
    print(text)
    text.write(pen, font=('Arial', 10, 'bold'))

    circle.draw(pen)

    #Quad
    quad = Quadrilateral(200, 60, at=(215,-5))
    print(f"vertices={quad.vertices}")
    quad.draw(pen)

    # Canvas
    canvas = Canvas(1600, 700, bg="lightgrey")
    canvas.draw_axes()
    canvas.draw_grid()
    canvas.draw(circle)
    canvas.write(text)

    canvas = Canvas(1000, 700)
    gquad = Quadrilateral(200, 300, fill='#006400', stroke='white', at=(-200, 0))
    wquad = Quadrilateral(200, 300, fill='white', stroke='#dddddd', at=(0, 0))
    oquad = Quadrilateral(200, 300, fill='darkorange', stroke='white', at=(200, 0))

    text = Text('IRELAND', at=(0, -250), color = "black")
    canvas.draw(gquad)
    canvas.draw(wquad)
    canvas.draw(oquad)
    canvas.write(text, align='center', font=('Arial', 60, 'bold'))

    turtle.done()

    return 0 #os.EX_OK



if __name__ == "__main__":
    sys.exit(main())
