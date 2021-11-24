# Import modules
import os
import sys
import yaml
from math import pi


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

    @classmethod
    def from_yaml(cls, string): # class method will return an instance
        """Create a circle from a yaml string"""
        circle_dict = yaml.load(string, Loader=yaml.Loader)
        print(circle_dict) # Need to check the dictionary when stantiate

        # Here instantiate the circle via deserialisation
        obj = cls(circle_dict["raidus"], fill=circle_dict["fill"], stroke=circle_dict["stroke"], at=circle_dict["at"])
        return obj


class Quadrilateral:
    def __init__(self, width, height, fill="blue", stroke = "red"):
        self._width = width
        self._height = height
        self._fill = fill
        self._stroke = stroke

    def calculate_area2(self):
        """Calculates the area of quadrilateral"""
        return self._width * self._height

    def __len__(self):
        return int(self._width + self._height + self._width + self._height)


class Canvas:
   def __init__(self, height, width, bg="grey"):
       self._height = height
       self._width = width
       self._bg = bg



# Class Text

def main():
    circle = Circle(5.0, fill="orange", stroke="red")
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

    return 0 #os.EX_OK

if __name__ == "__main__":
    sys.exit(main())
