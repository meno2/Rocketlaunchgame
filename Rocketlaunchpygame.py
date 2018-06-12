import pygame as pg
import ISA as isa
import rocket_functions as rf
import random
from math import *

pg.init()
black =(0,0,0)
white=(255,255,255)

#Pygame text stuff
pg.font.init()
myfont = pg.font.SysFont('Times New Roman', 15)

startliftoff = myfont.render('Press space bar to lift off!', False, (0, 0, 0))

#Loading the images
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

headingvupd = 0.5*pi
h_earth = 0            #[m]
vel = 0                #[m/s]
rho0 = 1.225           #[kg/m^3]
mass1start = 2923387   #[kg]
mass1burnout = 658801  #[kg]
mass2start = 527306    #[kg]
mass2burnout = 174989  #[kg]
mass3start = 143249    #[kg]
mass3burnout = 52563   #[kg]
payload = 41000        #[kg]

mass0 = mass1start

x = 400

heading = 0.5*pi 
hpos = 0
vpos = 0

stage  = 0
timesincekey = 0

running =  True
while running:
    pg.event.pump()

    t0 = t
    t = pg.time.get_ticks()*0.001
    dt = t- t0
    if dt == 0:
        dt = 0.001
    
    timesincekey = timesincekey + dt

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        heading  = heading + 0.5*dt
        if heading > 0.5*pi:
            heading = 0.5*pi
        

    if keys[pg.K_RIGHT]:
        heading = heading - 0.5*dt

    if keys[pg.K_SPACE] and timesincekey > 0.3:
        stage = stage + 1
        timesincekey = 0
        
    
    #Now the actual functions:
    rho1 = isa.ISA(vpos)
    bluecol = int(rho1/rho0 * 255)
    redcol = int(bluecol/5)
    greencol = int(bluecol/1.4)

    background = (redcol,greencol,bluecol)
    
    scr.fill(background)

    if stage == 0:
        firststagerect.center = (x,400)
        scr.blit(startliftoff,(0,0))
        scr.blit(firststage,firststagerect) 

    if stage == 1:
        thrust = 38257990
        isp = 304
        mass1 = rf.mass_acc(mass0, isp, thrust, dt)
        mass0 = mass1
        
        if mass1 > mass1burnout:
            thrust = 38257990 #N
        if mass1 <= mass1burnout:
            thrust = 0

        #Basic high school physics & mathematics
        hpos,vpos,vel,headingvupd,heading = rf.flight_path(vel, rho1, 5, mass1, thrust, isp, dt, heading, headingvupd, hpos,vpos)

        #Exhaust fumes!
        for fumes5 in range(500):
            fume = abs(random.randint(0,fumes5))
            fume2 = int(random.randint(-fume,fume)/5)
            colorfume = random.randint(0,50)
            pg.draw.circle(scr,(255,200+colorfume,100+colorfume*3),
                           [(400+fume2+random.randint(-22,22))+int(sin(heading-pi/2)*(300+fume)),400+int(cos(heading-0.5*pi)*(300+fume))+int(random.randint(-22,22)*sin(heading-0.5*pi))],
                           random.randint(1,int(fume/10)+5))
            
        #Displaying stuff
        altitudestr = ["Altitude is",str(round(vpos,1))]
        horposstr = ["Distance traveled:",str(round(hpos,1))]
        timestr = ["Time is",str(round(t,3))]
        percentagetillburnout = ["Percentage of stage left:",str(round(((mass1-mass1burnout)/(mass1start-mass1burnout)*100),3))]
        altitude = myfont.render(str(altitudestr), False, white)
        timetxt = myfont.render(str(timestr),False,white)
        horpostxt = myfont.render(str(horposstr),False,white)
        perctxt = myfont.render(str(percentagetillburnout),False,white)
        firststagerect.center = (x,400)
        firststagerot = pg.transform.rotate(firststage, 180/pi*(heading-0.5*pi))
        firststagerotcent = firststagerot.get_rect(center=(400,400))
        scr.blit(firststagerot,firststagerotcent)
        scr.blit(altitude, (0,0))
        scr.blit(horpostxt, (0,20))
        scr.blit(timetxt, (0,40))
        scr.blit(perctxt,(0,60))
        
        
    if stage == 2:
        for fumes5 in range(500):
            fume = abs(random.randint(0,fumes5))
            fume2 = int(random.randint(-fume,fume)/5)
            colorfume = random.randint(0,50)
            pg.draw.circle(scr,(255,200+colorfume,100+colorfume*3),
                           [(400+fume2+random.randint(-22,22))+int(sin(heading-pi/2)*(210+fume)),400+int(cos(heading-0.5*pi)*(210+fume))+int(random.randint(-22,22)*sin(heading-0.5*pi))],
                           random.randint(1,int(fume/10)+5))

        secondstagerect.center = (x,400)
        secondstagerot = pg.transform.rotate(secondstage, 180/pi*(heading-0.5*pi))
        secondstagerotcent = secondstagerot.get_rect(center=(400,400))
        scr.blit(secondstagerot,secondstagerotcent)

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
