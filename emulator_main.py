# ============================================================================
# 차로 데이터 생성 에뮬레이터
# ============================================================================

import time
import socket
import random
import threading
from datetime import datetime, timedelta

from emulator_msg import *
from emulator_que import *
from emulator_setting import *


# 사용자 선택 및 차량 데이터 지정
def main():
    print("[1] Version - Gantry1 : VDS / Gantry2 : RFID, IPU (말레이시아)")
    print("[2] Version - Gantry1 : VDS,RFID / Gantry2 : IPU (정읍)")
    print(f"Gantry1 <-> 2 사이 거리 : {bet_gan1_gan2}")
    version_check = input("테스트 버전 설정 (1 or 2): ")

    lane1_trigger = 1
    lane2_trigger = 1
    while True:
        car_info = []
        road1_info = []
        road2_info = []
        if int(version_check) == 1:
            print("[말레이시아 버전]")
        elif int(version_check) == 2:
            print("[정읍 버전]")

        car_count = input("통행 차량 댓수 입력 : ")
        notag_count = input("태그 미부착 차량 댓수 (-1 : 랜덤 발생) : ")
        if int(car_count) < int(notag_count):
            print("태그 미부착 차량 댓수 오류-랜덤 발생")

        # 태그 미부착 차량 댓수가 -1 : 랜덤 발생
        if int(notag_count) == -1 or int(notag_count) > int(car_count):
            for _ in range(int(car_count)):
                lane = random.randint(1, 2)  # 1, 2차로 중 랜덤으로 선택
                car_type = random.choice(list(cars.keys()))  # 차종 랜덤 선택
                speed = random.randint(70, 130)  # 속도 랜덤 선택
                tag_on_off = random.randint(1, 5)  # 태그 부착 여부 (80% 확률 : 부착, 20% 확률 : 미부착)
                if tag_on_off == 5:
                    rfid = 'X'
                else:
                    tag_char = 'ABCDEF123456789ABCDEF123456798'
                    rfid = ''.join(random.sample(tag_char, 24))

                car_info.append({'lane': lane, 'car_type': car_type, 'speed': speed, 'rfid': rfid})

            # 태그 미부착 차량 댓수가 있을 경우
        else:
            for _ in range(int(notag_count)):
                lane = random.randint(1, 2)  # 1, 2차로 중 랜덤으로 선택
                car_type = random.choice(list(cars.keys()))  # 차종 랜덤 선택
                speed = random.randint(70, 130)  # 속도 랜덤 선택
                car_info.append({'lane': lane, 'car_type': car_type, 'speed': speed, 'rfid': 'X'})

            for _ in range(int(car_count) - int(notag_count)):
                lane = random.randint(1, 2)  # 1, 2차로 중 랜덤으로 선택
                car_type = random.choice(list(cars.keys()))  # 차종 랜덤 선택
                speed = random.randint(70, 130)  # 속도 랜덤 선택
                tag_char = 'ABCDEF123456789ABCDEF123456798'
                rfid = ''.join(random.sample(tag_char, 24))
                car_info.append({'lane': lane, 'car_type': car_type, 'speed': speed, 'rfid': rfid})

            # 차량데이터 정렬
        car_info = sorted(car_info, key=lambda x: x['speed'], reverse=True)

        # 생성된 차량 정보를 분류 + 트리거 번호 부여
        for data in car_info:
            if data['lane'] == 1:
                road1_info.append(
                    {'lane': data['lane'], 'car_type': data['car_type'], 'speed': data['speed'],
                     'rfid': data['rfid']})
                road1_info[-1]['trigger'] = lane1_trigger
                lane1_trigger += 1
            elif data['lane'] == 2:
                road2_info.append(
                    {'lane': data['lane'], 'car_type': data['car_type'], 'speed': data['speed'],
                     'rfid': data['rfid']})
                road2_info[-1]['trigger'] = lane2_trigger
                lane2_trigger += 1

        print("-" * 100)
        print("1번 차로 차량 정보")
        for data in road1_info:
            print(data)
        print("-" * 100)
        print("2번 차로 차량 정보")
        for data in road2_info:
            print(data)
        print("-" * 50)

        thread1 = threading.Thread(target=make_packet, args=(road1_info, 1, int(version_check)))
        thread1.start()
        thread2 = threading.Thread(target=make_packet, args=(road2_info, 2, int(version_check)))
        thread2.start()
        thread1.join()
        thread2.join()

