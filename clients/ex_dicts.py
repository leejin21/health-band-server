import random


def heart_example(kind, num):

    if kind == "s":
        # 서맥성 부정맥
        hl = [random.randint(20, 59) for i in range(num)]
    elif kind == "b":
        # 빈맥성 부정맥
        hl = [random.randint(111, 150) for i in range(num)]
    else:
        # 아무것도 아님
        hl = [random.randint(61, 109) for i in range(num)]

    l = []
    for i in range(num):
        l.append({
            "temp": "17",
            "humid": "50",
            "heartRate": str(hl[i]),
        })

    return l


def normal_example(num):
    l = []
    for i in range(num):
        l.append({
            "temp": str(random.randint(10, 18)),
            "humid": str(random.randint(45, 70)),
            "heartRate": str(random.randint(61, 109))
        })
    return l


def loc_example(num):
    l = []
    for i in range(num):
        l.append({
            "latitude": "latitude0001",
            "longitude": "longitude0001",
        })

    return l


def sum_event(kind, num):
    if kind == "C":
        tl = [random.randint(33, 34) for i in range(num)]
        hl = [random.randint(66, 79) for i in range(num)]

    l = []
    for i in range(num):
        l.append({
            "temp": tl[i],
            "humid": hl[i],
            "heartRate": str(random.randint(61, 109))
        })

    return l
