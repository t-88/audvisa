import numpy as np
import wave

file_name = "sounds/Tetris.wav"

file = wave.open(file_name,"rb")
freq =  file.getframerate()
frames = file.getnframes()

data_buffer_b = file.readframes(frames)
data_buffer = np.frombuffer(data_buffer_b,dtype=np.int16)
data_buffer = data_buffer[0::2] # left channel
file.close()



import pygame


def plot(ctx,x,y):
    assert len(x) == len(y)

    for i in range(0,len(x),2):
        pygame.draw.line(
                        ctx,
                        (255,255,0),
                        (x[i],y[i]         + h // 2),
                        (x[i + 1],y[i + 1] + h // 2),
                        )


h = 400
w = 600
pygame.mixer.init()
pygame.init()

pygame.mixer.music.load(file_name)
pygame.mixer.music.play()


display = pygame.display.set_mode((w,h))
clock  = pygame.time.Clock()
x = np.linspace(0,w,freq)

timer = 0
curr_sec = 0
freqs = 0
y = np.interp(data_buffer[freq*(curr_sec):freq*(curr_sec+1)],[-2**16,2**16],[-100,100])


done = False
while not done:
    dt = clock.tick(60) / 1000
    timer += dt
    freqs = min(freqs + freq * dt,freq) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    display.fill((0,0,0))
    pygame.draw.line(display,(255,255,255),(0,h//2),(w,h//2))

    if timer >= 1:
        print(freqs,freq)
        timer = 0
        freqs = 0
        curr_sec += 1
        y = np.interp(data_buffer[freq*(curr_sec):freq*(curr_sec+1)],[-2**16,2**16],[-100,100])

    plot(display,x,y)


    carrot_x = np.interp(freqs,[0,freq],[0,w])
    pygame.draw.line(display,(255,0,0),(carrot_x,0),(carrot_x,h))

    pygame.display.flip()