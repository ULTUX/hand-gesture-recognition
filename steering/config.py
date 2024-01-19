import configparser

gesture_dict = {}
hold_time = 1000


def read_config():
    global gesture_dict
    global hold_time

    cfg = configparser.ConfigParser()
    with open('ustawienia.cfg', 'rt') as configfile:
        cfg.read_file(configfile)

    for gesture_label in cfg['Gesty']:
        gesture_label_str = str(gesture_label)
        gesture_dict[gesture_label_str] = cfg['Gesty'].get(gesture_label_str)

    hold_time = cfg['Opcje'].getint('czas_wstrzymania_ms')
