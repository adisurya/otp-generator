#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import time
import md5

class ProfileWindow:
    window = None
    profile_entry = None
    secret_entry = None
    secret_label = None
    def __init__(self, caller = None):
        self.caller = caller
        self.connection = caller.connection

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_transient_for(self.caller.window)
        self.window.set_modal(True)
        self.window.connect("delete_event", self.delete_event)

        container = gtk.VBox(False)
        container.show()
        label = gtk.Label("Profile Name")
        container.pack_start(label, False, False, 0)
        label.show()

        store = gtk.ListStore(str)

        self.profile_entry = gtk.ComboBoxEntry(store)
        container.pack_start(self.profile_entry, False, False, 0)
        self.populate_profile(self.profile_entry)
        self.profile_entry.show()

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
        cursor = self.connection.cursor()

        cursor.close()

    def remove_Profile(self, widget, data = None):
        pass
        
    def populate_profile(self, widget):
        store = widget.get_model()
        store.clear()

        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM profiles")

        for name, in cursor:
            store.append([name])
            print name

        cursor.close()

    def delete_event(self, widget, event, data = None):
        self.window.hide()
        return True
