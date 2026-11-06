"""Этап 1 (Вариант А): Моделирование карточки скважины, сохранение и чтение JSON.
 
Индивидуальные числа пары: N = N1 + N2 = 7 + 12 = 19.
"""
import json
from typing import Any
 
N1: int = 7   # номер по журналу: Михайлова Александра (Системный аналитик)
N2: int = 12  # номер по журналу: Шахманова Самира (Разработчик)
N: int = N1 + N2
 
 
def build_well_passport() -> dict[str, Any]:
    """Создаёт словарь паспорта скважины с индивидуальными данными пары.
 
    Формулы варианта А (N = 19):
        well_id  = "W-" + (100 + N)         -> "W-119"
        depth_m  = 1500 + 50 * (N % 40)     -> 2450
        q_liq    = 45.0 + 3.5 * (N % 30)    -> 111.5
        w_pct    = 12.0 + 2.0 * (N % 35)    -> 50.0
        power_kw = 40.0 + 5.0 * (N % 20)    -> 135.0
    """
    return {
        "well_id": f"W-{100 + N}",
        "field_name": "Приобское",  # Челлендж № 1: новое поле заказчика
        "depth_m": 1500 + 50 * (N % 40),
        "q_liq": 45.0 + 3.5 * (N % 30),
        "w_pct": 12.0 + 2.0 * (N % 35),
        "is_active": True,
        "pump": {
            "model": "ЭЦН5-80-1800",
            "power_kw": 40.0 + 5.0 * (N % 20),
        },
    }
 
 
def save_to_json(data: dict[str, Any], filename: str = "data.json") -> None:
    """Сериализует словарь Python в текстовый файл формата JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
 
 
def load_from_json(filename: str = "data.json") -> dict[str, Any]:
    """Десериализует (читает) JSON-файл с диска обратно в словарь Python."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
 
 
def print_passport_summary(passport: dict[str, Any]) -> None:
    """Выводит сводку по прочитанному из JSON паспорту и считает дебит чистой нефти."""
    q_oil = passport["q_liq"] * (1.0 - passport["w_pct"] / 100.0)
    pump_info = passport["pump"]
    print("=" * 56)
    print(f"ПАСПОРТ СКВАЖИНЫ ИЗ JSON: {passport['well_id']}")
    print("=" * 56)
    print(f"Месторождение: {passport['field_name']}")
    print(f"Глубина: {passport['depth_m']} м")
    print(f"Дебит жидкости: {passport['q_liq']:.2f} м3/сут (обводнённость {passport['w_pct']:.1f}%)")
    print(f"Расчёт чистой нефти: {q_oil:.2f} м3/сут")
    print(f"Насосная установка: {pump_info['model']} (мощность {pump_info['power_kw']} кВт)")
    print("=" * 56)
 
 
if __name__ == "__main__":
    # 1. Формируем словарь в памяти Python
    my_passport = build_well_passport()
 
    # 2. Сохраняем его в файл data.json (сериализация)
    save_to_json(my_passport, "data.json")
    print("[OK] Файл 'data.json' успешно записан на диск!")
 
    # 3. Читаем файл обратно с диска (десериализация) и проверяем, что данные не потерялись
    loaded_passport = load_from_json("data.json")
    assert loaded_passport == my_passport, "Ошибка: прочитанный словарь не совпадает с исходным!"
    print("[OK] Обратное чтение через json.load() прошло без потерь!\n")
 
    # 4. Печатаем инженерную сводку по прочитанным данным
    print_passport_summary(loaded_passport)
 