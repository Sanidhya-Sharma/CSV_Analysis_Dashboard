#IMPORTING REQUIREMENTS
from flask import Flask
from flask import render_template
import pandas as pd
import numpy as np
from flask import request
from flask import redirect
from flask import url_for
import os
import time


import FileWatch
from FileWatch import watch_file
import AnalysisHelper

#ASSINGNING APP AS__NAME_ FOR CALLING TO MAIN
app = Flask(__name__)

#DEFAULT ROUTING
@app.route('/')

#ROUTING TO HOME
@app.route('/Home')
def Home():
    print('Home')
    return render_template('Home.html')

#ROUTING TO WAW
@app.route('/WAW')
def WAW():
    print('Who are we')
    return render_template('WAW.html')

#ROUTING TO IDA
@app.route('/IDA', methods=['GET', 'POST'])
def IDA():
    print('IDA')
    return render_template('IDA.html')


#ROUTING TO IDA PHASE 1
@app.route('/IDA_P1')
def IDA_P1():
    print('IDA_P1')
# ---------------------------------------------------------FILE SCREENING-----------------------------------------------
# FILENAME
    filename = os.path.join(os.getcwd(), "source\Sample.csv")

# CHECKING THE FILE
    Check_Availability = FileWatch.watch_file(filename)

    if Check_Availability == True:
        print("File Found")
        data = pd.read_csv(filename, sep=',', dtype={}, na_values=['.', '??'])

    else:
        print("File not Found")
        return render_template('Error.html')

# ------------------------------------------------------------HELPER CLASS----------------------------------------------
    # GETTING HERLPER CLASS
    class_helper = AnalysisHelper.Helper(data)

    acol = class_helper.analyze_columns()
    acor = class_helper.analyze_correlations()
    null_case = class_helper.analyze_null_causes()
    apply_advices = class_helper.apply_advices()
    get_advices = class_helper.get_advices()

    # GETTING COLUMN INFO CLASS
    no_class = AnalysisHelper.ColumnInfos

    # data = no_class.has_advice(self)

    ##    # GETTING METHORDS
    ##    class_columninfo = AnalysisHelper.format_col_infos()

# --------------------------------------------------------CORRELATION DATA----------------------------------------------
    import re

    print("###############My code#################")
    # print(acor)

    output = {}
    i = 0
    j = 0

    num = re.sub(r'have|a|.and|"', "", acor)
    numsplit = num.splitlines()

    length = num.count('\n')

    # print(length)

    for element in numsplit:
        try:
            output[str(i)] = {}
            split_element = element.split("   ")
            first_split = split_element[0].split(" ")
            second_split = split_element[1].split(":")

            for item in second_split:
                first_split.append(item.strip())

            for item in first_split:
                # FILTERING
                if not "-" in str(first_split[3]):
                    output[str(i)][str(j)] = item
                    j += 1
            j = 0
            i += 1

        except Exception as e:
            print("LOG :", str(e))

    # PRINTING ALL THE VALUES
    #    for key in output:
    #        print(output[key]["3"])

    # PRINTING DEDICATED VALUES
    # print(output)
    # print(output["0"]["0"])
    # print(output["0"]["1"])

    ##    for i,j in output:
    ##        out = output ["i"]["j"]

