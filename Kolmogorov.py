# Решение системы дифур Колмогорова
# граф системы и описание тут http://mathhelpplanet.com/static.php?p=uravneniya-kolmogorova
# Параметр mm - варьирует величину интенсивности отказа одного из блоков
# Графики строятся при различных значениях этого параметра


import sys
from scipy import integrate #численное интегрирование
import numpy as np #вектора и матрицы
import matplotlib.pyplot as plt #графики

#Вычисляет значение правой части в момент времени t
def func(p,t):
	return D.dot(p)  

## решаем систему однородных дифур
def calc_system_odeint(tmax=3*24*3600):
    p = np.array([1.0, 0.0, 0.0, 0.0])
    t=np.linspace(0, tmax, 50)
    result = integrate.odeint(func,p,t) 
    result = np.insert(result, 0, t[:], axis=1) # добавляем к матрице результатов - в самое начало колонку времени
    return result

# добавляет решение на график
def add_to_plot(result, lbl):
	ax = plt.subplot(111)
	plt.xlabel(u't, c')
	plt.ylabel(u'p, %')
	plt.title(u'Reliability of system P(t) with different lambda')
	plt.grid(True)
	probap = result[:,1] + result[:,2] + result[:,3]   # cуммарная вероятность
	line_pr=ax.plot(result[:,0]/3600, 100*probap, linewidth=2, label=lbl)
	ax.legend(loc='upper right')
	#plt.savefig("test.png")
	return;


####################################################################################################################
#
# Структура системы и эксперименты
# граф системы тут http://mathhelpplanet.com/static.php?p=uravneniya-kolmogorova
# 
###################################################################################

# Исследуем зависимость системы от коэффициента лямбда
for mm in range(1, 10):
	λ01=mm*1.0 * 10**-5
	λ02=mm*2.0 * 10**-5
	λ10=2.0 * 10**-5
	λ13=mm*2.0 * 10**-5
	λ20=mm*3.0 * 10**-5
	λ23=1.0 * 10**-5
	λ31=3.0 * 10**-5
	λ32=2.0 * 10**-5

	D=np.array([
			[-(λ01+λ02), λ10, λ20, 0],				# p′0=λ10p1+λ20p2−(λ01+λ02)p0
			[λ01, -(λ10+λ13), 0, λ31],				# p′1=λ01p0+λ31p3−(λ10+λ13)p1
			[λ02, 0, -(λ20+λ23), λ32], 				# p′2=λ02p0+λ32p3−(λ20+λ23)p2
			[0, λ13, λ23, -(λ31+λ32)],				# p′3=λ13p1+λ23p2−(λ31+λ32)p3
	]);

    
	result = calc_system_odeint(tmax=1.5*24*3600)
	add_to_plot(result, "P" + str(mm))

print(u"Надежность системы от P(t,λ)")
plt.show()
