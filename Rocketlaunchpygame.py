import pygame as pg
import ISA as isa
import rocket_functions as rf
import random
from math import *

#Created by Guy Maré and Menno Berger


pg.init()
black =(0,0,0)
white=(255,255,255)

#Pygame text stuff
pg.font.init()
myfont = pg.font.SysFont('Times New Roman', 15)
headerfont = pg.font.SysFont('Times New Roman', 30)
largerheaderfont = pg.font.SysFont('Times New Roman', 40)
startliftoff = myfont.render('Press space bar to lift off!', False, (0, 0, 0))

#Loading the images
launchpad = pg.image.load("Launchpad.gif")
firststage = pg.image.load("fullstagerocket.gif")
secondstage = pg.image.load("2ndstagerocket.gif")
thirdstage = pg.image.load("Thirdstagerocket.gif")
laststage = pg.image.load("Laststagerocket.gif")
launchpadrect = launchpad.get_rect()
firststagerect = firststage.get_rect()
secondstagerect = secondstage.get_rect()
thirdstagerect = thirdstage.get_rect()
laststagerect = laststage.get_rect()

xmax = 800
ymax = 800
scr = pg.display.set_mode((xmax,ymax))

t = pg.time.get_ticks()*0.001
time2 = pg.time.get_ticks()*0.001





#Constants
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
mass2 = mass2start
mass4 = mass3start
x = 400

#Setting up time and stuff
highscores = [0,0,0,0,0]
headingvupd = 0.5*pi
heading = 0.5*pi 
hpos = 0
vpos = 55
timespd = 1
stage  = 0
timesincekey = 0
timesincekey2 = 0
time0 = 0
game = False
running =  True


