from Constants import *
import threading
import pygame
import time
from pygame import mixer
import random

def closest_angle_tick(angle):
    i = int(angle/ANGLE_UPDATE)
    return i*ANGLE_UPDATE

def closest_radial_tick(radius):
    i = int(radius/RADIAL_QUANT)
    return i*RADIAL_QUANT

def duration2angle(duration):
    return duration*ANGLE_UPDATE/UPDATE_PERIOD

def polar2rect(r,t):
    center_x = VIEWER_SIZE[0]/2
    center_y = VIEWER_SIZE[1]/2
    x = center_x + r*np.cos(t)
    y = center_y + r*np.sin(t)
    return (int(x), int(y))

def rect2polar(x,y):
    center_x = VIEWER_SIZE[0]/2
    center_y = VIEWER_SIZE[1]/2
    r = np.hypot(x-center_x, y-center_y)
    t = np.arctan2(y-center_y, x-center_x)
    return (int(r), t%(2*PI))


def draw_sector(screen, color, r1, r2, start, stop, width):
    if r1 <= 5:
        return

    center_x = VIEWER_SIZE[0]/2
    center_y = VIEWER_SIZE[1]/2
    bounding_rect1 = pygame.Rect(center_x - r1,
                                  center_y - r1,
                                  2*r1,
                                  2*r1)
    bounding_rect2 = pygame.Rect(center_x - r2,
                                  center_y - r2,
                                  2*r2,
                                  2*r2)
    p1 = polar2rect(r1, start)
    p2 = polar2rect(r2, start)
    p3 = polar2rect(r1, stop)
    p4 = polar2rect(r2, stop)

    pygame.draw.arc(screen, color, bounding_rect1, -stop, -start, width)
    pygame.draw.arc(screen, color, bounding_rect2, -stop, -start, width)
    pygame.draw.line(screen, color, p1, p2, width) 
    pygame.draw.line(screen, color, p3, p4, width) 

class SampleObject(object):
    def __init__(self, angle, num, duration, radius):
        super(SampleObject, self).__init__()
        self.angle = angle
        self.num = num
        self.duration = duration
        self.radius = radius

    def __hash__(self):
        return hash((self.angle, self.num, self.duration, self.radius))
    def __eq__(self, other):
        return (self.angle == other.angle 
               and self.num == other.num 
               and self.duration == other.duration
               and self.radius == other.radius)
        

