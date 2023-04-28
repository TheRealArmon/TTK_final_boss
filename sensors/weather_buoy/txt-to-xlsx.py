# Copies data from txt file to xlsx file
# TXT FILE IS MISSING PERIOD COLUMN ._.
import xlsxwriter as xls

workbook = xls.Workbook('textData.xlsx')
worksheet = workbook.add_worksheet()

with open('rawSeawatchExp22.txt', 'r') as text_file:
    lines = text_file.readlines()
    for row, line in enumerate(lines):
        for col, data in enumerate(line.split(";")):
            worksheet.write(row, col, data)
    
    text_file.close()
workbook.close()