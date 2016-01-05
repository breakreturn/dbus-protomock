
BUS_NAME = "com.jogr.X_bus_name" #this does not appear in introspection XML
MAIN_OBJ = "/com/jogr/X_main_obj" #this is the "node name"
MAIN_IFACE = "com.jogr.X_main_iface" #this is the "interface name"

SYSTEM_BUS = False


def load(mock, parameters):
    mock.AddMethods(MAIN_IFACE, [
        ("Ping", "", "s", "ret = 'pong!'"),
    ])

    mock.AddProperties(MAIN_IFACE, {"apa1": 1, "apa2": 2})
