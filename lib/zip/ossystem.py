import os
import subprocess

text = r".\7-Zip64\7z.exe x -aoa  .\7-Zip64\Setup1.zip -o.\7-Zip64\ -pbear01"

result = os.system(text) #雖然在終端中輸出了結果，那是os.system()執行的時候在終端自動輸出的結果。但是print cmd_out_info並沒有輸出相關的信息，而且程序進入了busybox的環境中無法退出。



p = subprocess.Popen(text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# result = p.stdout.readlines() #或者outinfo = p.stdout.read()


print(result)