# ------------------------------------------------------COLUMN INFO-----------------------------------------------------
    import re

    # ASSIGNING THE COLUMN VALUES TO VARIABLE ACOL
    columninfo = acol

    col = []
    typeof = []
    nullval = []
    uniqueval = []
    someval = []

    # CLEANING VALUES FROM ACOL DATA
    filter_0 = columninfo.split("\n")

    i = 0
    for items in filter_0:

        if "of type" in items:
            filter_2 = items.replace('of type', '').replace("..", "").replace(str(i) + ":", "")

            filter_3 = filter_2.replace('"', '').replace('and', '').replace('\n', '').replace('values', '')

            filter_4 = re.sub(r'\s+', ' ', filter_3, flags=re.I).replace('\x1b', ' ').replace('[1;31;47m', ' ').replace(
                '[1;32;47m', ' ').replace('[1;33;47m', ' ').replace("[0m", " ")

            filter_5 = filter_4.replace("  ", "").replace(".", "").strip().split(" ")

            col.append(filter_5[0::800])
            typeof.append(filter_5[1::800])
            nullval.append(filter_5[2::800])
            uniqueval.append(filter_5[4::800])
            someval.append(filter_5[6::])

            i += 1

    # PRINTING OUTPUT FROM ACOL
    print(filter_0)
    print(col)
    print(typeof)
    print(nullval)
    print(uniqueval)
    print(someval)


    # FLATTENING 2D LIST TO 1D LIST (COLUMNINFO)
    from itertools import chain
    flatten_list_null = list(chain.from_iterable(nullval))
    flatten_list_uniq = list(chain.from_iterable(uniqueval))
    flatten_list_typeof = list(chain.from_iterable(typeof))
    flatten_list_someval = list(chain.from_iterable(someval))

    # UNIQUE VS NULL BAR GRAPH VALUES
    null_val = flatten_list_null
    unique_val = flatten_list_uniq
    # someval_val = flatten_list_someval
    # #print(someval_val)

    # DATATYPE PIE CHART
    df_2 = pd.DataFrame(flatten_list_typeof)
    df_3 = df_2.set_axis(['DataType'], axis=1, inplace=False)
    df_4 = df_3['DataType'].value_counts()

    df_dtype = df_4.index.to_list()
    df_dtype_count = list(df_4.values)

    # Converting int, Strings, objects to simple words
    dtype_simplify_1 = [sub.replace('int64', 'Numbers') for sub in df_dtype]
    dtype_simplify_2 = [sub.replace('object', 'Words') for sub in dtype_simplify_1]
    dtype_simplify_3 = [sub.replace('float64', 'Decimals') for sub in dtype_simplify_2]
    df_dtype_word = dtype_simplify_3

    #Taking percentage of the simple words
    df_type_sum = sum(df_dtype_count)
    df_dtype_count_percentage = (df_dtype_count/df_type_sum)*100

    # df_datatypes_filter1 = df_4.replace("int64", "Numbers").replace("object", "Words").replace("float64", "Decimals")
    #
    #
    # print(df_datatypes_simple)

    item_1 = []
    item_2 = []


    # for df_val in df_6:
    #     item_1.append(df_val[0])
    #     item_2.append(df_val[1])
    # print(item_1)
    # print(item_2)

# ----------------------------------------------OVERVIEW & NULL VALUES GRAPH--------------------------------------------

    # OVERVIEW & FIRST CHART FOR UNIQUE VALUES
    numOfRows = data.shape[0]                                      #Total no of Rows
    numofColumns = data.shape[1]                                   #Total no of Columns
    datauni = (numOfRows - data.nunique(0)).reset_index()          #Total no of Unique rows
    nulldata = data.isnull().sum().sum()                           #Total no of null values
    uniqsum = sum(map(int, unique_val))                            #Total no of unique values

    # BAR GRAPH FOR DUPLICATES
    row_0 = []
    row_1 = []

    for rows in datauni.values:
        row_0.append(str(rows[0]))
        row_1.append(rows[1])

    val = row_1
    lab = row_0
    legend = 'No of Duplicates Values'

    duplicsum = sum(map(int, row_1))                              #Total no of duplicate values

    # RETURNING VALUES TO THE FLASK TEMPLATES
    return render_template('IDA_P1.html', values=val,
                                          labels=lab,
                                          legend=legend,
                                          colcount=numofColumns,
                                          rowcount=numOfRows,
                                          nullcount=nulldata,
                                          total_uniq=uniqsum,
                                          duplic_total=duplicsum,
                                          null_graphdata=null_val,
                                          uniq_graphdata=unique_val,
                                          dtype_pie_lable=df_dtype_word,
                                          dtype_pie_value=df_dtype_count_percentage)


#MAIN CALL FUNCTION CALLING FLASK =_NAME_
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
