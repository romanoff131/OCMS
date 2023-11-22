import math
import matplotlib.pyplot as plt 
import numpy as np

def print_graph(PLd,ddl,dul):
    plt.figure(1)
    plt.plot(PLd)
    plt.axhline(MAPL_UL, color="red")
    plt.axhline(MAPL_DL,color="yellow")
    plt.axvline(ddl,color="yellow")
    plt.axvline(dul,color="red")
    plt.show()

def UMiNLOS(PLd):
    dul = 0
    ddl = 0
    i = 0
    for i in range(1,3000):
        per = 26 * math.log10(1.8) + 22.7 + 36.7 * math.log10(i)
        PLd.append( 26 * math.log10(1.8) + 22.7 + 36.7 * math.log10(i))

        if round(per,1) == round(MAPL_DL,1):
            ddl = i
        if round(per,1) == round(MAPL_UL,1):
            dul = i

    print(ddl)
    print(dul)
    print_graph(PLd,ddl,dul)



#Входные данные:
TX_Powers_BS = 46 #[dBm] Мощность передатчика базовой станции
TX_Powers_UE = 24 #[dBm] Мощность передатчика абоненстской станции
Ant_Gains_BS = 21 #[dBi] коэффицент усиления приемо-передающей антенны базовой станции
Penetration_M = 15 #[dB] запас сигнала на проникновение сквозь стены
Interpheration_M = 1 #[dB] запас мощности на интерференцию
r = 1 #[m]
S_BS = 1.95*r**2 #[m**2]
S_ter = 100*10**5 #[m**2]
PL_d = 1 #[dB]
Feeder_LOSS = 2 # [dB]
MIMO_Gain = 3*2 # [dB]
# 1) Выполните расчет бюджета восходящего канала, используя входные данные и определите уровень максимально допустимых потерь сигнала MAPL_UL.
# Формула для расчёта: TX_Power_UE - Feeder_LOSS + Ant_Gain_BS + MIMO_Gain - PL(d) (MAPL_UL) - IM - Penetration_M >= RX_Sens_BS

# 1.1) Найдём RX_Sens_BS ( Noise_Figure + Thermal_Noise + Reqired_SINR ):
BW = 1.8*10**7 # Полоса частот в DL и UL
Thermal_Noise = -174 + 10*math.log10(BW)
Noise_Figure_BS = 2.4 # [dB] Коэффициент шума приемника BS
Reqired_SINR_BS = 4 # [dB] Требуемое отношение SINR для UL

RX_Sens_BS = Noise_Figure_BS + Thermal_Noise + Reqired_SINR_BS
#print("RX_Sens_BS: ",RX_Sens_BS)

# 1.2) Найдём MAPL_UL :
MAPL_UL = (RX_Sens_BS - TX_Powers_UE + Feeder_LOSS - Ant_Gains_BS - MIMO_Gain + Interpheration_M + Penetration_M) * -1
print("\nMAPL_UL: ",MAPL_UL)
#RX_Sens_BS2 = TX_Powers_UE - Feeder_LOSS + Ant_Gains_BS + MIMO_Gain - MAPL_UL - Interpheration_M - Penetration_M 
#print(RX_Sens_BS2)

# 2) Выполните расчет бюджета нисходящего канала, используя входные данные и определите уровень максимально допустимых потерь сигнала MAPL_DL.

# Формула для расчёта: TX_Power_BS - Feeder_LOSS + Ant_Gain_BS + MIMO_Gain - PL(d) (MAPL_DL) - IM - Penetration_M >= RX_Sens_US

# Найдём RX_Sens_UE ( Noise_Figure + Thermal_Noise + Reqired_SINR ):
Noise_Figure_UE = 6 # [dB] Коэффициент шума приемника DL
Reqired_SINR_UE = 2 # [dB] Требуемое отношение SINR для DL

RX_Sens_UE = Noise_Figure_UE + Thermal_Noise + Reqired_SINR_UE
#print("RX_Sens_UE: ",RX_Sens_UE)

# 2.2) Найдём MAPL_DL :
MAPL_DL = (RX_Sens_UE - TX_Powers_BS + Feeder_LOSS - Ant_Gains_BS - MIMO_Gain + Interpheration_M + Penetration_M) * -1
print ("MAPL_DL: ",MAPL_DL,"\n")

PL = []
#UMiNLOS(PL)
#COST231(PL)
dul =0
ddl = 0
i = 0
A=B=0
hBS = hms = 20
a=s=0
Lclutter = 0
h_BW = 1.8

if 0.15 < h_BW < 1.5:
    A = 69.55
    B =26.16
if 1.5 <= h_BW < 2.0:
    A = 46.3
    B = 33.9
#buta = input()
#match buta():
#    case[1]:
#        a = 3.2 * (math.log10(11.75 * hms)**2)- 4.97 #DU & U
#    case[2]:
#        a = (1.1 * math.log10(h_BW * 10**3) * hms - (1.56 * math.log10(h_BW * 10**3) - 0.8)) #SU & RURAL & ROAD
print("Enter a:\n1.Плотная застройка\n2.Город\n3.Пригород\n4.Сельская местность\n5.Трасса\n")

butb = int
butb = input()

print(type(butb))

match butb:
    case 1:
        print(butb,"rwgefbeb")
        Lclutter = 3#DU
        a = 3.2 * (math.log10(11.75 * hms)**2)- 4.97 #DU & U
    case 2:
        Lclutter = 0#U
        a = 3.2 * (math.log10(11.75 * hms)**2)- 4.97 #DU & U
    case 3:
        print(butb,"rwgefbeb")
        Lclutter = -((2*(math.log10(h_BW)**2))+5.4)#SU
        a = (1.1 * math.log10(h_BW * 10**3) * hms - (1.56 * math.log10(h_BW * 10**3) - 0.8)) #SU & RURAL & 
    case 4:
        Lclutter = -(4.78*(math.log10(h_BW)**2)-18.33*(math.log10(h_BW))+40.94)#RURAL
        a = (1.1 * math.log10(h_BW * 10**3) * hms - (1.56 * math.log10(h_BW * 10**3) - 0.8)) #SU & RURAL & ROAD
    case 5:
        Lclutter = -(4.78*(math.log10(h_BW)**2)-18.33*(math.log10(h_BW))+35.94)#ROAD
        a = (1.1 * math.log10(h_BW * 10**3) * hms - (1.56 * math.log10(h_BW * 10**3) - 0.8)) #SU & RURAL & ROAD
    case _:
        print("not")


for i in range(1,3000):
    per = 26 * math.log10(1.8) + 22.7 + 36.7 * math.log10(i)
    #PL.append( 26 * math.log10(1.8) + 22.7 + 36.7 * math.log10(i))

    PL.append(A + B * math.log10(BW) - 13.82 * math.log10(hBS) - a + s * math.log10(i) + Lclutter)

    if round(per,1) == round(MAPL_DL,1):
        ddl = i
    if round(per,1) == round(MAPL_UL,1):
        dul = i
print(ddl)
print(dul)