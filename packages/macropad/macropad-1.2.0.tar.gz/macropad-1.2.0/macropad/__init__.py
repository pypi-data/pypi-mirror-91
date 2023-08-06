from .CustomLP import CustomLP
from threading import Thread
from datetime import datetime


class MacroPad:



    lp = CustomLP()
    _bindings = {}
    _binding_execution_thread_enabled = False
    _color_on_binding_activate = {}
    _color_on_binding_deactivate = {}
    _enabled_leds = []
    _switches = {}



    def __init__(self, number=0, name="Mk2"):
        self.lp.Close()
        self.lp.Open(number, name)
        self.lp.LedAllOn(0)



    def close(self):
        self.lp.Close()



    def bind(self, x: int, y: int, colorcode=0, color_on_activate: int = None, on_release=False):
        def inner(func):

            if (x, y) in self._switches: return

            self._bindings[(x, y, not on_release)] = func
            self._color_on_binding_activate[(x, y)] = color_on_activate if color_on_activate else colorcode
            self._color_on_binding_deactivate[(x, y)] = colorcode

            self.lp.LedCtrlXYByCode(x, y, colorcode if not on_release else color_on_activate)

        return inner



    def unbind(self, x, y):
        if (x, y, True) in self._bindings:
            del self._bindings[x, y, True]
            del self._color_on_binding_activate[(x, y)]
            del self._color_on_binding_deactivate[(x, y)]
            self.lp.LedCtrlXYByCode(x, y, 0)

        elif (x, y, False) in self._bindings:
            del self._bindings[x, y, False]
            del self._color_on_binding_activate[(x, y)]
            del self._color_on_binding_deactivate[(x, y)]
            self.lp.LedCtrlXYByCode(x, y, 0)



    def unbind_all(self):

        for x, y, _ in self._bindings:
            print(0, datetime.now())
            self.lp.LedCtrlXYByCode(x, y, 0)

        self._bindings = {}
        self._color_on_binding_activate = {}
        self._color_on_binding_deactivate = {}



    def start_binding_execution_thread(self):
        def thread():

            while self._binding_execution_thread_enabled:
                buttons = self.lp.GetButtonsXY()

                if not buttons: continue

                for button in buttons:

                    if (button.x, button.y, button.pressed) in self._bindings:

                        self.lp.LedCtrlXYByCode(button.x, button.y, self._color_on_binding_activate[(button.x, button.y)])
                        self._bindings[(button.x, button.y, button.pressed)].__call__()


                    elif (button.x, button.y, not button.pressed) in self._bindings:
                        self.lp.LedCtrlXYByCode(button.x, button.y, self._color_on_binding_deactivate[(button.x, button.y)])

                    elif (button.x, button.y) in self._switches:
                        if button.pressed:

                            self._switches[button.x, button.y] = [self._switches[button.x, button.y][0],
                                                                  self._switches[button.x, button.y][1],
                                                                  not self._switches[button.x, button.y][2],
                                                                  self._switches[button.x, button.y][3]]

                            self.lp.LedCtrlXYByCode(button.x, button.y, self._switches[button.x, button.y][0] if
                            self._switches[button.x, button.y][2] else self._switches[button.x, button.y][1])

                            self._switches[button.x, button.y][3].__call__(self._switches[button.x, button.y][2])

        self._binding_execution_thread_enabled = True
        t = Thread(target=thread)
        t.start()
        return t




    def stop_binding_execution_thread(self):
        self._binding_execution_thread_enabled = False



    def enable_led(self, x, y, colorcode):
        if (x, y, True) in self._bindings or (x, y, False) in self._bindings or (x, y) in self._switches: return

        self.lp.LedCtrlXYByCode(x, y, colorcode)
        self._enabled_leds.append((x, y))



    def disable_led(self,x, y):
        if (x, y) in self._enabled_leds: self.lp.LedCtrlXYByCode(x, y, 0)



    def disable_all_leds(self):

        for x, y in self._enabled_leds:
            self.lp.LedCtrlXYByCode(x, y, 0)

    def bind_switch(self, x: int, y: int, color_enabled=0, color_disabled=0, run_on_bind=False, default_enabled=False):
        def inner(func):


            if (x, y, True) in self._bindings or (x, y, False) in self._bindings: return

            self._switches[(x, y)] = [color_enabled, color_disabled, default_enabled, func]

            self.lp.LedCtrlXYByCode(x, y, color_disabled if not default_enabled else color_enabled)

            if run_on_bind: func.__call__(default_enabled)

        return inner

    def unbind_switch(self, x, y):

        try:
            del self._switches[(x, y)]
            self.lp.LedCtrlXYByCode(x, y, 0)
        except: pass

    def unbind_all_switches(self):
        for switch in self._switches:
            print(switch)
            #self.lp.LedCtrlXYByCode(x, y, 0)

        print("done")

        self._switches.clear()
        print("completely")

    def printall(self):
        print(self._switches)
        print(self._bindings)
        print(self._enabled_leds)