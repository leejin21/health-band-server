import random


def example_s():
    # 서맥성 부정맥
    hl = [random.randint(20, 59) for i in range(20)]
    l = []
    for i in range(len(hl)):
        l.append({
            "temp": "17",
            "humid": "53",
            "heartRate": str(hl[i]),
        })

    return l
