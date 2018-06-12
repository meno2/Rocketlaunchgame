import pygame as pg
import ISA as isa
import random
pg.init()
black =(0,0,0)
white=(255,255,255)

firststage = pg.image.load("fullstagerocket.gif")
secondstage = pg.image.load("2ndstagerocket.gif")
thirdstage = pg.image.load("Thirdstagerocket.gif")
laststage = pg.image.load("Laststagerocket.gif")
firststagerect = firststage.get_rect()
secondstagerect = secondstage.get_rect()
thirdstagerect = thirdstage.get_rect()
laststagerect = laststage.get_rect()

xmax = 800
ymax = 800
scr = pg.display.set_mode((xmax,ymax))

t = pg.time.get_ticks()*0.001


h_earth = 0         #[m]
v1 = 0              #[m/s]
rho0 = 1.225        #[kg/m^3]
mass0 = 2923387     #[kg]

x = 400

stage  = 1


timesincekey = 0

running =  True
while running:
    pg.event.pump()

    t0 = t
    t = pg.time.get_ticks()*0.001
    dt = t- t0
    timesincekey = timesincekey + dt

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        pass

    if keys[pg.K_RIGHT]:
        pass
    
    if keys[pg.K_SPACE] and timesincekey > 0.3:
        stage = stage + 1
        timesincekey = 0
        

    h_earth = h_earth + v1*dt
    
    #Now the actual functions:
    rho1 = isa.ISA(h_earth)
    bluecol = int(rho1/rho0 * 255)
    redcol = int(bluecol/5)
    greencol = int(bluecol/1.4)

    

    background = (redcol,greencol,bluecol)
    
    scr.fill(background)
    
    if stage == 1:
        firststagerect.center = (x,400)
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        pg.draw.circle(scr,white,[int(xmax/2),750+random.randint(-50,50)],random.randint(5,30))
        scr.blit(firststage,firststagerect)

    if stage == 2:
        secondstagerect.center = (x,400)
        for fumes in range(5):
             pg.draw.circle(scr,white,[int(xmax/2),550+random.randint(0,50)],random.randint(1,5))

        for fumes2 in range(30):
            pg.draw.circle(scr,white,[int(xmax/2)+random.randint(-25,25),650+random.randint(-30,50)],random.randint(5,15))

        for fumes3 in range(30):
            pg.draw.circle(scr,white,[int(xmax/2)+random.randint(-50,50),750+random.randint(-50,50)],random.randint(15,30))
        
        scr.blit(secondstage,secondstagerect)

    if stage == 3:
        thirdstagerect.center = (x,400)
        scr.blit(thirdstage,thirdstagerect)

    if stage > 3:
        laststagerect.center = (x,400)
        scr.blit(laststage,laststagerect)
    
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
