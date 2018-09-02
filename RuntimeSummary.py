import re
import json
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

def show_summary():
    count = 0
    error = 0
    total = 0

    infos = []

    with open('opentuner.log', 'r') as f:
        for line in f:
            if 'INFO' in line:
                infos.append(line.split("    "))
                # print info
                total += 1


            elif 'WARNING' in line:
                # print "E: " + str(error) + " " +  line
                error += 1
            count += 1


    # print infos[0]

    # find how many columns
    match_config = re.search('\{(.*?)\}', infos[0][1])
    test_conf_json = json.loads(infos[0][1][match_config.start(): match_config.end()])
    # print test_conf_json

    test_conf = ast.literal_eval(json.dumps(test_conf_json))
    # print test_conf

    columns = test_conf.keys()


    df = pd.DataFrame(columns=columns)
    row = 1

    for info in infos:
        match_config = re.search('\{(.*?)\}', info[1])
        test_conf_json = json.loads(info[1][match_config.start(): match_config.end()])
        test_conf = ast.literal_eval(json.dumps(test_conf_json))

        # print test_result
        # print type(test_result)

        match_config = re.search('cost time=(.*?)\,', info[1])
        test_time = info[1][match_config.start() + 10 : match_config.end() - 1]
        # print test_time
        test_conf["test_time"] = float(test_time)

        for key in test_conf:
            df.loc[row, key] = test_conf[key]
        row += 1


    # print df.head()
    # print df.info()

    # print df._get_numeric_data().columns.values.tolist()[:-1]
    # print df['test_time']
    # print df.head(30)

    num_col = df._get_numeric_data().columns.values.tolist()[:-1]
    str_col = list(filter(lambda x: x not in num_col, columns))
    lb = []
    lb.append('empty')

    # print "str "
    # print str_col
    # print df[str_col[0]]

    for i in num_col:
        graph_name = "graph_" + i
        plt.plot(df['test_time'], df[str(i)])
        plt.gca().invert_xaxis()
        plt.title("Parameter: " + i)
        plt.xlabel("Time (s)")
        plt.ylabel("Configuration of " + i)

        plt.savefig("img/" + graph_name, dpi = 50)
        plt.figure().clear()


    fig, ax = plt.subplots()

    row = 1

    for item in str_col:
        dot_color = []
        dot_label = []
        flag = df[item].tolist()
        x = df['test_time'].tolist()
        y = [item] * len(x)

        # print flag


        for i in range(len(y)):
            if flag[i] == 'on':
                dot_color.append('red')
                dot_label.append('on')
            elif flag[i] == 'off':
                dot_color.append('green')
                dot_label.append('off')
            elif flag[i] == 'default':
                dot_color.append('yellow')
                dot_label.append('default')
            else:
                dot_color.append('write')
                dot_label.append('empty')
        # print dot_color
        ax.scatter(x, y, c = dot_color)

        # print(item)
        lb.append(item)
        ax.grid(True)


    '''
    for i in str_col:
        ax.scatter(df['test_time'], df[i], label=i)
    '''
    # print lb
    olb = np.arange(0, len(columns) + 1, 1)
    # ax.set_yticks(olb, lb)

    plt.gca().invert_xaxis()
    rcParams.update({'figure.autolayout': True})

    # plt.tight_layout()
    plt.yticks(rotation = 60)
    plt.title('Enumerate/boolean parameters')
    fig.subplots_adjust(left = 0.25)
    fig.subplots_adjust()
    plt.xlabel("Time (s)")
    plt.ylabel("Parameters")
    plt.gcf().text(0.85, 1, 'On - Red\n Off - Green\n Default - Yellow', fontsize=10)
    plt.savefig("img/" + 'graph_enumerate_or_boolean_parameters', dpi = 50)


    print "count " + str(count)
    print "total " + str(total)
    print "error " + str(error)

