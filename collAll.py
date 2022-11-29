import time
import random
import pygame
import Need.MAP as MAP
import Need.VARRTstar as VARRTstar
from tkinter import *
import pandas as pd
import numpy as np
import math


#**************************** DEF VARIABLE***************************************************

echel=2
NuObs = 70
Pas = 10
landa = 500

Start=(10,10)
Goal=(520,520)

red = (255, 0, 0)
green = (0, 255, 0)
bleu = (0, 0, 255)
grey = (0, 0, 0)
yallow = (255, 255, 0)

#**************************** DEF FONCTION***************************************************
cases=[]
casefiltrer=[]

def givepoint():
    x = int(random.uniform(20, 490)/20)*20
    y = int(random.uniform(20, 490)/20)*20
    return (x, y)

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def Draw_position(p,coleur):
    rectangle = pygame.Rect(p, (20, 20))
    pygame.draw.rect(map.Map, coleur, rectangle)
    pygame.display.update()

def excuter_action(pos,action):
    if action==0:
        new_pos=(pos[0],pos[1]-20)
    if action==1:
        new_pos = (pos[0]+20, pos[1] - 20)
    if action==2:
        new_pos = (pos[0]+20, pos[1])
    if action==3:
        new_pos = (pos[0] + 20, pos[1]+20)
    if action==4:
        new_pos = (pos[0] , pos[1]+20)
    if action==5:
        new_pos = (pos[0]- 20, pos[1]+20)
    if action==6:
        new_pos = (pos[0]-20, pos[1])
    if action==7:
        new_pos = (pos[0] - 20, pos[1]-20)
    if action == 8:
        new_pos = pos

    Draw_position(new_pos,yallow)

    return new_pos

def casetraget(traget,matrice):
    cases=[]
    for p in range(len(traget)):
        X = int(traget[p][0] / 20) * 20
        Y = int(traget[p][1] / 20) * 20
        if (X, Y) in cases:
            pass
        else:
            if matrice[int(X/20)][int(Y/20)]==1:
                pass
            else:
                cases.append((X, Y))
    return cases

def filtrecases(cases,map):

    casefiltrer=[cases[0]]

    for i in range(1,len(cases)-1):
        if distance(cases[i-1],cases[i+1])>28.3:
            casefiltrer.append(cases[i])
        else:
            if cases[i-1] in casefiltrer:
                pass
            else:
                casefiltrer.append(cases[i])
    casefiltrer.append(cases[-1])

    for p in casefiltrer:
        rectangle = pygame.Rect(p, (20, 20))
        pygame.draw.rect(map.Map, bleu, rectangle)
    pygame.display.update()


    return casefiltrer

def get_sortie_capteur(p,matrice,map):


    I = [0 for j in range(8)]
    M = 53

#                    I0                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y - k
        if yv < 0:
            k = M
        else:
            if matrice[x][yv] == 0:
                I[0] = k
            else:
                k = M
        k = k + 1

#                    I1                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y - k
        xv = x + k
        if yv < 0 or xv > 52:
            k = M
        else:
            if matrice[xv][yv] == 0:
                I[1] = k
            else:
                k = M
        k = k + 1

#                    I2                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y
        xv = x + k
        if xv > 52:
            k = M
        else:
            if matrice[xv][yv] == 0:
                I[2] = k
            else:
                k = M
        k = k + 1

#                    I3                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y + k
        xv = x + k
        if yv > 52 or xv > 52:
            k = M
        else:
            if matrice[xv][yv] == 0:
                I[3] = k
            else:
                k = M
        k = k + 1

#                    I4                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y + k
        xv = x
        if yv > 52:
            k = M
        else:
            if matrice[xv][yv] == 0:
                I[4] = k
            else:
                k = M
        k = k + 1

#                    I5                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y + k
        xv = x - k
        if xv < 0 or yv > 52:
            k = M
        else:
            if matrice[xv][yv] == 0:
                I[5] = k
            else:
                k = M
        k = k + 1

#                    I6                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y
        xv = x - k
        if xv < 0:
            k = M
        else:
            if matrice[xv][yv] == 0:
                I[6] = k
            else:
                k = M
        k = k + 1

#                    I7                  #

    x, y = int(p[0] / 20), int(p[1] / 20)
    k = 1
    while (k < M):
        yv = y - k
        xv = x - k
        if xv < 0 or yv < 0:
            k = M
        else:
            if matrice[xv][yv] == 0:
                I[7] = k
            else:
                k = M
        k = k + 1




    I.append((-p[0]+map.goal[0])/10)
    I.append((-p[1]+map.goal[1])/10)

    #print(I, "     ", (x, y), "    ", (xdirection, ydirection), "    ", p)
    return I

def get_action(VS,i,I):
    p=VS[i]
    x, y = int(p[0] / 20), int(p[1] / 20)
    if VS[i] == VS[-1]:
        I.append(8)
    else:
        xdirection = int(VS[i + 1][0] / 20)
        ydirection = int(VS[i + 1][1] / 20)

        if x == xdirection:
            if y < ydirection:
                I.append(4)
            elif y == ydirection:
                I.append(8)
            else:
                I.append(0)
        elif x < xdirection:
            if y == ydirection:
                I.append(2)
            if y < ydirection:
                I.append(3)
            if y > ydirection:
                I.append(1)
        else:
            if y == ydirection:
                I.append(6)
            if y < ydirection:
                I.append(5)
            if y > ydirection:
                I.append(7)
    return I

