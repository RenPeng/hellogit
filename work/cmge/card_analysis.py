#!/usr/bin/env python
# -*- coding=utf-8 -*-

from data_map import area_map,card_map
import xlwt

all_area_key = sorted(area_map.keys())
card_keys = sorted(card_map.keys())
ignore_area = [1,2,1003,18]
area_keys = []

for key in all_area_key:
    if key in ignore_area:
        pass
    else:
        area_keys.append(key)

def generate_dict():
    tmp_dict = {}
    for ak in area_keys:
        tmp_dict[ak] = {'1张':0,'2张':0,'3张':0}
    return tmp_dict
def write_xls_title():
    xls.write(0,0,'名臣')
    xls.write(0,1,'ID')
    xls.write(0,2,'总人数')
    card_dict = generate_dict()
    title_c = 3
    for area in area_keys:
        for card_num in sorted(card_dict[area].keys()):
            xls.write(0,title_c,area_map[area]+':'+card_num)
            title_c += 1
def calc_card(card_id,card_row):
    card_dict = generate_dict()
    user_data = '/data/tmpdir/wh_100_user_info_20140716.txt'
    user_data_handler = open(user_data)
    EOF = True
    total = 0
    while EOF:
        EOF = user_data_handler.readline()
        row = EOF.split('\t')
        if len(row) < 16:
            pass
        else:
            area = int(row[2])
            officer = row[13]
            if area not in area_keys:
                pass
            else:
                if str(card_id) in officer:
                    total += 1
                if str(card_id)+',1' in officer:
                    card_dict[area]['1张'] += 1
                if str(card_id)+',2' in officer:
                    card_dict[area]['2张'] += 1
                if str(card_id)+',3' in officer:
                    card_dict[area]['3张'] += 1
    xls.write(card_row,0,card_map[card_id])
    xls.write(card_row,1,card_id)
    xls.write(card_row,2,total)
    card_c = 3
    for area in area_keys:
        for card_num in sorted(card_dict[area].keys()):
            xls.write(card_row,card_c,card_dict[area][card_num])
            card_c += 1
if __name__ == '__main__':
    wb = xlwt.Workbook(encoding='utf-8')
    xls = wb.add_sheet('卡牌分布')
    write_xls_title()
    card_row = 1
    for card in card_keys:
        print card
        calc_card(card,card_row)
        card_row += 1
    wb.save('/data/tmpdir/card_result.xls')
