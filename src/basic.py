#!/usr/bin/env python3

"""
Computer delaunay triangulations of a randomly generated list of triangles

Using the s-hull algorithm described here:
http://www.s-hull.org/paper/s_hull.pdf

# http://www.qhull.org/html/index.htm
# http://www.cs.mcgill.ca/~fukuda/soft/polyfaq/polyfaq.html
"""

import math
import random

### todo

# 2. Right-handed ordering of points on a circle.
# 3. check if two segments intersect. (http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect)
# 4. The Euclidean minimum spanning tree of a set of points is a subset of the Delaunay triangulation of the same points, and this can be exploited to compute it efficiently.
# 5. convex hull

#Constrained Delaunay triangulation
# https://en.wikipedia.org/wiki/Mesh_generation
# https://www.openmesh.org/


class Point(object):
    """
    A point
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __hash__(self):
        t = (self.x, self.y)
        return hash(t)

    def __add__(self, p2):
        x = self.x + p2.x
        y = self.y + p2.y
        return Point(x, y)

    def __sub__(self, p2):
        x = self.x - p2.x
        y = self.y - p2.y
        return Point(x, y)

    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y

    def distance(self, p2):
        d_squared = (self.x - p2.x)**2 + (self.y - p2.y)**2
        return math.sqrt(d_squared)

    def draw(self):
        import rhinoscriptsyntax as rs
        rs.AddPoint([self.x, self.y, 0])

    def cross_product(self, p2):
        return (self.x * p2.y) - (self.y * p2.x)


def points_average(points):
    """
    Take the average of a list of points.
    """
    xs = sum([p.x for p in points])
    ys = sum([p.y for p in points])
    count = float(len(points))
    average = Point(xs/count, ys/count)
    return average


class Segment(object):
    """
    A line segment
    """
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def __repr__(self):
        return "Segment {}, {}".format(self.p1, self.p2)

    def move(self, vector):
        return Segment(self.p1+vector, self.p2+vector)

    def vector(self):
        return self.p2 - self.p1

    def intersects(self, s2):
        p = self.p1
        q = s2.p1
        r = self.vector()
        s = s2.vector()

        r_cross_s = r.cross_product(s)

        if r_cross_s == 0:
            return False   # todo: fix case of two collinear, overlapping segments

        t = (q - p).cross_product(s) / r_cross_s
        u = (q - p).cross_product(r) / r_cross_s
        return (0 <= t <= 1) and (0 <= u <= 1)

    def draw(self):
        import rhinoscriptsyntax as rs
        rs.AddLine([self.p1.x, self.p1.y, 0], [self.p2.x, self.p2.y, 0])


class Circle(object):
    """
    the set of all points in a plane that are at a given distance from a given point, the centre.
    """
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return "Circle (c={}, r={})".format(self.center, self.radius)

    def distance(self, point):
        return point.distance(self.center)

    def distance_from_edge(self, point):
        d = self.distance(point)

        if d > self.radius:
            return d - self.radius
        else:
            return self.radius - d
            
    def inside(self, point):
        return self.distance(point) < self.radius


    def draw(self):
        import rhinoscriptsyntax as rs
        rs.AddCircle([self.center.x, self.center.y, 0], self.radius)
        

    def cartesian_to_polar(self, p): pass
    def polar_to_cartesian(theta): pass


class Triangle(object):
    """
    A triangle is a polygon with three edges and three vertices. 
    It is one of the basic shapes in geometry.
    """
    
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def segments(self):
        return [
            Segment(self.p1, self.p2),
            Segment(self.p2, self.p3),
            Segment(self.p3, self.p1),
            ]

    def circumcenter(self):
        """
        The center point of the circle that circumscribes three points.
        """
    
        b_ = self.p2 - self.p1
        c_ = self.p3 - self.p1

        D_ = 2 * (b_.x * c_.y - b_.y * c_.x)

        x = (c_.y * (b_.x**2 + b_.y**2) - b_.y * (c_.x**2 + c_.y**2)) / D_
        y = (b_.x * (c_.x ** 2 + c_.y ** 2) - c_.x * (b_.x **2 + b_.y**2)) / D_

        cc = Point(x,y) + self.p1

        return cc
        
    def circumcircle(self):
        center = self.circumcenter()
        radius = center.distance(self.p1)
        return Circle(center, radius)


    def draw(self):
        for segment in self.segments():
            segment.draw()



class Path(object): pass    

class Mesh(object): pass

class Voronoi(object): pass



class Triangulation(object): 

    def __init__(self, triangles):
        self.triangles = triangles
    

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def points(self):
        s = set()
        for triangle in self.triangles:
            s.add(triangle.p1)
            s.add(triangle.p2)
            s.add(triangle.p3)

        return s

    def segments(self):
        s = set()

        for triangle in self.triangles:
            for segment in triangle.segments():
                s.add(segment)


class Graph(object): 

    def __init__(self, edges=None):
        if edges is None:
            edges = []

        self.edges = set(edges)

    def vertices(self):
        s = set()
        for edge in self.edges:
            s.add(edge.p1)
            s.add(edge.p2)

        return s


    def add_edge(self, edge):
        self.edges.add(edge)

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)

    def add_triangle(self, triangle):
        self.add_edges(triangle.segments())

    def intersects_edge(self, segment):
        for edge in self.edges:
            if segment.intersects(edge):
                return True

        return False


def main():
    """
    Generate connection images
    """

    test()



    #points = random_points(100, 10)
    #center = points_average(points)

    #connect_points(points)

    #delaunay_algorithms(points)
    
    #shull()
        
    
def shull():
    points = random_points(100, 10)

    average_point = points_average(points) # Maybe just pick a point at random.
    sorted_points = sorted(points, key=lambda p: average_point.distance(p))
    seed_point = sorted_points[0]
    sorted_by_seed = sorted(sorted_points[1:], key=lambda p: seed_point.distance(p))
    p2 = sorted_by_seed[0]
    circumcircle_sorted = sorted(sorted_by_seed[1:], key=lambda p: Triangle(seed_point, p2, p).circumcircle().radius)
    p3 = circumcircle_sorted[0]
    triangle = Triangle(seed_point, p2, p3)

    circumcenter = triangle.circumcenter()
    points_from_circumcenter = sorted(circumcircle_sorted[1:], key=lambda p: circumcenter.distance(p))


    g = Graph()
    g.add_triangle(triangle)

    for p1 in points_from_circumcenter:
        added_points = g.vertices()
        for p2 in added_points:
            s1 = Segment(p1, p2)
            if not g.intersects_edge(s1):
                print("adding edge")
                g.add_edge(s1)


    #for edge in g.edges:
    #    edge.draw()



                

        

    

    
    

    
    
    
    


def draw_all_lines(points):
    """
    Draw every line. Excessive.
    """
    for start in points:
        for end in points:
            if start != end:
                line = Segment(start, end)
                line.draw()


def connect_points(points):
    """
    Connect each point to two random points
    """

    npoints = points[:]
    random.shuffle(npoints)

    segments = [Segment(start, end) for (start, end) in zip(npoints, npoints[1:])]
    for s in segments:
        s.draw()


def delaunay_algorithms(points):

    # https://en.wikipedia.org/wiki/Delaunay_triangulation#Algorithms

    for segment in incremental(points):
        segment.move(Point(20,0)).draw()

    flip(points)
    sweephull(points)


def incremental(points):
    unconnected = points

    [point.draw() for point in unconnected]
    connected = set()

    previous = unconnected.pop()
    p2 = unconnected.pop()
    segments = []
    
    while unconnected:
        unconnected = sorted(unconnected, key=lambda p: previous.distance(p))
        point = unconnected.pop(0)
        segment = Segment(previous, point)
        segments.append(segment)
        previous = point

    return segments
        

def flip(points): pass
def sweephull(points): pass


def random_points(n, scale=1):
    
    xs = [scale * random.random() for e in range(n)]
    ys = [scale * random.random() for e in range(n)]
    zs = [scale * 0 for e in range(n)]
    return [Point(*p) for p in zip(xs, ys)]


if __name__ == "__main__":
    main()
