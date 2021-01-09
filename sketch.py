from p5 import *
import random


class Boid:
    def __init__(self):
        self.position = Vector(random.uniform(0,500) ,random.uniform(0,500))
        self.velocity = Vector(random.uniform(-5,5),random.uniform(-5,5))
        self.acceleration = Vector(0,0)
        self.perception = 50
        self.maxSpeed = 10
        self.maxForce = 1

    #This is one of the three complex functions of the boid
    #In essence what it does is takes all the boids, that is not the current boid, that is located within the current
    #Boids perception range which is a circle of randius r = perception around the boid
    #The velocity of all the boids located in this perception circle is summed together in one vector
    #Then divided by a constant boidcount which is the number of boids within the perception circle
    #This gives us an average velocity
    #The value is returned as the alignment is called within the update function
    #So the change in velocity between the current boid's velocity and the found average velocity
    #Is set to the acceleration
    def align(self,flock):
        average = Vector(0,0)
        boidcount = len(flock)
        for boid in flock:
            average = average + boid.velocity
        if boidcount > 0:
            average = average / boidcount
            average.magnitude = self.maxSpeed
            average = average - self.velocity
            average.limit(self.maxForce)
        return average

    def cohesion(self,flock):
        average = Vector(0,0)
        boidcount = len(flock)
        for boid in flock:
            average = average + boid.position
        if boidcount > 0:
            average = average / boidcount
            average = average - self.position
            average.magnitude = self.maxSpeed
            average = average - self.velocity
            average.limit(self.maxForce)
        return average

    def separation(self, flock):
        average = Vector(0,0)
        boidcount = len(flock)
        difference = Vector(0,0)
        for boid in flock:
            difference = self.position - boid.position
            difference = difference / (distance(self.position, boid.position) ** 2)
            average = average + difference
        if boidcount > 0:
            average = average / (boidcount)
            average.magnitude = self.maxSpeed
            average = average - self.velocity
            average.limit(self.maxForce)
        return average

    def update(self, flock):
        inRange = []
        inRange2 = []
        for boid in flock:
            d = distance(boid.position, self.position)
            if d < self.perception and boid != self:
                inRange.append(boid)
            if d < self.perception *2 and boid != self:
                inRange2.append(boid)

        self.acceleration = self.align(inRange) + self.cohesion(inRange) + self.separation(inRange2)
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit(self.maxSpeed)
        self.acceleration = self.acceleration * 0


    def edges(self):
        if self.position.x < 0:
            self.position.x = 500
        elif self.position.x > 500:
            self.position.x = 0
        if self.position.y > 500:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = 500


    def show(self):
        stroke(0)
        fill(175)
        circle((self.position.x, self.position.y), 9)

#create a flock of boids
flock = []
n = int(input("Enter the amount of boid's you want: "))
for x in range(n):
    flock.append(Boid())


def setup():
    size(500,500)
    background(255)

def draw():
    global flock
    background(255)
    for boid in flock:
        boid.edges()
        boid.update(flock)
        boid.show()

if __name__ == '__main__':
    run(frame_rate=100)