while running:
    pg.event.pump()
    
    #Now the actual functions:
    rho1 = isa.ISA(vpos)
    if rho1 > 1.225:
        rho1 = 1.225
    
    bluecol = int(rho1/rho0 * 255)
    redcol = int(bluecol/5)
    greencol = int(bluecol/1.4)


    
    keys = pg.key.get_pressed()

    if game == True:
        background = (redcol,greencol,bluecol)
        
        scr.fill(background)

        time0 = pg.time.get_ticks()*0.001
        
        #Speeding up time:
        if keys[pg.K_1]:
            timespd = 1
        if keys[pg.K_2]:
            timespd = 2
        if keys[pg.K_3]:
            timespd = 3
        if keys[pg.K_4]:
            timespd = 4
        if keys[pg.K_5]:
            timespd = 5
        if keys[pg.K_6]:
            timespd = 6
        if keys[pg.K_7]:
            timespd = 7
        if keys[pg.K_8]:
            timespd = 8
    
        if vpos > 0:
            t0 = t
            t = pg.time.get_ticks()*0.001
            dt = timespd*(t- t0)
            if dt == 0:
                dt = 0.001
            
            timesincekey = timesincekey + dt/timespd

            #Key controls:
            if keys[pg.K_LEFT]:
                heading  = heading + 0.5*dt
                if heading > 0.5*pi:
                    heading = 0.5*pi

            if keys[pg.K_RIGHT]:
                heading = heading - 0.5*dt

            if keys[pg.K_SPACE] and timesincekey > 0.3:
                stage = stage + 1
                timesincekey = 0


            #Launch phase
            if stage == 0:
                firststagerect.center = (x,400)
                scr.blit(startliftoff,(0,0))
                scr.blit(firststage,firststagerect) 
                scr.blit(launchpad, (180,50))
                ground = pg.Rect(0,410+int(vpos*729/110),900,1000) 
                pg.draw.rect(scr,(94, 237, 0),ground)
                
            #Full rocket
            if stage == 1:
                thrust = 38257990
                isp = 280
                mass1 = rf.mass_acc(mass0, isp, thrust, dt)
                mass0 = mass1
                
                if mass1 > mass1burnout:
                    thrust = 38257990 #N
                if mass1 <= mass1burnout:
                    thrust = 0

                #Basic high school physics & mathematics
                hpos,vpos,vel,headingvupd,heading = rf.flight_path(vel, rho1, 5, mass1, thrust, isp, dt, heading, headingvupd, hpos,vpos)

                #Exhaust fumes!
                if thrust > 0:
                    for fumes5 in range(500):
                        fume = abs(random.randint(0,fumes5))
                        fume2 = int(random.randint(-fume,fume)/5)
                        colorfume = random.randint(0,50)
                        pg.draw.circle(scr,(255,200+colorfume,100+colorfume*3),
                                   [(400+fume2+random.randint(-22,22))+int(sin(heading-pi/2)*(300+fume)),400+int(cos(heading-0.5*pi)*(300+fume))+int(random.randint(-22,22)*sin(heading-0.5*pi))],
                                   random.randint(1,int(fume/10)+5))

                  #Rotating the rocket
                firststagerect.center = (x,400)
                firststagerot = pg.transform.rotate(firststage, 180/pi*(heading-0.5*pi))
                firststagerotcent = firststagerot.get_rect(center=(400,400))
                scr.blit(firststagerot,firststagerotcent)


                #Percentage till burnout display
                percentagetillburnout = ["Percentage of stage left:",str(round(((mass1-mass1burnout)/(mass1start-mass1burnout)*100),3))]

                if (mass1-mass1burnout)/(mass1start-mass1burnout) > 0:
                    perctxt = myfont.render(str(percentagetillburnout),False,white)

                if (mass1-mass1burnout)/(mass1start-mass1burnout) <= 0:
                    perctxt = myfont.render(str(0),False,white)
                scr.blit(perctxt,(0,40))
                #-------


            #Stage 2
            if stage == 2:
                thrust = 4446648
                isp = 420
                mass1 = rf.mass_acc(mass2, isp, thrust, dt)
                mass2 = mass1
                
                if mass1 > mass2burnout:
                    thrust = 4446648 #N
                if mass1 <= mass2burnout:
                    thrust = 0

                #Basic high school physics & mathematics
                hpos,vpos,vel,headingvupd,heading = rf.flight_path(vel, rho1, 5, mass1, thrust, isp, dt, heading, headingvupd, hpos,vpos)
                #Exhaust fumes!
                if thrust > 0:
                    for fumes5 in range(500):
                        fume = abs(random.randint(0,fumes5))
                        fume2 = int(random.randint(-fume,fume)/5)
                        colorfume = random.randint(0,50)
                        pg.draw.circle(scr,(255,200+colorfume,100+colorfume*3),
                                   [(400+fume2+random.randint(-22,22))+int(sin(heading-pi/2)*(210+fume)),400+int(cos(heading-0.5*pi)*(210+fume))+int(random.randint(-22,22)*sin(heading-0.5*pi))],
                                   random.randint(1,int(fume/10)+5))
                #Rotating the rocket
                secondstagerect.center = (x,400)
                secondstagerot = pg.transform.rotate(secondstage, 180/pi*(heading-0.5*pi))
                secondstagerotcent = secondstagerot.get_rect(center=(400,400))
                scr.blit(secondstagerot,secondstagerotcent)


                #Percentage till burnout display
                percentagetillburnout = ["Percentage of stage left:",str(round(((mass1-mass2burnout)/(mass2start-mass2burnout)*100),3))]

                if (mass1-mass2burnout)/(mass2start-mass2burnout) > 0:
                    perctxt = myfont.render(str(percentagetillburnout),False,white)

                if (mass1-mass2burnout)/(mass2start-mass2burnout) <= 0:
                    perctxt = myfont.render(str(0),False,white)
                scr.blit(perctxt,(0,40))
                #-------

            #Stage 3
            if stage == 3:
                thrust = 889325
                isp = 420
                mass1 = rf.mass_acc(mass4, isp, thrust, dt)
                mass4 = mass1
                
                if mass1 > mass3burnout:
                    thrust = 889325 #N
                if mass1 <= mass3burnout:
                    thrust = 0

                #Basic high school physics & mathematics
                hpos,vpos,vel,headingvupd,heading = rf.flight_path(vel, rho1, 5, mass1, thrust, isp, dt, heading, headingvupd, hpos,vpos)

                #Exhaust fumes
                if thrust > 0:
                    for fumes5 in range(500):
                        fume = abs(random.randint(0,fumes5))
                        fume2 = int(random.randint(-fume,fume)/5)
                        colorfume = random.randint(0,50)
                        pg.draw.circle(scr,(255,200+colorfume,100+colorfume*3),
                                   [(400+fume2)+int(sin(heading-pi/2)*(130+fume)),400+int(cos(heading-0.5*pi)*(130+fume))],
                                   random.randint(1,int(fume/10)+5))

                thirdstagerect.center = (x,400)
                thirdstagerot = pg.transform.rotate(thirdstage, 180/pi*(heading-0.5*pi))
                thirdstagerotcent = thirdstagerot.get_rect(center=(400,400))
                scr.blit(thirdstagerot,thirdstagerotcent)

                #Percentage till burnout display
                percentagetillburnout = ["Percentage of stage left:",str(round(((mass1-mass3burnout)/(mass3start-mass3burnout)*100),3))]

                if (mass1-mass3burnout)/(mass3start-mass3burnout) > 0:
                    perctxt = myfont.render(str(percentagetillburnout),False,white)

                if (mass1-mass3burnout)/(mass3start-mass3burnout) <= 0:
                    perctxt = myfont.render(str(0),False,white)
                scr.blit(perctxt,(0,40))
                #-------

            #Last stage
            if stage > 3:
                hpos,vpos,vel,headingvupd,heading = rf.flight_path(vel, rho1, 5, payload, 0, 1, dt, heading, headingvupd, hpos,vpos)
                laststagerect.center = (x,400)
                laststagerot = pg.transform.rotate(laststage, 180/pi*(heading-0.5*pi))
                laststagerotcent = laststagerot.get_rect(center=(400,400))
                scr.blit(laststagerot,laststagerotcent)
                  
            #On Screen displays
            if stage > 0:
                altitudestr = ["Altitude is",str(round(vpos,1))]
                horposstr = ["Distance traveled:",str(round(hpos,1))]
                timestr = ["Time is",str(round(t,3))]
                altitude = myfont.render(str(altitudestr), False, white)
                timetxt = myfont.render(str(timestr),False,white)
                horpostxt = myfont.render(str(horposstr),False,white)
                scr.blit(myfont.render("Time progression:",False,white),(680,20))
                scr.blit(headerfont.render(str(timespd),False,white),(730,35))
                scr.blit(headerfont.render("x",False,white),(750,35))
                scr.blit(altitude, (0,0))
                scr.blit(horpostxt, (0,20))
                #scr.blit(timetxt, (0,40))
                scr.blit(launchpad, (180-int(hpos*729/110),-314+int(vpos*729/110)))
                #ground display
                ground = pg.Rect(0,410+int(vpos*729/110),900,500) 
                pg.draw.rect(scr,(94, 237, 0),ground)


        #Game over (rocket hits the earth)
        if vpos <= 0:
                vpos = 0
                altitudestr = ["Altitude is",str(round(vpos,1))]
                horposstr = ["Distance traveled:",str(round(hpos,1))]
                timestr = ["Time is",str(round(t,3))]
                altitude = myfont.render(str(altitudestr), False, white)
                timetxt = myfont.render(str(timestr),False,white)
                horpostxt = myfont.render(str(horposstr),False,white)
                gameovertxt = headerfont.render(str("GAME OVER! Your traveled distance was:"),False, white)
                yourdisttxt = headerfont.render(str(round(hpos,1)),False,white)
                spacebartxt = headerfont.render("Press spacebar to go back to menu",False,white)
                scr.blit(altitude, (0,0))
                scr.blit(horpostxt, (0,20))
                #scr.blit(timetxt, (0,40))
                scr.blit(launchpad, (180-int(hpos*729/110),-314+int(vpos*729/110)))

                #ground & spacecraft display
                ground = pg.Rect(0,410+int(vpos*729/110),900,1000) 
                pg.draw.rect(scr,(94, 237, 0),ground)
                laststagerect.center = (x,400)
                laststagerot = pg.transform.rotate(laststage, 180/pi*(heading-0.5*pi))
                laststagerotcent = laststagerot.get_rect(center=(400,400))
                scr.blit(laststagerot,laststagerotcent)

                scr.blit(gameovertxt, (130,300))
                scr.blit(yourdisttxt,(350,330))
                scr.blit(spacebartxt,(190,360))

                if keys[pg.K_SPACE]:
                    if hpos > min(highscores):
                        lstminimum = highscores.index(min(highscores))
                        highscores[lstminimum] = hpos
                    game = False
    #The menu
    if game == False:
        timesincekey2 = 0
        time2 = pg.time.get_ticks()*0.001
        dt2 = time2 - time0
        timesincekey2 = timesincekey2 + dt2
        scr.fill(black)

        
        scr.blit((largerheaderfont.render("Launching the Apollo 11 rocket from ",False,white)),(110,50))
        scr.blit((largerheaderfont.render("scientificcaly accurate flat earth ",False,white)),(140,90))

        scr.blit((headerfont.render("The 'real' Apollo 11 mission's distance covered: [m]",False,white)),(100,280))
        scr.blit((headerfont.render("1,534,832,036",False,white)),(300,320))

        scr.blit((headerfont.render("Your best scores: [m]",False,white)),(280,430))

        scr.blit((myfont.render("To control: press spacebar for stage seperation and launch,",False,white)),(230,680))
        scr.blit((myfont.render("right and left arrow keys to tilt (the rocket only flies towards the right)", False,white)),(200,700))
        scr.blit((myfont.render("keys 1-8 speed up the time by 1-8x", False,white)),(300,720))

        scr.blit((myfont.render("Made by: Menno Berger & Guy Maré",False,white)),(290,760))
        
        for i in range (5):
            scr.blit((headerfont.render(str(round(highscores[i],1)),False, white)),(385,465+30*i))
            
       #Getting back into the game 
        if keys[pg.K_SPACE] and timesincekey2 > 0.3:
                game = True
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
                stage = 0
                mass0 = mass1start
                mass2 = mass2start
                mass4 = mass3start
                x = 400
                t = pg.time.get_ticks()*0.001
                heading = 0.5*pi 
                hpos = 0
                vpos = 55
            
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
