# 차량 정보
cars = {
    'A': {'len': 359, 'width': 159, 'height': 152},  # 경차 차 사이즈 , 차장, 차폭, 차고 순 단위 cm
    'B': {'len': 471, 'width': 182, 'height': 142},  # 일반 승용차
    'C': {'len': 515, 'width': 174, 'height': 197}  # 포터, 트럭 등
}

# 갠트리 구성
bet_gan1_gan2 = 15      # 갠트리 1번과 2번 사이의 거리

# 트리거번호 초기화


__all__ = [
    'cars','bet_gan1_gan2'
]