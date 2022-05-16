from prometheus_pandas import query
import os
import re
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
from datetime import timedelta
from prometheus_pandas import query as pp
import runipy
import requests
import json
import time
ANAPLANTOKEN='AnaplanAuthToken ivFEST1VWhaf6/UhPaomjA==.Q3LNhGlWoEdrhPZE90jJ2OxFuKn9YMpye/seb5SXnwKjR7hlSyZMIyGOB7eCrI2ojpZ25c7XIKZctJupZl29Q6W7JbmVAZ+scZKqMf1sAwAm1+HLcpgTLyqYo7S0LKGKbdT9AhFezLYctBhX52/k5Ok3xZrHT2dHSbRgcXm+stXW1gVuMhWSDsmWtvoFusMaN6DN+TR9oP+wy6qqHVuc8IE319vBNdLQpASchOveYHmBIGqjETN9X9IkkZRkzqYj7ixXWcmmf5QAncitVnaQkf7JQ82H/CG8sbR+ORLx69HD/wPGs+8X6JNBr9E2yFHAAUI6QMK36XDcIWbkmBQQqYvDiHyvz/4uPJ/ttPqptdYmcF4xWrezMpRaXTygXvJCi6ZhndwSbQIsbZdd43R9IC0k8F9xX83pObHCUajVRxFphswd/5xEWFAi6OKtwYDQq5dXhWk7M+4ZVu1LwHpwpfZJSVllJmvnIxuoTXnx+CqErthRMhbK6CzhBsmqkvR4.90Bu20wlZHjqMEH64LFpk+ssmNfLoHZgRtbfBndma1M='


def anaplanstart():
    # получение времени запуска для отслеживания метрик
    d = datetime.now()
    starttime = d.strftime("%Y-%m-%dT%H:%M:%SZ")

    # процессы построены, необходимо только его начать
    url = "https://api.anaplan.com/2/0/workspaces/8a868cdc794dca060179fbc4d8767f99/models/C06EDFD7EE20468EB0344F4ECD159E90/processes/118000000001/tasks"
    headers = {'authorization': ANAPLANTOKEN, 'Content-Type': 'application/json'}
    payload = '{"localeName": "en_US"}'
    r = requests.post(url, data=payload, headers=headers)
    data = r.json()
    print(data)
    print(r)

    # получение времени окончания для отслеживания метрик
    d = datetime.now()
    stoptime = d.strftime("%Y-%m-%dT%H:%M:%SZ")
    return starttime, stoptime

def promquery(starttime, stoptime):
    # задержка, для того чтобы node exporter успел собрать метрики
    time.sleep(5)
    p = query.Prometheus('http://localhost:8428')
    # требуется проверка времени, тк часовые пояса иногда слетают - лучше вывести за день

    ############ПРОЦЕССОР############
    cpu = p.query_range(
        'sum(rate(node_cpu_seconds_total[5m]))',
        starttime, stoptime, '1s')
    print(cpu.to_string())
    with open("metrics_cpu.txt", "w") as metrics:
        print(cpu.to_string(), file=metrics)
        metrics.close()

    ###########ОЗУ############
    ram = p.query_range(
        'sum(rate(node_memory_MemTotal_bytes[5m]))',
        starttime, stoptime, '1s')
    print(ram.to_string())
    with open("metrics_ram.txt", "w") as metrics:
        print(ram.to_string(), file=metrics)
        metrics.close()

    ############СЕТЬ############
    ram = p.query_range(
        'sum(node_network_receive_bytes_total)',
        starttime, stoptime, '1s')
    print(ram.to_string())
    with open("metrics_network.txt", "w") as metrics:
        print(ram.to_string(), file=metrics)
        metrics.close()


def jupyterstart():
    # получение времени начала запуска
    url = "http://127.0.0.1:9228/starttime"
    r = requests.get(url)
    data = r.json()
    resultstart = (data["text/plain"].replace("'", ""))

    # запуск скрипта по блокам
    for i in range(19):
        url = "http://127.0.0.1:9228/run%s" % i
        # print(url)
        r = requests.get(url)

    # получение времени конца запуска
    url = "http://127.0.0.1:9228/stoptime"
    r = requests.get(url)
    data = r.json()
    resultstop = (data["text/plain"].replace("'", ""))

    # рабочий курл
    #curl http://localhost:8888/api/contents -H "Authorization: token f4e4170fc9dcae27e1b26aab49492c55e6089ed6fc5ea7da"
    return resultstart, resultstop

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # запрос анаплан
    timetuple = anaplanstart()
    print("Сбор метрик проводится за время работы Anaplan:")
    print(timetuple[0], timetuple[1])
    # статистика
    # promquery(timetuple[0], timetuple[1])

    # запрос на юпитер
    # timetuple = jupyterstart()
    # print("Сбор метрик проводится за время работы Jupyter Notebook:")
    # print(timetuple[0], timetuple[1])
    # статистика
    # promquery(timetuple[0], timetuple[1])

    # создание временного ряда
