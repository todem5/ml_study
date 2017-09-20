#!/usr/bin/python
#coding=utf-8
# http://0agr.ru/blog/2011/04/15/%D1%81%D0%B8%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81-%D0%BC%D0%B5%D1%82%D0%BE%D0%B4/
#
# MustRead
# https://habrahabr.ru/post/330648/
# https://ru.stackoverflow.com/questions/472169/%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%B5%D0%B9%D1%88%D0%B8%D0%B9-%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1-%D1%80%D0%B5%D1%88%D0%B8%D1%82%D1%8C-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D1%83-%D0%BF%D0%BE%D1%85%D0%BE%D0%B6%D1%83%D1%8E-%D0%BD%D0%B0-%D0%BB%D0%B8%D0%BD%D0%B5%D0%B9%D0%BD%D0%BE%D0%B5-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5
# https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D0%BD%D0%B5%D0%B9%D0%BD%D0%BE%D0%B5_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5
# http://cyclowiki.org/wiki/%D0%A2%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%BD%D0%B0%D1%8F_%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0
# http://docplayer.ru/37092434-Reshenie-zadach-lineynogo-programmirovaniya-s-ispolzovaniem-gnu-octave-glpk-i-python-a-v-ponomarev.html
# http://www.machinelearning.ru/wiki/index.php?title=%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%9D%D0%B5%D0%BB%D0%B4%D0%B5%D1%80%D0%B0-%D0%9C%D0%B8%D0%B4%D0%B0



 
 
"""
Решение задач линейного программирования с помощью симплекс-таблицы
(метод последовательного улучшения плана)
Реализация: Григорьев Алексей
"""
 
# установить в False, если не нужно показывать информацию о ходе выполнения
SHOW_INFO = True
 
 
# задаем функции, которые понадобятся для вычислений
inf = float('infinity')
# возвращает массив, содержащий столбец матрицы
get_col = lambda col, array: [row[col] for row in array]
# транспонируем матрицу
trans = lambda array: [get_col(i, array) for i in xrange(len(array[0]))]
 
# деление двух чисел - делим только те числа, что больше нуля
divide_or_inf = lambda a, b: a / b if b > 0 else inf
 
# функции, одна делит весь массив на число, вторая умножает
array_div = lambda array, divider: [el / divider for el in array]
array_mul = lambda array, divider: [el * divider for el in array] 
minus = lambda a, b: a - b
 
# функции для обработки линейных неравенств
 
# в зависимости от знака неравенства функции возвращают различный результат
 
# первая часть результата - массив из 0 и 1 (-1) на месте переменной
# вторая часть результата - тип переменной. обозначения:
#     f - свободная переменная; b - базисная переменная; t - временная переменная
# третья часть сообщает о том, идет ли эта переменная в базис при первой итерации 
 
def less_or_equals(i, _m):
    # <=: добавляется базисная переменная со знаком "+"
    res = [0] * _m
    res[i] = 1.0
    return [res], ["b"], [True]
 
def greater_or_equals(i, _m):
    # >=: добавляется базисная переменная со знаком "-" и временная переменная со знаком "+"
    res1 = [0] * _m
    res1[i] = -1.0
    res2 = [0] * _m
    res2[i] = 1.0
    return [res1, res2], ["b", "t"], [False, True]
 
def equals(i, _m):
    # =:  добавляется временная переменная со знаком "+"
    res = [0] * _m
    res[i] = 1.0
    return [res], ["t"], [True]
 
 
