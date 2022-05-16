from prometheus_pandas import query
import os
import re
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from datetime import timedelta
from prometheus_pandas import query as pp
import runipy
import requests
import json
import time
ANAPLANTOKEN='AnaplanAuthToken YFZ6AzF8yPX98LhrMPR/ag==.vgOotD0RB7sHql+n3qlMY67DSuUDbkw1AaVHHZqu/h1k+RYJzAaC2sKVk6xeeIbGoc3kCAAeQPU+VgrgaaFyNUhHPO+pSBvYmDDcVjBdpGsDH+qZVOAkMPGFTfjfmBMAsS/b1HZUpE+9F1ICLwKdhjfgogrIhEz993+MizGU78PR601DOSGLHH3OHjZwM/GY240CMKWFoeIgBgFvn2ymSJddwrELhef158LMtZeSRqDdt3wiT6sP+9aQdQlqlyuD7GMeusFxyrvKeC4M77jeG0ImG/jPgFaQxCmQNvrNf0th3FnR0zwYxFRdwR4DbCTuqx3h5MZyIgdccLqQ/yE9tr3JddlLIA/BGB8Jyy3E3tq59eVxVAMEkYlIOiWeXysRBpW+SEp51LrWrDtoy5ZXe8dtWzmCNXTXQaJWYRDDyOitHbblDz0f76SAhKhpuWn8lC1DSCq1C1aNW4VBVtv5jsSXav0KqfbHeoFuLH3/DDAuaOTTXBaV3vMd2fvqtEzi.mD8PLInzazwHsOtJpNXb1L+KnSIfyFMrpQqsTKs34X8='


def anaplanstart():
    # получение времени запуска для отслеживания метрик
    d = datetime.now() - timedelta(hours=3)
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
    d = datetime.now() - timedelta(hours=3) + timedelta(seconds=10)
    stoptime = d.strftime("%Y-%m-%dT%H:%M:%SZ")
    return starttime, stoptime


def promquery(starttime, stoptime, stringtemp):
    # задержка, для того чтобы node exporter успел собрать метрики
    time.sleep(5)
    p = query.Prometheus('http://localhost:8428')
    # требуется проверка времени, тк часовые пояса иногда слетают - лучше вывести за день

    ############ПРОЦЕССОР############
    cpu = p.query_range(
        'sum(rate(node_cpu_seconds_total[5m]))',
        starttime, stoptime, '0.5s')
    print(cpu.to_string())
    with open(stringtemp + "metrics_cpu.txt", "w") as metrics:
        print(cpu.to_string(), file=metrics)
        metrics.close()

    ###########ОЗУ############
    ram = p.query_range(
        'node_memory_MemTotal_bytes{job="node_exporter_metrics"} - node_memory_MemFree_bytes{job="node_exporter_metrics"} - (node_memory_Cached_bytes{job="node_exporter_metrics"} + node_memory_Buffers_bytes{job="node_exporter_metrics"})',
        starttime, stoptime, '0.5s')
    print(ram.to_string())
    with open(stringtemp + "metrics_ram.txt", "w") as metrics:
        print(ram.to_string(), file=metrics)
        metrics.close()

    ############СЕТЬ############
    ram = p.query_range(
        'sum(node_network_receive_bytes_total)',
        starttime, stoptime, '0.5s')
    print(ram.to_string())
    with open(stringtemp + "metrics_network.txt", "w") as metrics:
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
    promquery(timetuple[0], timetuple[1], "anaplan")

    # запрос на юпитер
    timetuple = jupyterstart()
    print("Сбор метрик проводится за время работы Jupyter Notebook:")
    print(timetuple[0], timetuple[1])
    # статистика
    promquery(timetuple[0], timetuple[1], "juputer")
    #done

    # создание временного ряда
