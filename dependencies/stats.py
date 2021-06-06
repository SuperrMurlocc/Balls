def save_level(level_num):
    with open("read/stats.txt", "a") as file:
        file.write(f"{level_num}\n")


def check_highscore():
    high = 0
    avg = 0
    n = 0
    with open("read/stats.txt", "r") as file:
        for line in file:
            score = int(line)
            if score > high:
                high = score
            avg += score
            n += 1
    if n != 0:
        avg //= n
    return high, avg


if __name__ == '__main__':
    print(check_highscore())