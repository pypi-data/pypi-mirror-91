import platform
if platform.system() == "Windows":
    LEFT_JOY_X = 0
    LEFT_JOY_Y = 1
    RIGHT_JOY_X = 3
    RIGHT_JOY_Y = 4
else:
    LEFT_JOY_X = 1
    LEFT_JOY_Y = 0
    RIGHT_JOY_X = 3
    RIGHT_JOY_Y = 2

RIGHT_TRIGGER = 5
LEFT_TRIGGER = 2