class Viewer(threading.Thread):
    def __init__(self):
        super(Viewer, self).__init__()
        self.draw = True
        self.objects = set() #contains objs -> [angle, id, duration, radius]
        self.votes = dict()
        self.objects_mutex = threading.Lock()
        self.cur_angle = 0
        self.cur_angle_display = 0
        self.update_time = time.time() + UPDATE_PERIOD
        self.draw_time = time.time() + RENDER_PERIOD
        self.done = False
        self.mouse_pos = [0,0]
        self.cur_sample = 0

    def load_sounds(self):
        BASE_FILENAME = "%s.wav"#"C:\\Users\\marcd_000\\Downloads\\thtf\\original\\%s.flac"
        filenames = ["g1", "g2", "g3", "g4"]
        self.sounds = []
        try:
            for i in xrange(len(filenames)):
                self.sounds.append(mixer.Sound(BASE_FILENAME%(filenames[i])))
        except Exception, e:
            print "Failure loading"
            print e
            exit()

    def run(self):
        print "Starting Media"
        pygame.init()
        mixer.init()
        self.load_sounds()
        self.screen = pygame.display.set_mode(VIEWER_SIZE, pygame.NOFRAME | pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.clock = pygame.time.Clock()

        while not self.done:
            self.update(time.time())
            self.render(time.time())
            self.clock.tick(VIEWER_FPS)

        pygame.quit()

    def update(self, time):
        if time >= self.update_time:
            self.update_time += UPDATE_PERIOD            
        else:
            return

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.quit()
                elif event.key == pygame.K_f:
                    self.cur_sample = (self.cur_sample + 1)%4
                elif event.key == pygame.K_r:
                    self.cur_angle = PI/2
                elif event.key == pygame.K_c:
                    self.objects = set()

        # Update our board ??
        self.play_inview()
            
        self.cur_angle = (self.cur_angle + ANGLE_UPDATE) % (2*PI)
        self.cur_angle_display = self.cur_angle

    def render(self, time):
        if time >= self.draw_time:
            self.draw_time += RENDER_PERIOD            
        else:
            return

        # Draw Graphics
        self.draw_screen()
        pygame.display.flip()
        self.cur_angle_display += ANGLE_UPDATE/(UPDATE_PERIOD/RENDER_PERIOD)

    def quit(self):
        self.draw = False
        pygame.quit()
        exit()

    # Sound stuff
    """
    Returns a copy of the objects as a, iterable list
    """
    def get_objects(self):
        objects = []
        self.objects_mutex.acquire()
        for obj in self.objects:
            if self.votes[obj] >= REQ_VOTES:
                objects.append(obj)
        self.objects_mutex.release()
        return objects

    def add_objects(self, new_objects):
        new_objects_set = set(new_objects)
        self.objects_mutex.acquire()
        missing = self.objects.difference(new_objects)

        # Decrement those no longer in same spot
        for obj in missing:
            self.votes[obj]-=1
        
        for newobj in new_objects:
            self.votes[newobj] = 1000000000#10*REQ_VOTES
            if newobj not in self.objects:
                self.objects.add(newobj)

        self.objects_mutex.release()

    def clear_objects(self):
        self.objects_mutex.acquire()
        self.objects.clear()
        self.objects_mutex.release()

    def shape2board(self, shapes):
        #self.clear_objects()
        objects = []
        for shape in shapes:
            style = shape[0]
            color = shape[1]
            m = np.mean(shape[2], 0)
            polar = rect2polar(m[0]*VIEWER_SIZE[0], m[1]*VIEWER_SIZE[1])
            num = SHAPE_TO_ID[style][color]
            duration = 1.0
            duration = duration*self.sounds[self.cur_sample].get_length()
            obj = SampleObject(closest_angle_tick(polar[1]), 
                               num, 
                               duration, 
                               closest_radial_tick(polar[0]))
            objects.append(obj)
        self.add_objects(objects)

    def play_inview(self):
        min_angle = self.cur_angle
        max_angle = self.cur_angle + ANGLE_UPDATE
        objects = self.get_objects()
        for obj in objects:
            if min_angle <= obj.angle and obj.angle <= max_angle:
                self.sounds[obj.num].play(maxtime=int(1000*obj.duration))

    # I/O Stuff
    def handle_mouse(self, pos):
        polar = rect2polar(pos[0], pos[1]) 
        duration = 1.0 #polar[0]/(VIEWER_SIZE[0]/2.0)
        duration = duration*self.sounds[self.cur_sample].get_length()
        obj = SampleObject(closest_angle_tick(polar[1]), 
                           self.cur_sample, 
                           duration, 
                           closest_radial_tick(polar[0]))
        self.add_objects( [obj] )


    # Drawing Stuff
    def draw_screen(self):
        # Clear Screen
        self.screen.fill(BLACK_RGB)
        objects = self.get_objects()
        line_width = 1
        size = 3
        for obj in objects:
            xy = polar2rect(obj.radius, obj.angle)
            rect = [xy[0]-size, xy[1]-size, 2*size, 2*size]
            color = COLORS[obj.num]
            pygame.draw.rect(self.screen, color, rect, line_width)
            start_angle = obj.angle
            stop_angle = start_angle + duration2angle(obj.duration)
            diff_angle = random.randint(0,1000)/1000.0
            color = tuple( (np.array(color)*diff_angle).astype(int) )
            radius = obj.radius
            draw_sector(self.screen, color, radius, radius, start_angle, stop_angle, line_width)


        # Draw inner circle
        pygame.draw.circle(self.screen, WHITE_RGB, [VIEWER_SIZE[0]/2, VIEWER_SIZE[1]/2], 10, 3)

        # Draw current spot
        line_width = 1
        radius1 = 10
        radius2 = VIEWER_SIZE[1]/2
        #start_angle = self.cur_angle - ANGLE_UPDATE/2
        #stop_angle = self.cur_angle + ANGLE_UPDATE/2
        #draw_sector(self.screen, BLACK_RGB, radius1, radius2, start_angle, stop_angle, line_width)
        start_angle = self.cur_angle_display 
        stop_angle = self.cur_angle_display
        draw_sector(self.screen, WHITE_RGB, radius1, radius2, start_angle, stop_angle, line_width)

        # Draw Mouse
        color = COLORS[self.cur_sample]
        rect = [self.mouse_pos[0]-5, self.mouse_pos[1]-5, 10, 10]
        pygame.draw.rect(self.screen, color, rect, line_width) 

        # Draw Mouse
        polar_mouse = rect2polar(self.mouse_pos[0], self.mouse_pos[1])
        radius1 = 10
        radius2 = closest_radial_tick(VIEWER_SIZE[1]/2)
        start_angle = closest_angle_tick(polar_mouse[1])
        stop_angle = start_angle
        line_width = 1
        draw_sector(self.screen, WHITE_RGB, radius1, radius2, start_angle, stop_angle, line_width)
