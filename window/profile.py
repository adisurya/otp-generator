#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import time
import md5

class ProfileWindow:
    def __init__(self, caller = None):
        self.caller = caller

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_transient_for(self.caller.window)
        self.window.set_modal(True)

        container = gtk.VBox(False)
        container.show()

        label = gtk.Label("Profile Name")
        container.pack_start(label, False, False, 0)
        label.show()

        self.Profile_name_entry = gtk.Entry()
        container.pack_start(self.Profile_name_entry, False, False, 0)
        self.Profile_name_entry.show()

        label = gtk.Label("Secret")
        container.pack_start(label, False, False, 0)
        label.show()



        secret_button = gtk.RadioButton(None, "Automatic")
        secret_button.connect("toggled", self.secret_toggle, "Automatic")
        container.pack_start(secret_button, False, False, 0)
        secret_button.show()

        secret_box = gtk.HBox(False)
        container.pack_start(secret_box, False, False, 0)
        secret_box.show()

        secret_button = gtk.RadioButton(secret_button, "Manual Entry")
        secret_button.connect("toggled", self.secret_toggle, "Manual")
        secret_box.pack_start(secret_button, False, False, 0)
        secret_button.show()
        
        self.secret_entry = gtk.Entry()
        self.secret_entry.set_sensitive(False)
        secret_box.pack_start(self.secret_entry, False, False, 0)
        self.secret_entry.show()

        self.secret_label = gtk.Label()
        container.pack_start(self.secret_label, False, False, 0)
        self.secret_label.show()

        button_box = gtk.HButtonBox()
        button_box.set_layout(gtk.BUTTONBOX_END)
        container.pack_start(button_box, False, False, 0)
        button_box.show()


        button = gtk.Button("Add")
        button.connect("clicked", self.add_Profile)
        button.show()
        button_box.add(button)

        button = gtk.Button("Remove")
        button.connect("clicked", self.remove_Profile)
        button.show()
        button_box.add(button)

        self.window.add(container)

    def show(self):
        self.window.show()

    def secret_toggle(self, widget, data = None):
        if data == "Manual":
            self.secret_entry.set_sensitive(True)
        else:
            self.secret_entry.set_sensitive(False)
            self.secret_entry.set_text("")

    def add_Profile(self, widget, data = None):
        pass

    def remove_Profile(self, widget, data = None):
        pass
