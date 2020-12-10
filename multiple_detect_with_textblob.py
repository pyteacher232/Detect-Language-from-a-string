import csv
import xlrd
import threading
from iso639 import languages
from textblob import TextBlob
import random
import nltk
import time

proxy_file_name = 'proxy_http_ip.txt'
PROXIES = []
with open(proxy_file_name, 'rb') as text:
    PROXIES = ["http://" + x.decode("utf-8").strip() for x in text.readlines()]

csv_writer = csv.writer(open("Result/udemy_list_complete.csv", "w", encoding='utf-8-sig', newline=''))

input_dt = []
input_fname = 'Result/udemy_list.xlsx'
input_xls = xlrd.open_workbook(input_fname)
sheet = input_xls.sheet_by_index(0)
for row_index in range(0, sheet.nrows):
    row = [sheet.cell(row_index, col_index).value for col_index in range(sheet.ncols)]
    input_dt.append(row)

input_dt.reverse()
title = input_dt.pop()
csv_writer.writerow(title)

print("Input data is loaded successfully.")

cnt = 0

def detect_lang():
    global input_dt
    global cnt
    global csv_writer

    row = input_dt.pop()
    title = row[4]
    about = row[5]
    try:
        pxy = random.choice(PROXIES)
        nltk.set_proxy(pxy)
        language = languages.get(alpha2=TextBlob(title + ' ' + about).detect_language()).name
    except:
        input_dt = [row] + input_dt
        return

    row[10] = language

    csv_writer.writerow(row)
    cnt += 1
    print(f"[Result {cnt}] {row}")

threads = []
max_threads = 100

while threads or input_dt:
    for thread in threads:
        if not thread.is_alive():
            threads.remove(thread)

    while len(threads) < max_threads and input_dt:
        thread = threading.Thread(target=detect_lang)
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)