def make_packet(car_info, lane_info, version):
    current_id = threading.current_thread().ident
    # 소켓 연결
    while True:
        try:
            mcu_ip = '127.0.0.1'
            mcu_port = int(20333)
            mcu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mcu_socket.connect((mcu_ip, mcu_port))
            print(f"{lane_info}차로 MCU 서버 연결 >>> [Success]")
            break
        except Exception as e:
            print("MCU 서버 연결 >>> [Failed] " + str(e))
            time.sleep(2)


    start_time = datetime.now()  # 첫 차량이 출발지에서 출발하는 시간
    for i, data in enumerate(car_info, 1):
        road_num = data['lane']  # 차로 번호
        car_type = cars[data['car_type']]  # 종
        car_len = car_type['len']  # 차장
        car_width = car_type['width']  # 차폭
        car_height = car_type['height']  # 차고
        speed = data['speed']  # 차속도
        tag_id = data['rfid']  # 태그 ID
        trigger_num = data['trigger']

        speed_mps = speed * 1000 / 3600  # km/h 를 m/s 로 변경
        time1 = 30 / speed_mps  # 출발지 부터 감지 시작 까지 30m
        time2 = car_len / speed_mps / 100  # 차량 길이 m 로 변환, 감지 시작, 감지해제 사이의 시간
        time3 = bet_gan1_gan2 / speed_mps  # Gantry1 <-> Gantry2 사이 15 m 를 가는데 걸린 시간

        if version == 1:
            detect_start_time = start_time + timedelta(seconds=time1)  # 감지 시작, 영상정보 촬영
            detect_end_time = detect_start_time + timedelta(seconds=time2)  # 감지 해제
            rfid_tag_time = detect_start_time + timedelta(seconds=time3)  # RFID 태그 감지
            rfid_tag_end_time = rfid_tag_time + timedelta(seconds=time2)  # RFID 태그 감지 해제
            start_time = rfid_tag_end_time  # 첫 차량이 태그 감지 해제 되면 다음 차가 출발한다고 가정

        elif version == 2:
            detect_start_time = start_time + timedelta(seconds=time1)  # 감지 시작, 영상정보 촬영
            detect_end_time = detect_start_time + timedelta(seconds=time2)  # 감지 해제
            rfid_tag_time = detect_start_time  # RFID 태그 감지
            rfid_tag_end_time = rfid_tag_time + timedelta(seconds=time2)  # RFID 태그 감지 해제
            start_time = rfid_tag_end_time

        # 감지 시작 메시지 생성
        detect_start_header = make_header_msg(i, road_num, 28, 0)
        detect_start_body = make_detect_start_msg(road_num, detect_start_time, trigger_num)
        detect_start_full = detect_start_header + detect_start_body
        mcu_socket.send(bytes.fromhex(detect_start_full))
        msg = mcu_socket.recv(100)
        print(f"{lane_info}차로 {i}번째 차량 감지시작 : {detect_start_full}\n[감지시작 응답] {bytes(msg).hex()}")
        time.sleep(0.2)

        # 영상 정보 메시지 생성
        image_info_header = make_header_msg(i, road_num, 39, 1)
        image_info_body = make_image_msg(road_num, detect_start_time, trigger_num)
        image_msg_full = image_info_header + image_info_body
        mcu_socket.send(bytes.fromhex(image_msg_full))
        msg = mcu_socket.recv(100)
        print(f"{lane_info}차로 {i}번째 차량 영상정보 : {image_msg_full}\n[영상정보 응답] {bytes(msg).hex()}")
        time.sleep(0.2)

        # 감지 해제 메시지 생성
        detect_end_header = make_header_msg(i, road_num, 50, 0)
        detect_end_body = make_detect_end_msg(road_num, detect_end_time, trigger_num, time2, data['car_type'], car_len,
                                              car_width, car_height, speed)
        detect_end_full = detect_end_header + detect_end_body

        mcu_socket.send(bytes.fromhex(detect_end_full))
        msg = mcu_socket.recv(100)
        print(f"{lane_info}차로 {i}번째 차량 감지해제 : {detect_end_full}\n[감지해제 응답] {bytes(msg).hex()}")
        print(f"")
        time.sleep(0.2)

        # 태그 메시지 큐 적재
        if tag_id != 'X':
            tag_qmsg = make_tag_msg(tag_id, rfid_tag_time, rfid_tag_end_time)
            print(f"{lane_info}차로 {i}번째 차량  TAG Data : " + str(tag_qmsg))
            insert_tag_queue(tag_qmsg, current_id)
            time.sleep(0.1)
        elif tag_id == 'X':
            print(f"{lane_info}차로 {i}번째 차량  RFID태그 미부착")

if __name__ == "__main__":
    print("=" * 100)
    print("[차로 데이터 생성기 (2차선)]")
    print("=" * 100)
    main()
