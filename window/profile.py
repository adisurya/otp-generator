#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import md5
import random

class ProfileWindow:
    window = None
    profile_entry = None
    secret_entry = None
    secret_label = None
    secret_status = "auto"
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
            self.secret_status = "manual"
        else:
            self.secret_entry.set_sensitive(False)
            self.secret_entry.set_text("")
            self.secret_status = "auto"

    def add_Profile(self, widget, data = None):
        cursor = self.connection.cursor()
        entry = self.profile_entry.child
        profile_name = entry.get_text()

        # check for empty profile name
        if len(profile_name) <= 0:
            dialog = gtk.MessageDialog(
                self.window,
                gtk.DIALOG_MODAL,
                gtk.MESSAGE_WARNING,
                gtk.BUTTONS_OK,
                "Please enter your profile name!"
            )
            response = dialog.run()
            if response:
                dialog.destroy()
                entry.grab_focus()
            return None

        # check for already used profile name
        sql = "SELECT name FROM profiles WHERE name = ?"
        cursor.execute(sql, (profile_name,))
        if cursor.rowcount > 0:
            dialog = gtk.MessageDialog(
                self.window,
                gtk.DIALOG_MODAL,
                gtk.MESSAGE_WARNING,
                gtk.BUTTONS_OK,
                "Profile name is already used!"
            )
            response = dialog.run()
            if response:
                dialog.destroy()
                entry.grab_focus()
            return None

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

    def generate_secret(self):
        if self.secret_status == "manual":
            secret = self.secret_entry.get_text()
            if len(secret) <= 0:
                dialog = gtk.MessageDialog(
                    self.window,
                    gtk.DIALOG_MODAL,
                    gtk.MESSAGE_WARNING,
                    gtk.BUTTONS_OK,
                    "Please enter secret key or choose Automatic"
                )
                response = dialog.run()
                if response:
                    dialog.destroy()
                    self.secret_entry.grab_focus()
                return None
            else:
                return secret
        else:
            rand_number = str(random.getrandbits(400))
            md = md5.new()
            md.update(rand_number)
            return md.hexdigest()
