import numpy as np
import matplotlib.pyplot as plt
import math

#Входные данные:
TX_Powers_BS = 46 #[dBm] Мощность передатчика базовой станции
TX_Powers_UE = 24 #[dBm] Мощность передатчика абоненстской станции
Ant_Gains_BS = 21 #[dBi] коэффицент усиления приемо-передающей антенны базовой станции
Penetration_M = 15 #[dB] запас сигнала на проникновение сквозь стены
Interpheration_M = 1 #[dB] запас мощности на интерференцию
Feeder_LOSS = 2 # [dB]
MIMO_Gain = 3*2 # [dB]
# 1) Выполните расчет бюджета восходящего канала, используя входные данные и определите уровень максимально допустимых потерь сигнала MAPL_UL.
# Формула для расчёта: TX_Power_UE - Feeder_LOSS + Ant_Gain_BS + MIMO_Gain - PL(d) (MAPL_UL) - IM - Penetration_M >= RX_Sens_BS

# 1.1) Найдём RX_Sens_BS ( Noise_Figure + Thermal_Noise + Reqired_SINR ):
BW_UL = 10*10**6 # Полоса частот в UL
Thermal_Noise_UL = -174 + 10*math.log10(BW_UL)
#print(Thermal_Noise)
Noise_Figure_BS = 2.4 # [dB] Коэффициент шума приемника BS
Reqired_SINR_UL = 4 # [dB] Требуемое отношение SINR для UL
RX_Sens_BS = Noise_Figure_BS + Thermal_Noise_UL + Reqired_SINR_UL
#print(RX_Sens_BS)
# 1.2) Найдём MAPL_UL :
MAPL_UL = (RX_Sens_BS-TX_Powers_UE+Feeder_LOSS-Ant_Gains_BS-MIMO_Gain+Interpheration_M+Penetration_M)*(-1)
print(MAPL_UL)
#RX_Sens_BS2 = TX_Powers_UE - Feeder_LOSS + Ant_Gains_BS + MIMO_Gain - MAPL_UL - Interpheration_M - Penetration_M 
#print(RX_Sens_BS2)

# 2) Выполните расчет бюджета нисходящего канала, используя входные данные и определите уровень максимально допустимых потерь сигнала MAPL_DL.
# Формула для расчёта: TX_Power_BS - Feeder_LOSS + Ant_Gain_BS + MIMO_Gain - PL(d) (MAPL_DL) - IM - Penetration_M >= RX_Sens_US
# 2.1) Найдём RX_Sens_UE ( Noise_Figure + Thermal_Noise + Reqired_SINR ):
BW_DL = 20*10**6
Thermal_Noise_DL = -174 + 10*math.log10(BW_DL)
Noise_Figure_UE = 6 # [dB] Коэффициент шума приемника DL
Reqired_SINR_DL = 2 # [dB] Требуемое отношение SINR для DL
RX_Sens_UE = Noise_Figure_UE+Thermal_Noise_DL+Reqired_SINR_DL
#print(RX_Sens_UE)
# 2.2) Найдём MAPL_DL :
MAPL_DL = (RX_Sens_UE-TX_Powers_BS+Feeder_LOSS-Ant_Gains_BS-MIMO_Gain+Interpheration_M+Penetration_M)*(-1)
print (MAPL_DL)

# 3) Постройте зависимость величины входных потерь радиосигнала от расстояния между приемником и передатчиком по всем трем описанным в п.2.2 моделям.

# Глобальные переменные:
distance = np.arange(1, 2000) # Расстояние
f = 1.8e9 # [ГГц] Диапозон частот
plt.figure(figsize=[10,10])


# 3.1) Модель UMiNLOS (Urban Micro Non-Line-of-Sight)
def PL_UMiNLOS(distance:int): # Функция UMiNLOS
    return 26*math.log10(f/1e9)+22.7+36.7*math.log10(distance)

#Проверка:
y = []
for i in range(len(distance)):
    y.append(PL_UMiNLOS(distance[i]))
    if (int(y[i]) == int(MAPL_UL)):
        xUmiNLOS_1 = i
    if (int(y[i]) == int(MAPL_DL)):
        xUmiNLOS_2 = i

plt.plot(distance,y, label = 'UMiNLOS')
#print('UMiNLOS для MAPL_UL = ',xUmiNLOS_1)
#print('UMiNLOS для MAPL_DL = ',xUmiNLOS_2)
print('UMiNLOS ( S=5кв.км ) R =',xUmiNLOS_1,'[м]', '   Кол-во BS =', int(5000**2/(1.95*xUmiNLOS_1**2)))

