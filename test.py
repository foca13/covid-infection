#!/usr/bin/python

###Alternate header Rod #!/usr/bin/python
###!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import numpy.random as random
import math
import turtle
from turtle import Turtle
from itertools import combinations
"""
Created on Fri Mar 13 14:13:42 2020

@author: guillemguigoicorominas
"""
class Human(Turtle):
    def __init__(self, infection_ratio, killing_ratio, healing_ratio, infected = False):
        super(Human, self).__init__()
        self.infected = infected
        self.infection_ratio = infection_ratio
        self.killing_ratio = killing_ratio
        self.healing_ratio = healing_ratio
        self.penup()
        self.goto(random.randint(-290, 290), random.randint(-290, 290))
        self.dx = random.randint(-1,2) * 0.1
        self.dy = random.randint(-1,2) * 0.1
        self.shape('circle')
        self.setcolor()
        self.speed(0)
        self.healed = False
        self.recent_interactions = []

    def accelerate(self):
        self.dy += random.randint(-1,2) * 0.1
        self.dx += random.randint(-1,2) * 0.1
        
    def check_max_speed(self):
        if self.dx < - 5:
            self.dx = -4
        if self.dx > 5:
            self.dx = 4
        if self.dy < -5:
            self.dy = -4
        if self.dy > 5:
            self.dy = 4
    
    def move(self):
        self.sety(self.ycor() + self.dy)
        self.setx(self.xcor() + self.dx)
        self.accelerate()
        self.check_max_speed()
        self.check_edge()
        self.check_healing()
    
    def check_edge(self):
        if self.ycor() < -300 or self.ycor() > 300:
            self.dy *= -1
        if self.xcor() < -300 or self.xcor() > 300:
            self.dx *= -1
    
    def check_healing(self):
        if self.infected and random.rand() < self.healing_ratio * 0.001:
            self.heal()
    
    def heal(self):
        self.infected = False
        self.healed = True
        self.color('purple')
    
    def check_kill(self):
        if self.infected and random.rand() < self.killing_ratio * 0.001:
            self.clear()
            self.ht()
            return True
            
    def setcolor(self):
        self.color('green')
        if self.infected:
            self.color('red')
    
    def infect(self):
        if self.healed == False and random.rand() < self.infection_ratio:
            self.infected = True
            self.color('red')

def ball_collision(ball_1, ball_2):

    v1 = np.array([ball_1.dx, ball_1.dy])
    p1 = np.array([ball_1.xcor(), ball_1.ycor()])
    v2 = np.array([ball_2.dx, ball_2.dy])
    p2 = np.array([ball_2.xcor(), ball_2.ycor()])
    
    ball_1.dx = v1[0] - np.inner(v1 - v2, p1 - p2)/np.inner(p1 - p2, p1 - p2) * (p1[0] - p2[0])
    ball_1.dy = v1[1] - np.inner(v1 - v2, p1 - p2)/np.inner(p1 - p2, p1 - p2) * (p1[1] - p2[1])
    ball_2.dx = v2[0] - np.inner(v2 - v1, p2 - p1)/np.inner(p1 - p2, p1 - p2) * (p2[0] - p1[0])
    ball_2.dy = v2[1] - np.inner(v2 - v1, p2 - p1)/np.inner(p1 - p2, p1 - p2) * (p2[1] - p1[1])

    distance = math.sqrt(abs(ball_1.xcor() - ball_2.xcor())**2+abs(ball_1.ycor() - ball_2.ycor())**2)

    #collision distance correction
    ball_1.setx(p1[0] + (p1[0] - p2[0])*(20-distance)/distance/2)
    ball_1.sety(p1[1] + (p1[1] - p2[1])*(20-distance)/distance/2)
    ball_2.setx(p2[0] + (p2[0] - p1[0])*(20-distance)/distance/2)
    ball_2.sety(p2[1] + (p2[1] - p1[1])*(20-distance)/distance/2)

window = turtle.Screen()
window.tracer(0)

balls = [Human(0.5,0.5,0.5) for i in range(30)]

balls.append(Human(0.5,0.01,0.1,True))

#check initial collisions
for ball_1, ball_2 in combinations(balls, 2):

    x1, y1 = ball_1.xcor(), ball_1.ycor()
    x2, y2 = ball_2.xcor(), ball_2.ycor()

    distance = math.sqrt((x1 - x2)**2+(y1 - y2)**2)

    if distance < 20:
        ball_1.setx(x1 + (x1 - x2)*(20-distance)/distance/2)
        ball_1.sety(y1 + (y1 - y2)*(20-distance)/distance/2)
        ball_2.setx(x2 + (x2 - x1)*(20-distance)/distance/2)
        ball_2.sety(y2 + (y2 - y1)*(20-distance)/distance/2)
                
while True:
    window.update()
    for ball in balls:
        ball.move()
        if ball.check_kill():
            balls.remove(ball)
            
    for ball_1, ball_2 in combinations(balls, 2):
        distance = math.sqrt(abs(ball_1.xcor() - ball_2.xcor())**2+abs(ball_1.ycor() - ball_2.ycor())**2)
        if distance < 20:
            if ball_1.infected:
                ball_2.infect()
            if ball_2.infected:
                ball_1.infect()
            ball_collision(ball_1,ball_2)

turtle.exitonclick()

