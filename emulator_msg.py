# 인터페이스 내용 포함으로 비공개

import time
import datetime

# 전문 공통 헤더 메시지 생성
def make_header_msg(sequence, lane, data_len, flag):
 
# 감지 시작 메시지 생성
def make_detect_start_msg(lane, time_val, trigger_num):    

# 영상 정보 메시지 생성
def make_image_msg(lane, time_val, trigger_num):
   
# 감지 해제 메시지 생성
def make_detect_end_msg(lane, time_val, trigger_num, second_time, car_type, car_len, car_width, car_height, speed):

# 태그 메시지 생성
def make_tag_msg(tagid, time1, time2):
   

__all__ = [
    'make_header_msg','make_detect_start_msg','make_image_msg','make_detect_end_msg','make_tag_msg'
]
    
