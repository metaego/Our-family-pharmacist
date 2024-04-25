def impute_weight(sex, age):
    print(sex, age)
    if sex == 'f':
        if age < 6:
            weight = None
        elif age < 9:
            weight = 26.9
        elif age < 12:
            weight = 40.0
        elif age < 15:
            weight = 52.2
        elif age < 19:
            weight = 56.5
        elif age < 30:
            weight = 59.0
        elif age < 40:
            weight = 59.6
        elif age < 50:
            weight = 59.8
        elif age < 60:
            weight = 58.9
        elif age < 70:
            weight = 58.2
        elif age < 80:
            weight = 57.2
        else:
            weight = 53.5
    elif sex == 'm':
        if age < 6:
            weight = None
        elif age < 9:
            weight = 28.5
        elif age < 12:
            weight = 43.1
        elif age < 15:
            weight = 59.9
        elif age < 19:
            weight = 69.6
        elif age < 30:
            weight = 75.7
        elif age < 40:
            weight = 79.5
        elif age < 50:
            weight = 77.4
        elif age < 60:
            weight = 73.1
        elif age < 70:
            weight = 69.5
        elif age < 80:
            weight = 66.6
        else:
            weight = 63.3
    return weight

def impute_height(sex, age):
    if sex == 'f':
        if age < 6:
            height = None
        elif age < 9:
            height = 125.6
        elif age < 12:
            height = 144.2
        elif age < 15:
            height = 158.4
        elif age < 19:
            height = 161.4
        elif age < 30:
            height = 161.8
        elif age < 40:
            height = 161.9
        elif age < 50:
            height = 160.6
        elif age < 60:
            height = 157.9
        elif age < 70:
            height = 155.3
        elif age < 80:
            height = 152.6
        else:
            height = 149.0
    elif sex == 'm':
        if age < 6:
            height = 126.6
        elif age < 9:
            height = 144.2
        elif age < 12:
            height = 164.6
        elif age < 15:
            height = 173.5
        elif age < 19:
            height = 174.4
        elif age < 30:
            height = 174.4
        elif age < 40:
            height = 174.7
        elif age < 50:
            height = 173.5
        elif age < 60:
            height = 170.7
        elif age < 70:
            height = 168.0
        elif age < 80:
            height = 165.6
        else:
            height = 163.7
    return height