def simplex(A, I, B, Z, look_max=True):
    """
    A - двумерный массив, коэффициенты лин. неравенства
    I - знаки (не)равенства - один из знаков <=, =, >=
    B - свободные члены неравенства
    Z - коэффициенты при целевой функции
    look_max - ищем максимум, если True
    """
    # print A, I, B, Z
 
    # количество неравенств системы
    m = len(A)
    # количество участвующих в системе уравнений
    n = len(A[1])
 
    # если нужно найти максимум, то переходим к эквивалентной задаче на поиск минимума:
    # заменяем все коэффициенты при целевой функции на обратные
    if look_max:
        Z = map(lambda x: -x, Z)
 
    # переменные добавляются в зависимости от знака неравенства:
    # <=: добавляется базисная переменная со знаком "+"
    # >=: добавляется базисная переменная со знаком "-" и временная переменная со знаком "+"
    # =:  добавляется временная переменная со знаком "+"
    # однако базис на первой итерации должны образовывать переменные со знаком "+"
 
    sign = {"<=": less_or_equals, ">=": greater_or_equals, "=": equals}    
 
    # тут запоминаем типы переменных
    types = ["f"] * n
    # тут - добавляемую матрицу
    els = []
 
    # нужно запоминать, на какой строке находится какая переменная
    # для этого заведем массив длинной n + m, где первые n элементов будут для свободных переменных,
    # а последующие элементы - для базисных 
    # записывает -1 для переменных, находящихся не в базисе,
    # для находящихся в базисе записываем номер строки
    involved = [-1] * n
 
    # этот класс - счетчик, для возвращения номера переменной, участвующей в базисе
    class Counter():
        cnt = -1
        def inc(self):
            self.cnt = self.cnt + 1
            return self.cnt 
 
    cnt = Counter()
 
    # для всех уравнений смотрим знак и выполняем соответствующие знаку действия
    for i in xrange(len(I)):
        func = sign[I[i]]
        ar, ty, base = func(i, m)
 
        # если попадается переменная, идущая в базис, то помечаем ее
        involved = involved + [(cnt.inc() if b else -1) for b in base]
        types = types + ty
        els = els + ar
 
    # print zip(types, involved)
 
    # количество добавленных переменных
    varibles = len(els) 
 
    # транспонируем матрицу c добавляемыми переменными - для добавления к матрице A
    o = trans(els)
 
    # print o
 
    # добавляем базисные переменные - создаем базис
    # т.к. неравенств m, то и базисных переменных так же должно быть m
    # создаем единичную матрицу для базисных переменных
    # o = [[(1 if i == j else 0) for j in xrange(m)] for i in xrange(m)]
 
    # теперь неизвестных в системе n + m шт - от 1 до n свободные, от n + 1 до m - базисные
    # совмещаем матрицы 
    A_ = [a + b for (a, b) in zip(A, o)]
    # print A_
    # дополняем нулями целевую функцию - в местах, относящихся к новым переменным
    Z_ = Z + [0] * varibles
    # результат целевой функции
    Z0 = 0 
 
    # эту лямбда-функцию используем для форматированного отображения массивов
    str2 = lambda ar: "[" + " ".join(["%.4f" % e for e in ar]) + "]"
 
    iter_a = 0
 
    if SHOW_INFO:
        print iter_a
        print "\n".join(["%s = %.4f" % (str2(a), b) for (a, b) in zip(A_, B)])
        print 
 
    l = len(involved)
 
    # выполняем, пока решение не найдено
    while 1:
        # находим разрешающий столбец - столбец, в котором целевая функция имеет 
        # наименьший параметр (наибольший по модулю)
        # переменная из разрешающего столбца попадает в базис при следующей итерации
 
        # если на данной итерации в базисе участвуют временные переменные, то 
        # всместо строки z необходимо рассматривать оценку, в которой участвуют 
        # только строки таблцы, соответвующие временным переменным
 
        # получаем переменные, участвующие в текущей итерации в качестве базиса
        # и узнаем их тип
        # если среди типов есть временный, т.е. t, то минимум ищем по строке 
        # "оценка", иначе по строке функции z
 
        current_vars = [i for (i, e) in zip(xrange(l), involved) if e != -1] 
        current_vars_types = set([types[i] for i in current_vars])
 
        # проверяем, участвуют ли временные пременные в составлении базиса
        temporary_vars_inv = "t" in current_vars_types
 
 
        # если в строке z все коэффициенты неотрицательны, значит, решение найдено
        # значения временных переменных в расчет не берем вообще
        # if not temporary_vars_inv:
        check = [el for (i, el) in zip(xrange(l), Z_) if (el < 0 and types[i] != "t")]
 
        if not check and not temporary_vars_inv:
            print "Решение найдено:"
 
            # теперь проверям, какие из первоначально свободных переменных теперь
            # базисные - в них будет ответ
            elements = [(i, e) for (i, e) in zip(range(n), involved[:n]) if e != -1] 
            print "\n".join(["x_%d = %.4f" % (i, B[e]) for (i, e) in elements])
            print 
 
            # если ищем минимум, то обращаем знак целевой функции
            if not look_max:
                Z0 = -Z0
 
            print "значение целевой функции - %f" % Z0 
 
            return         
 
 
        if temporary_vars_inv:
            # строим строку "оценка" - в нее входят значения всех соответсвующих 
            # элементов для строк, у которых базис - временная переменная
            # для ее получения суммируем все значения для текущего столбца
            # строки, соответсвующей базисным переменным
 
            # выбираем строки, соответсвующие временным переменным
            tmpv = [involved[i] for i in current_vars if types[i] == "t"]
            # и составляем строку "оценка"
            est = [-sum([A_[j][i] for j in tmpv]) for i in xrange(l)]
 
            # для которой теперь нужно найти максимум по модулю
            if SHOW_INFO: print "est", str2(est)
 
            col = est
        else:
            if SHOW_INFO: print "Z", str2(Z_)
            col = Z_
 
        min_col_index = col.index(min(col))
        min_col = get_col(min_col_index, A_)
 
        # если в разрешающем стоблце все элементы меньше или равны 0, то решений нет
        check = [el for el in min_col if el > 0]
        if not check:
            print
            print "Решение не может быть найдено - задача не ограничена"
            return 
 
 
        # находим разрешающую строку
        # для этого разделим элементы столбца свободных членов на соответсвующие им 
        # элементы разрешающего стобца, и выберем минимум из неравных нулю элементов
        # элемент, соответсвующий разрешающей строке выходит из базиса
 
        ratio = map(divide_or_inf, B, min_col)
        min_row_index = ratio.index(min(ratio))
 
        # разрешающий элемент находится на пересечении разрешающего столбца и строки
        el = A_[min_row_index][min_col_index]
 
        # новая переменная становится базисной, а одна из базисных становится свободной
        # цель дальнейших преобразований - превратить столбец с новой базисной переменной
        # в единичный
 
        # исключаем старую базисную переменную
        involved[involved.index(min_row_index)] = -1
        # помечаем новую переменную, как базисную
        involved[min_col_index] = min_row_index
 
 
        # для этого берем всю разрешающую строку и делим на разрешающий элемент - 
        # в результате этого мы получим 1 для разрешающего элемента
        # так же делим на этот элемент соответсвующий свободный член
        A_[min_row_index] = array_div(A_[min_row_index], el)
        min_row = A_[min_row_index]
        B[min_row_index] = B[min_row_index] / el
 
        # далее необходимо получить 0 в стобце для всех остальных элементов и для z строки
        # для этого смотрим, какое значение стоит в столбце для текущей строки и умнажаем всю строку
        # на обратное ему (т.е. если стоит 1, умножаем всю строку на -1) 
        # и складываем полученную строку с тем, что было
        for i in [x for x in range(m) if x != min_row_index]:
            cur_el = A_[i][min_col_index]
            if cur_el != 0:
                A_[i] = map(minus, A_[i], array_mul(min_row, cur_el))
                B[i] = B[i] - B[min_row_index] * cur_el
 
        # тоже самое делаем для z строки
        cur_el = Z_[min_col_index]
        Z_ = map(minus, Z_, array_mul(min_row, cur_el))
        Z0 = Z0 - B[min_row_index] * cur_el
 
 
        iter_a += 1
        # тут выводим отчет по каждой итерации
        if SHOW_INFO:
            print 
            print iter_a
            print "\n".join(["%s = %.4f" % (str2(a), b) for (a, b) in zip(A_, B)])
            print "el:", el
            print "ratio:", str2(ratio)
            print "Z", str2(Z_)
            print "current_vars:", current_vars
            print "current_vars_types", current_vars_types
            print "temporary_vars_inv:", temporary_vars_inv
            print 
 
        if iter_a == 100:
            print "Решение не найдено за 100 итераций" 
            break
 
 
