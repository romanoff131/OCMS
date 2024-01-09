import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

# Ввод с клавиатуры своего имени и фамилии.
name = input("Введите своё имя: ")
surname = input("Введите свою фамилию: ")

def ascii_encoder(text):
    # Преобразование текста в массив ASCII кодов символов
    ascii_codes = [ord(char) for char in text]

    # Кодирование ASCII кодов в битовую последовательность
    bit_sequence = []
    for code in ascii_codes:
        # Конвертация ASCII кода в двоичное представление
        binary_code = bin(code)[2:].zfill(8)
        # Добавление каждого бита в битовую последовательность
        bit_sequence.extend([int(bit) for bit in binary_code])

    return bit_sequence

# Использование функции и вывод битовой последовательности
text = name + " " + surname
bit_sequence = ascii_encoder(text)
#print("Битовая последовательность: ",bit_sequence)
binary_array = np.array([int(bit) for bit in bit_sequence])
print("\nБитовая последовательность:", binary_array, "[{}]".format(len(binary_array))) # пока что строка по 8 символов(0,1)

plt.figure(1)
plt.plot(binary_array)
plt.xlabel("Количество символов")

def CRC_generate(binary_array, M):
    # Добавление в битовую последовательность М-1 нулей
    binary_array = np.array(list(binary_array) + list(np.zeros(len(M)-1, dtype=int)))
    
    # XOR
    for i in range(len(binary_array) - len(M) + 1):
        if binary_array[i] == 1:
            for j in range(len(M)):
                binary_array[i+j] ^= M[j]
                
    # Возврат только последних 7 бит
    return binary_array[-7:]

M = [1, 1, 0, 0, 0, 0, 1, 1]
CRC = CRC_generate(binary_array, M)
print("\nCRC:", CRC, "[{}]".format(len(CRC)))

def Gold_array(len_G):
    G = np.zeros(len_G) # Длинна последовательности Голда
    Gold_array = []
    xg = [1,0,0,0,1]
    yg = [1,1,0,0,0]
    for i in range(len(G)): 
        Gold_array.append(xg[4]^yg[4])
        sumx = xg[0] ^ xg[2]
        sumy = yg[1] ^ yg[3]
        del xg[-1]
        del yg[-1]
        xg.insert(0, sumx)
        yg.insert(0, sumy)
        
    return np.array(Gold_array)

Gold = Gold_array(24)
print("\nСинхронизация:",Gold, "[{}]".format(len(Gold)))

N = np.concatenate((Gold, binary_array, CRC, Gold))
print("\nОбщая последовательность:", np.array2string(N,separator=''), "[{}]".format(len(N)), '\n')



def bit_sequence_to_signal(bit_sequence, N):
    # Преобразование битовой последовательности во временные отсчеты сигнала
    signal = []
    for bit in bit_sequence:
        # Формирование N отсчетов сигнала для каждого бита
        samples = [bit] * N
        signal.extend(samples)
    
    return signal
    
# Преобразование общей последовательности во временные отсчеты сигнала

fs = 1000  # Частота дискретизации в Гц
samples_per_bit_list = [1000, 1200, 1600]  # Количество отсчетов на бит

# Создаем требуемые сигналы и заполняем их до размера 2000 нулями
signals = [np.pad(np.repeat(1, spb), (0, 2000 - spb), 'constant') for spb in samples_per_bit_list]

# Вычисляем FFT и fftshift для каждого сигнала
ffts = [np.fft.fft(signal) for signal in signals]
fftshifts = [np.fft.fftshift(fft) for fft in ffts]

# Генерация соответствующих частот
freqs = [np.fft.fftfreq(2000, 1 / fs) for _ in samples_per_bit_list]
freq_shifts = [np.fft.fftshift(freq) for freq in freqs]

# Создаем графические объекты для отображения
plt.figure(figsize=(14, 10))

# Построение графиков сигналов и их спектров
titles = ['1000 отсчетов на бит', '1200 отсчетов на бит', '1600 отсчетов на бит']
for i in range(3):
    plt.subplot(3, 1, i + 1)
    plt.title(titles[i])
    plt.plot(freq_shifts[i], np.abs(fftshifts[i]))
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.xlim( -fs, fs )  # Ограничение оси X до половины частоты дискретизации
    plt.ylim(-5, 100)  # Параметры Y-оси

plt.xlabel('Частота (Гц)')
plt.tight_layout()

N = np.repeat(N, 10)

N_2 = np.zeros(len(N)*2)
start_N = int(input("Введите значение от 0 до {}:".format(len(N))))

if 0 <= start_N < len(N):
    # Вставляем массив Nx в массив Nx_2x начиная с позиции start_Nx
    N_2[start_N:start_N + len(N)] = N
else:
    print("Ошибка: значение start_Nx вне допустимого диапазона.")

# Ввод значения стандартного отклонения шума с клавиатуры
s = float(input("Введите отклонение шума: "))
# Генерация шума с помощью нормального распределения
noise = np.random.normal(0, s, len(N_2))
# Сложение информационного сигнала с шумом
noisy_signal = N_2 + noise
# Построение графика зашумленного принятого сигнала
plt.figure(3)
plt.plot(noisy_signal)
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.title('Зашумленный принятый сигнал')

result = noisy_signal[::10] 

corr = correlate(result, Gold, mode='full') 
threshold = len(Gold)/2 - 0.2
indices = np.where(corr >= threshold)[0]
print("\nИндексы где найдена синхронизация", indices)
if len(indices) >= 2:
    result = result[indices[0]:(indices[1]-len(Gold)+1)]
else:
    print("Недостаточно элементов в массиве indices")

decod = []
for i in range(len(result)):
    if result[i] > 0.7:
        decod.append(1)
    else:
        decod.append(0)
decod = np.array(decod)
dec = list(decod)
print("\ndecod", decod)
print("\ndec", dec)
print("\nСигнал без синхронзаций с CRC:", np.array2string(decod,separator=''), "[{}]".format(len(decod)))

plt.figure(4)
plt.plot(decod)
plt.ylabel("Амплитуда")
plt.xlabel("Время")
plt.title('Сигнал без синхронзаций с CRC')

def crc_decod(arr, M):
    arr_b = arr.copy()
    for i in range(len(arr) - len(M) + 1):
        if arr[i] == 1:
            for j in range(len(M)):
                arr[i+j] ^= M[j]
    if arr.all() == 0:
        print("\nОшибок передачи не обнаружено")
    return arr_b[1:-7]


decod = crc_decod(decod, M)
print("\nСигнал без синхронзаций и CRC: ",np.array2string(decod,separator=''), "[{}]".format(len(decod)))

plt.figure(5)
plt.plot(decod)
plt.ylabel("Амплитуда")
plt.xlabel("Время")
plt.title('Сигнал без синхронзаций и CRC')


def bits_to_ascii(bit_array):
    # Преобразование массива бит в строку
    bit_string = ''.join(str(bit) for bit in bit_array)
    
    # Разделение строки на 8-битные блоки
    bit_blocks = [bit_string[i:i+8] for i in range(0, len(bit_string), 8)]
    
    # Преобразование каждого 8-битного блока в целое число
    ascii_list = [int(block, 2) for block in bit_blocks]
    
    # Преобразование целых чисел в символы ASCII
    ascii_string = ''.join(chr(ascii) for ascii in ascii_list)
    
    return ascii_string

# Вывод результата
ascii_result = bits_to_ascii(decod)
print("\nПолучившийся текст: ",ascii_result)

#plt.figure(6)
#plt.plot(ascii_result)
plt.title('Получившийся текст')

plt.show()