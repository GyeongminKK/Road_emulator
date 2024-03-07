import time
import datetime

def make_header_msg(sequence, lane, data_len, flag):
    stx = '02'
    seq = str('{:04x}'.format(sequence))
    retry = '00'
    msg_len = str('{:04x}'.format(data_len))
    if flag == 1: 
        equip_code = '0481'
    else :
        equip_code ='0381' if lane == 1 else '0382'
    reserved = '0000'
    
    header_msg = stx + seq + retry + msg_len + equip_code + reserved
    return header_msg

# 감지 시작 메시지 데이터 부분
def make_detect_start_msg(lane, time_val, trigger_num):
    # 시간 양식 변경
    milliseconds = time_val.strftime("%f")[:3]
    detect_start_time = time_val.strftime("%Y%m%d%H%M%S") + milliseconds +'0'

    param1 = '3101'
    param2 = '11' if lane == 1 else '22'
    param3 = detect_start_time
    param4 = '01' if lane == 1 else '02'
    param5 = str('{:08x}'.format(int(trigger_num)))
    param6 = '00'
    param7 = '0' * 20
    etx = '03'

    
    return param1 + param2 + param3 + param4 + param5 + param6 + param7 + etx

# 영상 정보 메시지 데이터 부분
def make_image_msg(lane, time_val, trigger_num):
    # 시간 양식 변경
    milliseconds = time_val.strftime("%f")[:3]
    get_image_time = time_val.strftime("%Y%m%d%H%M%S") + milliseconds +'0'
    
    param1 = '4101'
    param2 = '11' if lane == 1 else '22'
    param3 = get_image_time
    param4 = '01' if lane == 1 else '02'
    param5 = str('{:08x}'.format(int(trigger_num)))
    param6 = '11' + '9999999999' + 'FF' + '0000000000'
    param7 = '0' * 20
    etx = '03'
    
    return param1 + param2 + param3 + param4 + param5 + param6 + param7 + etx

def make_detect_end_msg(lane, time_val, trigger_num, second_time, car_type, car_len, car_width, car_height, speed):
    # 시간 양식 변경
    milliseconds = time_val.strftime("%f")[:3]
    detect_end_time = time_val.strftime("%Y%m%d%H%M%S") + milliseconds +'0'
    
    param1 = '3102'
    param2 = '11' if lane == 1 else '22'
    param3 = detect_end_time
    param4 = '01' if lane == 1 else '02'
    param5 = str('{:08x}'.format(int(trigger_num)))
    param6 = str('{:08x}'.format(int(second_time * 1000)))
    param7 = '01'
    param8 = '01'
    param9 = '02' if car_type == 'A' or car_type == 'B' else '01'
    param10 = '0000'    # 축수
    param11 = '0000'    # 윤폭
    param12 = '0000'    # 윤거
    param13 = str('{:04x}'.format(int(car_width)))  # 차폭
    param14 = str('{:04x}'.format(int(car_len)))    # 차장
    param15 = str('{:04x}'.format(int(car_height))) # 차고
    param16 = '0000'    # 발권단 위치
    param17 = str('{:04x}'.format(int(speed)))
    param18 = '0' * 20
    etx = '03'

    return param1 + param2 + param3 + param4 + param5 + param6 + param7 + param8 + param9 + param10 \
            + param11 + param12 + param13 + param14 + param15 + param16 + param17 + param18 + etx
            
def make_tag_msg(tagid, time1, time2):
    tag_mil1 = time1.strftime("%f")[:3]
    tag_mil2 = time2.strftime("%f")[:3]
    tag_start_time = time1.strftime("%Y%m%d%H%M%S") + tag_mil1 +'0'
    tag_end_time = time2.strftime("%Y%m%d%H%M%S") + tag_mil2 +'0'

    param1 = '3501'
    if tagid == 'X' :
        param2 = '0' * 24
    else : 
        param2 = tagid
    param3 = tag_start_time
    param4 = tag_end_time
    
    return param1 + param2 + param3 + param4

__all__ = [
    'make_header_msg','make_detect_start_msg','make_image_msg','make_detect_end_msg','make_tag_msg'
]
    
