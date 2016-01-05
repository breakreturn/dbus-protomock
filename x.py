
BUS_NAME = "com.jogr.X"
MAIN_OBJ = "/com/jogr/X"
MAIN_IFACE = "com.jogr.X"

SYSTEM_BUS = False


def load(mock, parameters):
    
    mock.AddMethods(MAIN_IFACE, [
        ("Ping", "", "s", "ret = True"),
    ])

