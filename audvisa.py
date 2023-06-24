import numpy as np
import wave

file_name = "sounds/are-you-sure-about-that.wav"

file = wave.open(file_name,"rb")
freq =  file.getframerate()
frames = file.getnframes()

data_buffer_b = file.readframes(frames)
data_buffer = np.frombuffer(data_buffer_b,dtype=np.int16)
data_buffer = data_buffer[0::2] # left channel
file.close()



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
        # pygame.draw.circle(
        #                 ctx,
        #                 (255,255,0),
        #                 (x[i] * xdis,    -y[i]         + yoff // 2),
        #                 2,
        #                 )
        


h = 800
w = 600

CHUNK = 1024 * 4
pygame.mixer.init(frequency=freq,buffer=CHUNK)
pygame.init()








def game_loop():
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()

    display = pygame.display.set_mode((w,h))
    clock  = pygame.time.Clock()

    done = False
    timer = 0
    curr_sec = 0
    freqs = 0

    data = data_buffer[freq*(curr_sec):freq*(curr_sec+1)]
    x = np.linspace(0,w,freq)
    y = np.interp(data,[-2**16,2**16],[-100,100])

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

        if timer >= 1:
            timer = 0
            freqs = 0
            curr_sec += 1
            data = data_buffer[freq*(curr_sec):freq*(curr_sec+1)]
            y = np.interp(data,[-2**16,2**16],[-100,100])

        plot(display,x,y)
        carrot_x = int(np.interp(freqs,[0,freq],[0,w]))
        pygame.draw.line(display,(255,0,0),(carrot_x,0),(carrot_x,400))



        #data_fft = np.abs(np.fft.fft(data[carrot_x])[:len(data[carrot_x])//2]) / freq
        data_fft = np.abs(np.fft.fft(data[int(freqs):int(freqs) + CHUNK]))[:CHUNK//2] / freq

        x_fft =  np.linspace(0,w,len(data_fft))
        y_fft = data_fft #np.interp(data_fft,[0,100],[0,100])
        plot(display,x_fft,y_fft,yoff=1200,xdis=2)



        pygame.display.flip()





game_loop()
