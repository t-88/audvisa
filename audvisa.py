import numpy as np
import wave

file_name = "sounds/440_sqr.wav"

file = wave.open(file_name,"rb")
freq =  file.getframerate()
frames = file.getnframes()




import pygame

def plot(ctx,x,y,yoff=200,xdis=1,pointes=False):
    assert len(x) == len(y)

    for i in range(0,len(x),1):
        if(i >= len(x) or (i + 1 >= len(x))):
            break
            
        if not pointes:
            pygame.draw.line(
                            ctx,
                            (255,255,0),
                            (x[i] * xdis,    -y[i]         + yoff),
                            (x[i + 1] * xdis,-y[i + 1] + yoff),
                            )
        else:
            pygame.draw.circle(
                            ctx,
                            (255,255,0),
                            (x[i] * xdis,    -y[i]         + yoff),
                            2,
                            )
        


h = 800
w = 600

CHUNK = 1024 * 4
pygame.mixer.init()
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

    x = np.linspace(0,w,CHUNK)
    y = np.zeros(CHUNK)

    while not done :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        dt = clock.tick(freq//CHUNK) / 1000
        timer += dt


        display.fill((0,0,0))
        pygame.draw.line(display,(255,255,255),(0,400//2),(w,400//2))


        data_buffer_b = file.readframes(int(freq * dt))
        data_buffer = np.frombuffer(data_buffer_b,dtype=np.int16)
        data_buffer = data_buffer[0::2] # left channel
        


        x = np.linspace(0,w,len(data_buffer))
        y = np.interp(data_buffer,[-2**16,2**16],[-100,100])
        plot(display,x,y)

        if(len(data_buffer) > 0):
        
            data_fft = np.abs(np.fft.fft(data_buffer)[:len(data_buffer)//2]) 

            

            x = np.linspace(0,w,len(data_fft))
            y = np.interp(data_fft,[0,max(data_fft)],[0,100])
        
        

            plot(display,x,y,yoff=500)

    



        pygame.display.flip()





game_loop()
file.close()
