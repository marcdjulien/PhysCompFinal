import pygame
from pygame import mixer
import time

BASE_FILENAME = "C:\\Users\\marcd_000\\Downloads\\thtf\\original\\%s.flac"
def getfilename(s):
    return BASE_FILENAME%(s)

pygame.display.set_mode((120, 120), pygame.DOUBLEBUF | pygame.HWSURFACE)

pygame.init()

pygame.mixer.init()
s1 = pygame.mixer.Sound(getfilename("THTF bass verse loop 1"))
s2 = pygame.mixer.Sound(getfilename("THTF drum loop 1"))
s3 = pygame.mixer.Sound(getfilename("THTF synth riff 1"))

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print event
            if event.key == pygame.K_q:
                playing = False
            elif event.key == pygame.K_z:
                s1.play()
            elif event.key == pygame.K_x:
                s2.play()
            elif event.key == pygame.K_c:
                s3.play()
