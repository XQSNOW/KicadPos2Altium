#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
import os
import msvcrt

VERSION = '0.03'

print('KicadPos2Altium v%s' % VERSION)

files = os.listdir(os.path.curdir)
csv_files = list()
for v in files:
    if v[-3:].upper() == 'CSV':
        csv_files.append(v)

altium_headers = ['Designator', 'Footprint', 'Mid X', 'Mid Y', 'Ref X', 'Ref Y', 'Pad X', 'Pad Y', 'Layer', 'Rotation', 'Comment']
kicad_headers = ['Ref', 'Val', 'Package', 'PosX', 'PosY', 'Rot', 'Side']
headers = ['%c%s%c' % ('\"', v, '\"') for v in altium_headers]

target = ''
if len(csv_files) > 1:
    while True:
        print('选择要转换文件的序号')
        for v in range(len(csv_files)):
            print('%d: %s' % (v, csv_files[v]))
        i = 0
        try:
            i = int(input())
        except Exception as exc:
            print('输入不正确: %s' % str(exc))
        else:
            if i < len(csv_files):
                target = csv_files[i]
                break
            else:
                print('输入不正确: 序号超限了')
elif len(csv_files) == 1:
    target = csv_files[0]
else:
    print('请把需要转换的文件拷贝到当前目录下')

print('开始转换 %s' % target)

if target[-3:].upper() == 'CSV':
    with open(target) as f:
        f_csv = csv.reader(f)
        hd = next(f_csv)
        flag = False
        for v in range(len(altium_headers)):
            if altium_headers[v] != hd[v]:
                flag = True
                break

        if flag:
            new_f = list()
            new_f.append(headers)
            for row in f_csv:
                a = list()
                a.append('%c%s%c' % ('\"', row[0], '\"'))
                a.append('%c%s%c' % ('\"', row[2], '\"'))
                a.extend(['%c%smm%c' % ('\"', v, '\"') for v in row[3:5]])
                a.extend(['', '', '', ''])
                a.append('\"T\"' if row[6] == 'top' else '\"B\"')
                a.append('%c%s%c' % ('\"', row[5], '\"'))
                a.append('%c%s%c' % ('\"', row[1], '\"'))
                new_f.append(a)

            f_csv = open(target[:-4] + '_new.csv', 'w')
            for items in new_f:
                for item in items:
                    f_csv.write('%s,' % item)
                f_csv.write('\n')

            f_csv.close()
            print('转换完成')
        else:
            print('文件已经是转换过的')

print('按任意键退出')
print(msvcrt.getch())

