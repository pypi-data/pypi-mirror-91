import os 
import pandas as pd
import json
import matplotlib.pyplot as plt
import csv

# coverting csv file json file 
def csv_json(i):
    df = pd.read_csv(i)
    result = df.to_json(orient="index")
    parsed = json.loads(result)
    
    # Serializing json  
    json_object = json.dumps(parsed, indent = 4) 
  
    return(json_object)

    
# Data summary
def data_summary(j):
    df = pd.read_csv(j)
    fig, axes = plt.subplots(nrows=2, ncols=3 , figsize=(15,15))

    df['geo_country'].value_counts()[1:20].plot(ax=axes[0,0],title = "country",kind = "barh",color = "red")
    df['geo_region'].value_counts()[1:20].plot(ax=axes[0,1],title = "region", kind = "bar",color = "blue")
    df['geo_city'].value_counts()[1:20].plot(ax=axes[1,0],title = "city", kind = "bar")
    df['sku'].value_counts().plot(ax=axes[1,1],title = "sku",kind ="pie")
    df['is_limited_ad_tracking'].value_counts().plot(ax=axes[0,2],title = "is_limited_ad_tracking",kind = "pie")
    df['device_language'].value_counts()[1:20].plot(ax=axes[1,2],title = "language", kind = "barh",color = "violet")
    plt.show()

    
    
    # Generating insert into statements 
def sql_insert(p):
    file = open(p, 'r',encoding="utf8")
    read = csv.reader(file)
    header_list = next(read)
    headers_list = map((lambda q: '"'+q+'"'), header_list)
    insert_list = 'INSERT INTO Table (' + ", ".join(headers_list) + ") VALUES "
    l = []
    for row in read:
        val = map((lambda q: "'"+q+"'"), row)
        l.append(str(insert_list +"("+ ",".join(val) +");"))
    r = '\n'.join(l)
    file.close()
    return(r)   
        