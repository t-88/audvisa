import numpy as np
import pyaudio


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
freq = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=freq,
                input=True,
                frames_per_buffer=CHUNK)



import pygame
def plot(ctx,x,y,yoff=400,xdis=1):
    assert len(x) == len(y)

    for i in range(0,len(x),1):
        if(i >= len(x) or (i + 1 >= len(x))):
            break
        pygame.draw.line(
                        ctx,
                        (255,255,0),
                        (x[i] * xdis,    -y[i]         + yoff // 2),
                        (x[i + 1] * xdis,-y[i + 1] + yoff // 2),
                        )


h = 800
w = 600

pygame.init()








def game_loop():


    display = pygame.display.set_mode((w,h))
    clock  = pygame.time.Clock()

    done = False
    timer = 0
    curr_sec = 0
    freqs = 0


    x = np.linspace(0,w,CHUNK)

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
        pygame.draw.line(display,(255,255,255),(0,400//2),(w,400//2))
        
        data = stream.read(CHUNK)
        data = np.frombuffer(data,dtype=np.int16)
        data = data[::2]
        print(len(data),len(x))

        y = np.interp(data,[-2**16,2**16],[-100,100])

        plot(display,x,y,xdis=5)


        data_fft = np.abs(np.fft.fft(data)[:len(data)//2]) / freq

        x_fft =  np.linspace(0,w,len(data_fft))
        y_fft = data_fft #np.interp(data_fft,[0,100],[0,100])
        plot(display,x_fft,y_fft,yoff=1200,xdis=5)



        pygame.display.flip()





game_loop()
