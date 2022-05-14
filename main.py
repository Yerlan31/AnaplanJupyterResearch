from prometheus_pandas import query
import os
import re
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime as dt
from datetime import timedelta
from prometheus_pandas import query as pp
import runipy
import requests
import json


def promquery(name):
    p = query.Prometheus('http://localhost:8428')
    # требуется проверка времени, тк часовые пояса иногда слетают - лучше вывести за день

    ############ПРОЦЕССОР############
     # cpu = p.query_range(
        # 'sum(rate(node_cpu_seconds_total[5m]))',
        # '2022-05-13T19:27:00Z', '2022-05-15T23:45:00Z', '1m')
    # print(cpu.to_string())
    # with open("metrics_cpu.txt", "w") as metrics:
    #     print(cpu.to_string(), file=metrics)
    #     metrics.close()
    ############ОЗУ############
    # ram = p.query_range(
    #     'sum(rate(node_memory_MemTotal_bytes[5m]))',
    #     '2022-05-13T19:27:00Z', '2022-05-15T23:45:00Z', '1m')
    # print(ram.to_string())
    # with open("metrics_ram.txt", "w") as metrics:
    #     print(ram.to_string(), file=metrics)
    #     metrics.close()
    ############СЕТЬ############
    ram = p.query_range(
        'sum(node_network_receive_bytes_total)',
        '2022-05-14T01:01:14Z', '2022-05-15T01:01:14Z', '1m')
    print(ram.to_string())
    with open("metrics_network.txt", "w") as metrics:
        print(ram.to_string(), file=metrics)
        metrics.close()


def jupyterstart():
    # получение времени начала запуска
    url = "http://127.0.0.1:9228/starttime"
    r = requests.get(url)
    data = r.json()
    # jsonData = json.loads(data)
    # print(jsonData["'text/plain'"])
    resultstart = (data["text/plain"])

    # получение времени конца запуска
    url = "http://127.0.0.1:9228/stoptime"
    r = requests.get(url)
    data = r.json()
    resultstop = (data["text/plain"])

    # рабочий курл
    #curl http://localhost:8888/api/contents -H "Authorization: token f4e4170fc9dcae27e1b26aab49492c55e6089ed6fc5ea7da"
    return resultstart, resultstop

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # запрос на создание в анаплане

    # статистика
    # promquery('PyCharm')

    # вручную запускаем ноутбук - запрос на получение время работы ноутбука
    timetuple = jupyterstart()
    # статистика
    # promquery('PyCharm')
    # создание временного ряда
