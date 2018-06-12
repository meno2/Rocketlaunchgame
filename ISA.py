from math import exp

'''
print("    ISA Calculator")

i = int(input("""1 Altitude in meters
2 Altitude in feet
3 Altitude in FL
Make your choice: """))


if i == 1:
    h = float(input("Enter altitude [m]:",))

if i == 2:
    h = float(input("Enter altitude [ft]:",))*0.3048
    
if i == 3:
    h = float(input("Enter altitude [FL]:",))*30.48'''

def ISA(h):
    T0 = float(288.15)
    P0 = float(101325.0)
    g0 = float(9.80665)
    R = float(287.0)

    hl_1 = 11000
    hl_2 = 20000
    hl_3 = 32000
    hl_4 = 47000
    hl_5 = 51000
    hl_6 = 71000
    hl_7 = 86000

    a1 = -6.5*10 ** -3
    a2 = 0
    a3 = 1*10 ** -3
    a4 = 2.8*10 ** -3
    a5 = 0
    a6 = -2.8*10 ** -3
    a7 = -2*10 ** -3

    h1 = min(h,hl_1)
    T1 = T0 -6.5*10 **-3 * h1
    P1 = P0 *(T1/T0) **(-g0/(-6.5*(10 ** -3) *R))

    if h > hl_1:
        h2 = min(h,hl_2)
        T1 = T1
        P1 = P1 * exp(-g0/(R*T1) * (h2 - hl_1))

    if h > hl_2:
        h3 = min(h,hl_3)
        T2 = T1 + a3 * (h3-hl_2)
        P1 = P1 *(T2/T1) **(-g0/( a3 *R))
        T1 = T2

    if h > hl_3:
        h4 = min(h,hl_4)
        T2 = T1 + a4 * (h4-hl_3)
        P1 = P1 *(T2/T1) **(-g0/( a4 *R))
        T1 = T2

    if h > hl_4:
        h5 = min(h,hl_5)
        T1 = T1
        P1 = P1 * exp(-g0/(R*T1) * (h5 - hl_4))
      
    if h > hl_5:
        h6 = min(h,hl_6)
        T2 = T1 + a6 * (h6-hl_5)
        P1 = P1 *(T2/T1) **(-g0/( a6 *R))
        T1 = T2
       
    if h > hl_6:
        h7 = min(h,hl_7)
        T2 = T1 + a7 * (h7-hl_6)
        P1 = P1 *(T2/T1) **(-g0/( a7 *R))
        T1 = T2
        
    rho1 = P1/(R*T1)
    return rho1

'''
if h > 86000:
    print("You're pretty much in space dude/dudette/apache, the calculations don't really apply anymore")

if h < 0:
    print("DON'T fuck with the system")

if h >= 0 and h <= 86000:
    print("Temperature:",round(T1,2),"K", "(",round(T1-273.15,2),"'C)")
    print("Pressure:", round(P1,1),"Pa")
    print("Density:", round(rho1,8),"kg/m^3")'''


