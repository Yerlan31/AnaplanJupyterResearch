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
from IPython.display import HTML, Javascript, display


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
        '2022-05-13T19:27:00Z', '2022-05-15T23:45:00Z', '1m')
    print(ram.to_string())
    with open("metrics_network.txt", "w") as metrics:
        print(ram.to_string(), file=metrics)
        metrics.close()


def jupyterstart():
    url = "http://maps.googleapis.com/maps/api/geocode/json"
    location = "delhi technological university"
    params = {'address': location}
    r = requests.post(url, params)
    data = r.json()
    temp = r.json
    print(data)
    print(temp)
    # runipy jup_graph.ipynb
    # curl - i - X
    # POST - H
    # "X-AUTH-TOKEN: $AUTH_TOKEN" - H
    # "Content-Type: application/json" - H
    # "Accept: application/json" \
    # - d
    # '{"path":"Users/abc@xyz.com/note1.ipynb", "command_type":"JupyterNotebookCommand",  "label":"spark-cluster-1", "arguments": {"name":"xyz", "age":"20"}}' \
    # "https://api.qubole.com/api/v1.2/commands"

    # рабочий курл
    #curl http://localhost:8888/api/contents -H "Authorization: token f4e4170fc9dcae27e1b26aab49492c55e6089ed6fc5ea7da"

def restart_kernel_and_run_all_cells():
    display(HTML(
        '''
            <script>
                code_show = false;
                function restart_run_all(){
                    IPython.notebook.kernel.restart();
                    setTimeout(function(){
                        IPython.notebook.execute_all_cells();
                    }, 10000)
                }
                function code_toggle() {
                    if (code_show) {
                        $('div.input').hide(200);
                    } else {
                        $('div.input').show(200);
                    }
                    code_show = !code_show
                }
                code_toggle() 
                restart_run_all()
            </script>

        '''
    )
    )



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # запрос на создание в анаплане

    # статистика
    promquery('PyCharm')
    # запрос на создание в юпитере
    #jupyterstart()

    #restart_kernel_and_run_all_cells()
    # статистика
    # promquery('PyCharm')
    # создание временного ряда