to_float = lambda a: [float(f) for f in a]
_to_float = lambda a: [to_float(f) for f in a]
 
if __name__ == "__main__":
 
    print "\n", "=" * 60, "\n"
 
    system = [
        ([2, 1], "<=", 64), 
        ([1, 3], "<=", 72), 
        ([0, 1], "<=", 20),
    ]
 
    print "system:", system
 
    A, I, B = zip(*system)
    Z = [4, 6]
 
    simplex(_to_float(A), I, to_float(B), to_float(Z), look_max=True)
    """
    Ожидаемый ответ:
    x0 = 24, x1 = 16, zmax = 192.
    """
 
    print "\n", "=" * 60, "\n"
 
    system = [
        ([3, 4], ">=", 6), 
        ([1, 3], "=",  3), 
        ([2, 1], "<=", 4),
    ]
 
    print "system:", system
 
    A, I, B = zip(*system)
    Z = [4, 16]
 
    simplex(_to_float(A), I, to_float(B), to_float(Z), look_max=True)
    """
    Ожидаемый ответ:
    x0 = 6/5; x1 = 3/5; zmax = 72/5. 
    """
 
    print "\n", "=" * 60, "\n"
 
    system = [
        ([10, 6, 12], ">=", 50), 
        ([7, 10, 11], ">=", 45), 
    ]
 
    print "system:", system
 
    A, I, B = zip(*system)
    Z = [2.20, 1.95, 2.87]
 
    simplex(_to_float(A), I, to_float(B), to_float(Z), look_max=False)
    """
    Ожидаемый ответ:
    x0 = 0.38; x1 = 0; x2 = 2.87, zmin = 11.88. 
    """
 
    '''
    print "\n", "=" * 60, "\n"  
 
    system = [
        ([0.3, 0.4, 0.6], '<=', 3360), 
        ([0.4, 0.4, 0.7], '<=', 2688), 
        ([0.5, 0.4, 0.8], '<=', 5040), 
        ([1, -2, 0], '=', 0),
        ([0, 3, -2], '=', 0),
        ([3, 0, -1], '=', 0), 
    ]
 
    print "system:", system
 
    A, I, B = zip(*system)
    Z = [2.5, 1.5, 2.2]
 
    simplex(_to_float(A), I, to_float(B), to_float(Z), look_max=True)
    '''
    print "\n", "=" * 60, "\n"