def donnes(matrice,Trajet_filtrer,map):

    VS=Trajet_filtrer
    #["Capteur 0","Capteur 1","Capteur 2","Capteur 3","Capteur 4","Capteur 5","Capteur 6","Capteur 7","direction","action"]
    IA=[]
    for i in range(len(Trajet_filtrer)):
        I=get_sortie_capteur(VS[i],matrice,map)
        I=get_action(VS,i,I)

        IA.append(I)
    print(IA)
    return IA


#**************************** GET MATRIC ***************************************************






def FCTrajet(map):
    RRT = VARRTstar.VARRTstar_Methode(Pas, map)
    trajet=RRT.Excute()
    return trajet

def ExtraxtA(St,Go):
    PositionMAP = [givepoint() for i in range(NuObs)]
    TailleMAP = [(random.choice([20]), random.choice([20])) for i in range(NuObs)]
    map = MAP.Map(St, Go, (530, 530), "MAP 1", PositionMAP, TailleMAP, echel)
    for k in range(1):

        map.DrawMap()
        resulta=True
        matrice=map.get_Matrice_Map()
        while resulta:

            trajet_continu=FCTrajet(map)
            XXX=True
            for p in range(len(trajet_continu)-1):
                if distance(trajet_continu[p],trajet_continu[p+1])<30:
                    pass
                else:
                    XXX=False
            if XXX==False:
                pass
            else:
                resulta=False


        casesDisc=casetraget(trajet_continu,matrice)

        casesFiltre=filtrecases(casesDisc,map)

        DONNES=donnes(matrice,casesFiltre,map)
    return DONNES

def ExtraxtB(St,Go):
    PositionMAP = [givepoint() for i in range(NuObs)]
    TailleMAP = [(random.choice([20,30]), random.choice([20,30])) for i in range(NuObs)]
    map = MAP.Map(St, Go, (530, 530), "MAP 1", PositionMAP, TailleMAP, echel)
    for k in range(1):

        map.DrawMap()
        resulta=True
        matrice=map.get_Matrice_Map()
        while resulta:

            trajet_continu=FCTrajet(map)
            XXX=True
            for p in range(len(trajet_continu)-1):
                if distance(trajet_continu[p],trajet_continu[p+1])<30:
                    pass
                else:
                    XXX=False
            if XXX==False:
                pass
            else:
                resulta=False


        casesDisc=casetraget(trajet_continu,matrice)

        casesFiltre=filtrecases(casesDisc,map)

        DONNES=donnes(matrice,casesFiltre,map)
    return DONNES

def ExtraxtC(St,Go):
    PositionMAP = [givepoint() for i in range(NuObs)]
    TailleMAP = [(random.choice([20,30,40]), random.choice([20,30,40])) for i in range(NuObs)]
    map = MAP.Map(St, Go, (530, 530), "MAP 1", PositionMAP, TailleMAP, echel)
    for k in range(1):

        map.DrawMap()
        resulta=True
        matrice=map.get_Matrice_Map()
        while resulta:

            trajet_continu=FCTrajet(map)
            XXX=True
            for p in range(len(trajet_continu)-1):
                if distance(trajet_continu[p],trajet_continu[p+1])<30:
                    pass
                else:
                    XXX=False
            if XXX==False:
                pass
            else:
                resulta=False


        casesDisc=casetraget(trajet_continu,matrice)

        casesFiltre=filtrecases(casesDisc,map)

        DONNES=donnes(matrice,casesFiltre,map)
    return DONNES
pourcentage=0
Don_Global=[]


for l in range(200):
    DONNES=ExtraxtB(Start,Goal)
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage=pourcentage+1
    print("------------------ ",pourcentage/8,"%")



    DONNES = ExtraxtB(Goal, Start)
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtB((10,520), (520,10))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtB((520,10),(10,520))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtB((250,10),(251,520))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtB((10,250),(520,250))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtB((250,520),(251,10))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtB((520,250),(10,250))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")

for l in range(200):
    DONNES=ExtraxtC(Start,Goal)
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage=pourcentage+1
    print("------------------ ",pourcentage/8,"%")



    DONNES = ExtraxtC(Goal, Start)
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtC((10,520), (520,10))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtC((520,10),(10,520))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtC((250,10),(251,520))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtC((10,250),(520,250))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtC((250,520),(251,10))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtC((520,250),(10,250))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")

for l in range(200):
    DONNES=ExtraxtA(Start,Goal)
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage=pourcentage+1
    print("------------------ ",pourcentage/8,"%")



    DONNES = ExtraxtA(Goal, Start)
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtA((10,520), (520,10))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtA((520,10),(10,520))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtA((250,10),(251,520))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtA((10,250),(520,250))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtA((250,520),(251,10))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")


    DONNES = ExtraxtA((520,250),(10,250))
    Don_Global = Don_Global + DONNES
    print(len(Don_Global))
    pourcentage = pourcentage + 1
    print("------------------ ", pourcentage / 8, "%")

output = pd.DataFrame(Don_Global)
output.to_excel('XC.xlsx', index=False, engine='xlsxwriter')
print("ok")

