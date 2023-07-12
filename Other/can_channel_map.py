### 通过CCU_x的CAN报文判断CAN通道，适配A02 9.x CMX By ZhangMing
### Lib: python_can
'''
public_CANFD1 = [0x268,0x330,0x339,0x123,0x361,0x125,0x126]
ccu_CANFD1 = [0x268,0x361]
ccu_CANFD2 = [0x268,0x330]
ccu_CANFD3 = [0x268,0x361,0x125]
czf_CANFD = [0x268, 0x127, 0x330, 0x123, 0x361, 0x126]
czl_CANFD = [0x268,0x127,0x139,0x13A,0x157,0x330,0x120,0x121,0x339,0x123,0x361,0x126]
czr_CANFD = [0x268,0x127,0x139,0x13A,0x157,0x14E,0x330,0x120,0x121,0x339,0x123,0x361,0x125,0x126]
czt_CANFD = [0x268,0x127,0x139,0x13A,0x157,0x330,0x120,0x121,0x123,0x361,0x126]
cidc_CANFD = [0x268,0x127,0x14E,0x330,0x120,0x339,0x123,0x361,0x125,0x126]
tbox_CANFD = [0x268,0x14E]
'''
### End of description

import can
import operator

filename = 'd:/tmp/VDCCAN_378ms.blf'

id_to_check_list = [0x268, 0x127, 0x139, 0x13A, 0x157, 0x14E, 0x330, 0x120, 0x121, 0x339, 0x123, 0x361, 0x125, 0x126]
public_CANFD1 = [0x268,0x330,0x339,0x123,0x361,0x125,0x126]
ccu_CANFD1 = [0x268,0x361]
ccu_CANFD2 = [0x268,0x330]
ccu_CANFD3 = [0x268,0x361,0x125]
czf_CANFD = [0x268, 0x127, 0x330, 0x123, 0x361, 0x126]
czl_CANFD = [0x268,0x127,0x139,0x13A,0x157,0x330,0x120,0x121,0x339,0x123,0x361,0x126]
czr_CANFD = [0x268,0x127,0x139,0x13A,0x157,0x14E,0x330,0x120,0x121,0x339,0x123,0x361,0x125,0x126]
czt_CANFD = [0x268,0x127,0x139,0x13A,0x157,0x330,0x120,0x121,0x123,0x361,0x126]
cidc_CANFD = [0x268,0x127,0x14E,0x330,0x120,0x339,0x123,0x361,0x125,0x126]
tbox_CANFD = [0x268,0x14E]

public_CANFD1.sort()
ccu_CANFD1.sort()
ccu_CANFD2.sort()
ccu_CANFD3.sort()
czf_CANFD.sort()
czl_CANFD.sort()
czr_CANFD.sort()
czt_CANFD.sort()
cidc_CANFD.sort()
tbox_CANFD.sort()
dict_ch_mapping = {
    'Public_CANFD1': public_CANFD1,
    'CCU_CANFD1': ccu_CANFD1,
    'CCU_CANFD2': ccu_CANFD2,
    'CCU_CANFD3': ccu_CANFD3,
    'CZL': czl_CANFD,
    'CZF': czf_CANFD,
    'CZR': czr_CANFD,
    'CZT': czt_CANFD,
    'CIDC': cidc_CANFD,
    'TBOX': tbox_CANFD
}

start_timestamp = 0
dict_channel = {}

def do_add_list(): #子涵数 统计每个channel的CAN id表
    if msg.channel in dict_channel.keys():
        if msg.arbitration_id not in dict_channel[msg.channel]:
            dict_channel[msg.channel].append(msg.arbitration_id)
        else:
            pass
    else:
        dict_channel[msg.channel]=[msg.arbitration_id]
    return

#开始读BLF文件
blf = can.BLFReader(filename)
msg_count = 0
# try:
for msg in blf:
    if msg.arbitration_id in id_to_check_list: 
        msg_count +=1
        if start_timestamp == 0: # 1st CAN message 处理
            start_timestamp = msg.timestamp
            do_add_list()
        elif msg.timestamp - start_timestamp > 5:
            print('Already checked 5 seconds. Exit. %d Messages checked' %msg_count)
            break
        else:
            do_add_list()
    else:
        pass
#     except:
#         continue

#处理通道映射关系
for key in dict_channel.keys():
    tmp_ch = dict_channel[key]
    tmp_ch.sort()
    pared = 0
    for ch in dict_ch_mapping.keys():
        if operator.eq(tmp_ch, dict_ch_mapping[ch]):
            dict_ch_mapping[ch] = key
            pared = 1
    if pared == 0:
        print('CAN %d not pared' %key)

#输出结果
print()
print('****Result****')
print()
tmp = ''
for key in dict_ch_mapping.keys():
    print(key, dict_ch_mapping[key])
    tmp= tmp + key+': ' + str(dict_ch_mapping[key]+1) + '\r\n'
print()
print('tmp is', tmp)
import win32api, win32con
print(win32api.MessageBox(0,tmp,'Channel Mapping', win32con.MB_OK))
print('EOF')  