"""
Predictive Gas Oracle — предсказание оптимального времени для отправки транзакций в Ethereum с минимальными комиссиями.

Инструмент использует историю изменения газа, чтобы предсказать благоприятное "окно" для отправки.
"""

import requests
import datetime
import statistics


def fetch_gas_data():
    url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
    response = requests.get(url).json()
    result = response.get("result", {})
    safe = int(result.get("SafeGasPrice", 0))
    propose = int(result.get("ProposeGasPrice", 0))
    fast = int(result.get("FastGasPrice", 0))
    return safe, propose, fast


def predict_gas_window(history):
    avg = statistics.mean(history)
    stddev = statistics.stdev(history) if len(history) > 1 else 0
    threshold = avg - stddev
    low_points = [i for i, g in enumerate(history) if g < threshold]
    if not low_points:
        return "Нет явного окна с низким газом. Рекомендуем ждать."

    index = low_points[0]
    time = datetime.datetime.utcnow() - datetime.timedelta(minutes=len(history) - index)
    return f"Следующее вероятное 'низкое' окно начнётся примерно в: {time.strftime('%Y-%m-%d %H:%M:%S')} UTC"


def main():
    print("[•] Собираем данные о цене газа за последние 30 минут...")
    history = []
    for _ in range(30):
        safe, _, _ = fetch_gas_data()
        history.append(safe)

    recommendation = predict_gas_window(history)
    print("[✓] Анализ завершён.")
    print("Рекомендация:", recommendation)


if __name__ == "__main__":
    main()
