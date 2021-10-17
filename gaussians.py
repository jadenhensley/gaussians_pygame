import pygame
import random
import numpy
from text import *

width = 800
height = 600

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gaussians Demo")
pygame.init()
clock = pygame.time.Clock()

# pygame.font.init()

def get_gaussian():
    i = numpy.random.normal()
    return i

def clamp_rgb(n, min_rgb=0, max_rgb=255):
    if max_rgb > 255:
        max_rgb = 255
    if min_rgb < 0:
        min_rgb = 0
    return max(min(max_rgb, n), min_rgb)

def clamp_by_length(n, array):
    return max(min(len(array) - 1, n), 0)

class BarChart():
    def __init__(self):
        self.num_bars = 50
        self.color = (0,255,0, 10)
        self.outline = (0,0,0)
        self.standard_deviation = 30
        self.mean_h = 80
        self.mean_s = 2
        self.randomness = "totally random"
        self.bars = []
        for bar in range(self.num_bars):
            self.bars.append(100)

    def draw(self):
        h = get_gaussian() * self.standard_deviation + self.mean_h
        selected_bar = get_gaussian() * len(self.bars)/2 + self.mean_s
        selected_bar = clamp_by_length(int(abs(selected_bar)), self.bars)
        # print(selected_bar)

        # for random colorization!
        # print(abs(int(h)))

        c = abs(int(h))
        
        # rc = clamp_rgb(c, 0, 50)
        # gc = clamp_rgb(c, 100, 255)
        rc = clamp_rgb(c, 170, 255)
        gc = clamp_rgb(c, 0, 20)
        # bc = clamp_rgb(c, 80, 120)
        bc = clamp_rgb(c, 0, 20)
        
        self.color = (rc,gc,bc,10)

        barwidth = width // self.num_bars
        
        # totally random selection
        if self.randomness == "totally random":
            self.bars[random.randint(0, len(self.bars)-1)] += int(h)
            draw_text(window, f"Bar chart incrementing randomally using gaussians (totally random)", normal_font, (0,0,0), width // 2 - 300, 140)

        # selected by gaussian deviation / distribution
        if self.randomness == "gaussian":
            self.bars[selected_bar] += 100
            draw_text(window, f"Bar chart demonstrating the gaussian deviation / distribution", normal_font, (0,0,0), width // 2 - 300, 140)

        for i, bar in enumerate(self.bars):
            barheight = bar * .1
            bar_rect = pygame.Rect(i * barwidth, 200, barwidth, barheight)
            bar_surface = pygame.Surface(bar_rect.size)

            # new

            bar_surface = pygame.Surface(pygame.Rect(bar_rect).size, pygame.SRCALPHA)
            pygame.draw.rect(bar_surface, self.color, bar_surface.get_rect())
            window.blit(bar_surface, bar_rect)
    def __class__(self):
        return "BarChart object"



class RandomCircle():
    def __init__(self):
        self.x = width // 2
        self.y = height // 2
        self.color = (0,0,0)
        self.standard_deviation = 30
        self.mean = 100
    def draw(self):
        r = get_gaussian() * self.standard_deviation + self.mean
        pygame.draw.circle(window, self.color, (self.x, self.y), r)
        draw_text(window, f"Drawing circle, size: {r}", normal_font, (0,0,0), width // 2 - 200, 30)
    def __class__(self):
        return "RandomCircle object"

class GraphDeviationHorizontally():
    def __init__(self):
        self.x = width // 2
        self.y = height // 2 - 200
        self.color = (0,0,150, 50)
        self.r = 10
        self.standard_deviation = 120
        self.mean = 50
    def draw(self):
        dotpos = get_gaussian() * self.standard_deviation + self.mean
        target_rect = pygame.Rect(self.x + dotpos, self.y, 0, 0).inflate((self.r*2, self.r*2))
        shape_surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surface, self.color, (self.r, self.r), self.r)
        window.blit(shape_surface, target_rect)
        draw_text(window, f"Graphing gaussian deviation using dots (horizontal)", normal_font, (0,0,0), width // 2 - 200, 60)
    def __class__(self):
        return "GraphDeviation object"


showing_circle = False
showing_dotgraph = False
showing_barchart = False

toggle_random = False
toggle_hide = False

def update(surface, group):
    global showing_circle, showing_dotgraph, showing_barchart, toggle_random, toggle_hide


    for obj in group:
        if obj.__class__() == "GraphDeviation object":
            showing_dotgraph = True
        if obj.__class__() == "RandomCircle object":
            window.fill((255,255,255))
            showing_circle = True
        obj.draw()
    if (showing_circle == True) and (showing_dotgraph == True):
        draw_text(window, "Remove circle object to display the dot graph properly (press d key)", small_font, (255,0,0), 10, 10)
    if (showing_circle == False):
        if not showing_barchart:
            draw_text(window, "Press the d key to display a beautiful bar chart", small_font, (0,100,0), 10, 10)
    if showing_barchart and not toggle_random:
        draw_text(window, "Press the g key to toggle bar chart randomness", small_font, (0,100,0), 10, 10)
    if showing_dotgraph and not toggle_hide and not showing_circle:
        draw_text(window, "Press the h key to hide the dot graph", small_font, (0,0,100), 10, 30)
    draw_text(window, "Escape or Q to exit program", small_font, (0,0,0), width - 250, height - 20)
    pygame.display.update()

def main():
    global showing_circle, showing_dotgraph, showing_barchart, toggle_random, toggle_hide
    run = True

    # setup
    shapes = []
    circle = RandomCircle()
    graph = GraphDeviationHorizontally()
    barchart = BarChart()
    shapes.append(circle)
    shapes.append(graph)
    # shapes.append(barchart)
    window.fill((255,255,255))


    # main loop (including input)

    times_pressed = 0

    while run:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE] or key[pygame.K_q]:
                run = False
            if key[pygame.K_d]:
                for i, obj in enumerate(shapes):
                    if obj.__class__() == "RandomCircle object":
                        shapes.remove(shapes[i])
                        showing_circle = False
                        window.fill((255,255,255))
                    if times_pressed == 1:
                        showing_barchart = True
                        window.fill((255,255,255))
                        shapes.append(barchart)
                    times_pressed += 1
            if key[pygame.K_g]:
                for i, obj in enumerate(shapes):
                    if obj.__class__() == "BarChart object":
                        if obj.randomness == "totally random":
                            window.fill((255,255,255))
                            for bar in obj.bars:
                                bar = 0
                            toggle_random = True
                            obj.randomness = "gaussian"
            if key[pygame.K_h]:
                for i, obj in enumerate(shapes):
                    if obj.__class__() == "GraphDeviation object":
                        shapes.remove(shapes[i])
                        window.fill((255,255,255))
                        toggle_hide = True



        update(window, shapes)

    pygame.quit()

main()