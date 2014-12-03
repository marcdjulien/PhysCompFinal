from Constants import *
import threading
import pygame
import time
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

class Viewer(threading.Thread):
    def __init__(self, synth):
        super(Viewer, self).__init__()
        self.synth = synth
        self.draw = True


    def run(self):
        print "Starting Viewer"
        pygame.init()
        self.screen = pygame.display.set_mode(VIEWER_SIZE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        while self.draw:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                       #self.handle_mouse(event.pos)
                        pass
                elif event.type == pygame.KEYDOWN:
                    if event.key == 113:
                        self.quit()
            # Update our board
            self.board = self.synth.get_board()
            self.cur_step = self.synth.cur_step
    
            # Draw Graphics
            self.draw_board()

            pygame.display.flip()
            self.clock.tick(VIEWER_FPS)


        pygame.quit()

    def quit(self):
        self.draw = False
        pygame.quit()
        self.synth.quit()
        exit()

    def handle_mouse(self, pos):
        Ri = ROW_WIDTH
        Ai = 2*PI/NOTES

        polar = rect2polar(pos[0], pos[1]) 
        if polar[0] < MIN_BOX:
            return

        row = int((polar[0] - (MIN_BOX))/Ri)
        col = int(polar[1]/Ai)
        print "%d,%d"%(row,col)
        
        if row < STEPS and col < NOTES:
            board = self.synth.get_board()
            board[row][col] = (board[row][col] + 1 ) % 4
            self.synth.set_board(board)


    def draw_board(self):
        # Clear Screen
        self.screen.fill(WHITE_RGB)
        
        board_width = 3

        arc_length = 360.0/NOTES
        center_x = VIEWER_SIZE[0]/2
        center_y = VIEWER_SIZE[1]/2
        width = 5
        for i in xrange(len(self.board)):
            radius1 = MIN_BOX + i*ROW_WIDTH
            radius2 = MIN_BOX + (i+1)*ROW_WIDTH

            for j in xrange(NOTES):
                start_angle = j*2*PI/NOTES
                stop_angle = (j+1)*2*PI/NOTES
                color = (200,200,200)
                draw_sector(self.screen, color, radius1, radius2, start_angle, stop_angle, board_width)
        
        for i in xrange(len(self.board)):
            line = self.board[i]

            radius1 = MIN_BOX + i*ROW_WIDTH
            radius2 = MIN_BOX + (i+1)*ROW_WIDTH

            for j in xrange(NOTES):
                start_angle = j*2*PI/NOTES
                stop_angle = (j+1)*2*PI/NOTES
                style = self.board[i][j]
                if style == CIRCLE:
                    color = RED_RGB
                elif style == SQUARE:
                    color = YELLOW_RGB
                elif style == STAR:
                    color = GREEN_RGB
                elif style == TRIANGLE:
                    color = BLUE_RGB
                else:
                    continue
                draw_sector(self.screen, color, radius1, radius2, start_angle, stop_angle, board_width)


        # Draw current spot
        radius1 = MIN_BOX + self.cur_step*ROW_WIDTH
        radius2 = MIN_BOX + (self.cur_step+1)*ROW_WIDTH
        width = 7
        draw_sector(self.screen, ORANGE_RGB, radius1, radius2, 0, 2*PI, width)


