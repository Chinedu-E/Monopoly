


def jail_rule(func):
    def wrapper(*args, **kwargs):
        doubles_count = 0
        doubles = True
        while doubles:
            roll = func(*args, **kwargs)
            yield roll
            if roll[0] == roll[1]:
                doubles = True
                doubles_count += 1
            else:
                doubles = False
            if doubles_count == 3:
                return "jail"
    return wrapper