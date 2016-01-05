#!/usr/bin/python

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib as glib
from gi.repository import GObject as gobject


BUS = dbus.SessionBus

NAME = "com.jogr.MyComponent"
OPATH = "/com/jogr/MyComponent"

COMPONENT_X_NAME = "com.jogr.X"
COMPONENT_X_OPATH = "/com/jogr/X"


class MyComponent(dbus.service.Object):
    """Example component

    Pings another component with a message and depending on the
    return value either continues or stops pinging.

    This componnent has a dependency to component X which needs to be on D-Bus and
    respond to method calls.
    """

    def __init__(self):
        self.__bus = BUS()

        # Get out on the bus and initialize parent
        request = self.__bus.request_name(NAME, dbus.bus.NAME_FLAG_REPLACE_EXISTING)
        bus_name = dbus.service.BusName(NAME, bus=self.__bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)

        # Find the X component on the bus
        self.__x_service = self.__get_x_iface()

        # Default message to pass to component X
        self.__message = "Hello world"

        # Initiate communication with component X
        self.StartPinging()

    @dbus.service.method(NAME, in_signature="", out_signature="", sender_keyword="sender")
    def StartPinging(self, sender=None):
        """Calling this method starts the communication with component X"""
        print "start pinging..."
        # call do_ping() every two seconds until it returns false
        glib.timeout_add(2000, self.__do_ping)

    @dbus.service.method(NAME, in_signature="s", out_signature="", sender_keyword="sender")
    def SetMessage(self, message, sender=None):
        """Set a new message to send to component X"""
        self.__message = message

    def __do_ping(self):
        """Make the call to component X. If the message "Bye" is returned we stop pinging"""
        ret = self.__x_service.Ping(self.__message)
        print self, "pinged with message \"", self.__message, "\"and got back:", ret
        if ret == "Bye":
            exit()
        return True

    def __get_x_iface(self):
        remote_object = self.__bus.get_object(COMPONENT_X_NAME, COMPONENT_X_OPATH)
        iface = dbus.Interface(remote_object, COMPONENT_X_NAME)
        return iface


if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    myservice = MyComponent()
    gobject.MainLoop().run()

