print("Практическая работа 1, Шахманова(разраб) и Михайлова(аналитик) БЦШ02-26-03")
print("Аварийная диагностика скважины (Вариант Б)\n")

# Номера по журналу
N1: int = 7
N2: int = 12
N: int = N1 + N2

# Индивидуальные входные данные
Q_LIQ: float = 40 + 4 * (N % 20)          # дебит жидкости, м^3/сут
W_PCT: float = 20 + 3 * (N % 28)          # обводнённость, %
P_RES: float = 22.0 + 0.5 * (N % 15)      # пластовое давление, МПа
P_BHP: float = 14.0 + 0.4 * (N % 18)      # забойное давление, МПа


W_CRITICAL: float = 85.0
W_EXTREME: float = 98.0  # Челлендж 2: экстренный порог обводнённости
DP_MIN_ACTIVE: float = 0.5
J_NORM_DEFAULT: float = 4.5 + 0.25 * (N % 12)  # норматив J_norm для нашей пары (N=19 -> 6.25)

def validate_telemetry(q_liq: float, w_pct: float, p_res: float, p_bhp: float) -> bool:
    """Проверяет, что все 4 датчика находятся в допустимых физических границах.

    Args:
        q_liq (float): Дебит жидкости (0..1000 м3/сут).
        w_pct (float): Обводнённость (0..100 %).
        p_res (float): Пластовое давление (5..60 МПа).
        p_bhp (float): Забойное давление (1..60 МПа).
    Returns:
        bool: True, если все показатели в норме, иначе False.
    """
    ...
def calc_hydraulics(q_liq: float, p_res: float, p_bhp: float) -> tuple[float, float]:
    """Считает депрессию dP = p_res - p_bhp и продуктивность J = q_liq / dP.
Если dP <= 0, то J принимается равным 0.0 (защита от деления на ноль).

    Args:
        q_liq (float): Дебит жидкости, м3/сут.
        p_res (float): Пластовое давление, МПа.
        p_bhp (float): Забойное давление, МПа.
    Returns:
        tuple[float, float]: Пара чисел (dP, J).
    """
    drawdown = p_res - p_bhp
    if drawdown <= 0:
        return drawdown, 0.0
    return drawdown, q_liq / drawdown
def determine_status_code(
    drawdown: float, w_pct: float, prod_index: float, j_norm: float = J_NORM_DEFAULT
) -> str:
    """Определяет код состояния скважины по приоритетной цепочке условий.
Порядок проверок (важен!):
        1. dP < 0                -> 'BLOWOUT'
        2. dP <= 0.5             -> 'IDLE'
иначе
        3. W >= 98.0             -> 'CRITICAL_WATER'  (новое правило заказчика)
        4. W >= 85.0             -> 'WATERED'
        5. J < J_norm            -> 'CLOGGED'
        6. 
                 -> 'NORMAL'

    Args:
        drawdown (float): Депрессия dP, МПа.
        w_pct (float): Обводнённость W, %.
        prod_index (float): Коэффициент продуктивности J.
        j_norm (float): Нормативный коэффициент J_norm.
    Returns:
        str: 
Код состояния ('BLOWOUT', 'IDLE', 'CRITICAL_WATER', 'WATERED',
        'CLOGGED' или 'NORMAL').
    """
    if drawdown < 0.0:
        return "BLOWOUT"
    elif drawdown <= DP_MIN_ACTIVE:
        return "IDLE"
    elif w_pct >= W_EXTREME:
        return "CRITICAL_WATER"
    elif w_pct >= W_CRITICAL:
        return "WATERED"
    elif prod_index < j_norm:
        return "CLOGGED"
    else:
        return "NORMAL"
    
def route_dispatcher_action(status_code: str) -> str:
    """Переводит код состояния в текстовую команду диспетчеру через match-case.

    Args:
        status_code (str): Код состояния скважины.
    Returns:
        str: 
    """
    ...

# Смена ролей
if __name__ == "__main__":

    # Основной расчёт для индивидуальных данных пары 
    my_dp, my_j = calc_hydraulics(Q_LIQ, P_RES, P_BHP)
    my_w = W_PCT
    code = determine_status_code(my_dp, my_w, my_j)
    print(f"N = {N1} + {N2} = {N}")
    print(f"Qж={Q_LIQ} м3/сут, W={W_PCT}%, Pпл={P_RES} МПа, Pзаб={P_BHP} МПа, J_norm={J_NORM_DEFAULT}")
    print(f"Вход: dP={my_dp:.2f}, W={my_w}%, J={my_j:.2f} -> Код: {code}")

    # Проверка Челленджа 2 и остальных веток 
    print("Тесты веток")
    print("W=98.0  ->", determine_status_code(my_dp, 98.0, my_j))   # CRITICAL_WATER
    print("W=99.5  ->", determine_status_code(my_dp, 99.5, my_j))   # CRITICAL_WATER
    print("W=90.0  ->", determine_status_code(my_dp, 90.0, my_j))   # WATERED
    print("dP=-1.0 ->", determine_status_code(-1.0, 50.0, 0.0))     # BLOWOUT
    print("dP=0.3  ->", determine_status_code(0.3, 50.0, 10.0))     # IDLE
    print("J=3.0   ->", determine_status_code(my_dp, my_w, 3.0))    # CLOGGED
    print("dP=0, Qж=116 ->", calc_hydraulics(116.0, 20.0, 20.0))    # (0.0, 0.0)

    # Челлендж 1: встроенная справка (выход из справки — клавиша Q)
    help(calc_hydraulics)