import configparser

gesture_dict = {}
hold_time = 1000


def read_config():
    global gesture_dict
    global hold_time

    cfg = configparser.ConfigParser()
    with open('ustawienia.cfg', 'rt') as configfile:
        cfg.read_file(configfile)

    for i in range(1, 6):
        gesture_dict[str(i)] = cfg['Gesty'].get(str(i))

    hold_time = cfg['Opcje'].getint('czas_wstrzymania_ms')
