from Constants import *
import threading
import pygame
import time

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
                    self.synth.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                       #self.handle_mouse(event.pos)
                        pass
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

    def handle_mouse(self, pos):
        row = (pos[0]-BOARD_X)/UNIT_W
        col = (pos[1]-BOARD_Y)/UNIT_H
        if row < STEPS and col < NOTES:
            board = self.synth.get_board()
            board[row][col] = (board[row][col] + 1 ) % 3
            self.synth.set_board(board)

    def draw_board(self):
        # Clear Screen
        self.screen.fill(WHITE_RGB)

        for i in xrange(len(self.board)):
            line = self.board[i]
            x = BOARD_X + i*UNIT_W

            for j in xrange(len(line)):
                y = BOARD_Y + j*UNIT_H

                # draw specific shape
                style = line[j]
                if style == SQUARE:
                    pygame.draw.rect(self.screen, GREEN_RGB, [x, y, UNIT_W, UNIT_H])
                elif style == CIRCLE:
                    pygame.draw.ellipse(self.screen, GREEN_RGB, [x, y, UNIT_W, UNIT_H])

                # draw spot grid                
                pygame.draw.rect(self.screen, BLACK_RGB, [x, y, UNIT_W, UNIT_H], 3)

        surf = pygame.Surface((UNIT_W, UNIT_H*NOTES), pygame.SRCALPHA)
        surf.fill((0,0,0,100))
        self.screen.blit(surf,(BOARD_X + UNIT_W*self.cur_step, BOARD_Y))


