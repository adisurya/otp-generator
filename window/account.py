#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import time
import md5

class AccountWindow:
    def __init__(self, caller = None):
        self.caller = caller

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

    def show(self):
        self.window.show()
