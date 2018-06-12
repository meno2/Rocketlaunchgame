#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 10:17:47 2018

@author: guymare
"""
from math import*

#gives change in mass under acceleration
def mass_acc(m, isp, thrust, dt): 
    mass_flow = float(thrust / (isp *9.80655))
    m_new = float(m - (mass_flow * dt))
    
    return m_new

#gives acc due to drag
def acc_drag(v, rho, r, m):
    A_cross = pi * (r ** 2)
    a_d = float((0.5 * rho * (v**2) * A_cross * 0.3) / m)
    
    return a_d

#gives acc due to thrust
def acc_thrust(thrust, m):
    a_t = float(thrust / m)
    
    return a_t

#gives total acc along v vector
def acc_vvector(v, rho, r, m, thrust, isp, dt):
    m_new = mass_acc(m, isp, thrust, dt)
    a_v = float(acc_thrust(thrust, m_new) - acc_drag(v, rho, r, m_new))
    
    return a_v

#updates x, y, v(magnitude), heading
def flight_path(v, rho, r, m, thrust, isp, dt, heading, x, y):
    
    ax = acc_vvector(v, rho, r, m, thrust, isp, dt) * cos(heading)
    ay = acc_vvector(v, rho, r, m, thrust, isp, dt) * sin(heading) - 9.80655
    
    vx = (v * cos(heading)) + ax * dt
    vy = (v * sin(heading)) + ay * dt
    
    Xnew = x + vx * dt
    Ynew = y + vy * dt 
    
    Vnew = sqrt((vy**2) + (vx**2))

    if vx < 0:
        heading_update = atan(vy / vx)

    if vx > 0:
        heading_update = atan(vy / vx)

    if vx == 0:
        heading_update = 0
    
    #xplt.append(Xnew)
    #yplt.append(Ynew)
    print(ay)
    #print("vy:",vy,"         ",vx)
    
    return Xnew, Ynew, Vnew, heading_update
    