# 3.2) Модель Окумура-Хата и ее модификация COST231 (Город)
def PL_COST_231(d):
    if d <= 0:
        return 0
    
    if (f > 150e6) and (f < 1500e6):
        A = 69.55
        B = 26.16
    elif (f > 1500e6) and (f < 2000e6):
        A = 46.3
        B = 33.9
    Lclutter = 0 #для U
    hBS = 30 #[м]   #(при высоте подвеса антенны базовой станции от 30 до 200 м)
    hms = 1  #[м]   #(при высоте антенны мобильного устройства от 1 до 10 м)
    a = 3.2 * (math.log10(11.75 * hms)**2) - 4.97
    if (d >= 1):
        s = 44.9 - 6.55 * math.log10(f/1e6)
    else:
        s = (47.88 + 13.9 * math.log10(f/1e6) - 13.9 * math.log10(hBS)) * (1/math.log10(50))
    
    return A + B * math.log10(f/1e6) - 13.82 * math.log10(hBS) - a + s * math.log10(d/1000) + Lclutter

#Проверка
y = []
for i in range(len(distance)):
    y.append(PL_COST_231(distance[i]))
    if (int(y[i]) == int(MAPL_UL)):
        x_cost1 = i
    if (int(y[i]) == int(MAPL_DL)):
        x_cost2 = i

plt.plot(distance,y,label = 'COST 231 Hata')
#print('COST_231 для MAPL_UL = ', x_cost1)
#print('COST_231 для MAPL_DL = ', x_cost2)
print('COST 231 Hata  (S=100кв.км) R =',x_cost1,'[м]', '   Кол-во BS =', int(100000**2/(1.95*x_cost1**2)))
# 3.3) Модель 

def Walfish_Ikegami_LOS(distance):
    if distance <= 0:
        return 0
    return 42.6 + 20*math.log10(f/1e9) + 26*math.log10(distance)

def Walfish_Ikegami_Non_LOS(distance):
    if distance == 0:
        return 0
    hBS = 50 #[м]   #(при высоте подвеса антенны базовой станции от 4 до 50 м)
    w = 200 #средняя ширина улиц, м
    h = 49 #средняя высота зданий, м
    hms = 1.5  #[м]   #(при высоте антенны мобильного устройства от 1 до 10 м)
    b = 200 # среднее расстояние между зданиями, м
    L0 = 32.44 + 20*math.log10(f/1e9) + 20*math.log10(distance)
    L1 = -16.9 - 10*math.log10(w) + 10*math.log10(f/1e9) + 20*math.log10(h - hms) + (-10 + 0.354*45)
    
    ka = 54
    kb = 18
    kf = -4 + 0.7* ((f/1e9)/925 - 1)
    
    L2 = (18*math.log10(1+hBS)) + ka + kb*math.log10(distance) + kf*math.log10(b)
    
    if (L1+L2 > 0):
        return L0 + L1 + L2
    else:
        return L0

#Проверка
y = []
for i in range(len(distance)):
    y.append(Walfish_Ikegami_LOS(distance[i]))
    if (int(y[i]) == int(MAPL_UL)):
        x_Walfish1 = i
    if (int(y[i]) == int(MAPL_DL)):
        x_Walfish2 = i
x_Walfish2 = 3401

plt.plot(distance,y,label = 'Walfish-Ikegami only LOS')

y = []
x_Walfish_non1 = 0
x_Walfish_non2 = 0
for i in range(len(distance)):
    y.append(Walfish_Ikegami_Non_LOS(distance[i]))
    if (int(y[i]) == int(MAPL_UL)):
        x_Walfish_non1 = i
    if (int(y[i]) == int(MAPL_DL)):
        x_Walfish_non2 = i
plt.plot(distance,y,label = 'Walfish-Ikegami Non LOS')
print('Walfish-Ikegami only LOS - d для MAPL_UL = ',x_Walfish1, '   d для MAPL_DL=', x_Walfish2)
print('Walfish-Ikegami Non LOS -  d для MAPL_UL = ',x_Walfish_non1, '   d для MAPL_DL=', x_Walfish_non2)


plt.axhline(y = MAPL_DL, color = 'r', linestyle = 'dashed',label = 'distance_DL')
plt.axhline(y = MAPL_UL, color = 'g', linestyle = 'dashed',label = 'distance_UL')
plt.legend(loc='lower right')
plt.grid()
plt.xlabel('Расстояние между приёмником и передатчиком, м')
plt.ylabel('Потери сигнала, дБ')
plt.show()