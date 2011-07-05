#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import time
import md5
import sqlite3

from window import profile
from window import about

class OTPGenerator:
    window = None
    profile_window = None
    def __init__(self):
        self.connection = sqlite3.connect('./data.sqlite')
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.profile_window = profile.ProfileWindow(self)
        self.window.set_title('OTP Generator')
        self.window.set_border_width(5)
        self.window.connect('destroy', lambda x: gtk.main_quit())

        ui = """
            <ui>
                <menubar name="MenuBar">
                    <menu action="Application">
                        <menuitem action="Profile" />
                        <menuitem action="About" />
                        <separator />
                        <menuitem action="Exit" />
                    </menu>
                </menubar>
            </ui>
            """
        ui_manager = gtk.UIManager()
        accel_group = ui_manager.get_accel_group()
        self.window.add_accel_group(accel_group)
        action_group = gtk.ActionGroup("Menu OTP")
        action_group.add_actions(
            [
                ("Application", None, "_Application", None, None, None),
                ("Profile", None, "_Profile", "<control>p", "Profile Setting", self.profile),
                ("About", None, "A_bout", "<control>b", "About This Application", self.about),
                ("Exit", None, "E_xit", "<control>x", "Exit This Application", gtk.main_quit)

            ]
        )
        ui_manager.insert_action_group(action_group, 0)
        ui_manager.add_ui_from_string(ui)
        menubar = ui_manager.get_widget("/MenuBar")

        container = gtk.VBox(False, 0)
        container.show()
        menubar.show()
        container.pack_start(menubar, False, False, 0)

        content = gtk.VBox(False)

        label = gtk.Label("Profile Name:")
        label.set_alignment(0,0)
        content.pack_start(label, False, False, 3)
        label.show()

        store = gtk.ListStore(str, str, int)

        self.profile_entry = gtk.ComboBoxEntry(store)
        content.pack_start(self.profile_entry, False, False, 0)
        self.populate_profile()
        self.profile_entry.show()


        label = gtk.Label('Pin')
        label.set_alignment(0,0)
        content.pack_start(label, False, False, 3)
        label.show()

        self.pin_entry = gtk.Entry(4)
        self.pin_entry.set_text("0000")
        content.pack_start(self.pin_entry, False, False, 3)
        self.pin_entry.show()

        generate_button = gtk.Button('Generate')
        generate_button.connect('clicked', self.generate_otp)
        content.pack_start(generate_button, False, False, 3)
        generate_button.show()
        

        self.result_label = gtk.Label('')
        content.pack_start(self.result_label, False, False, 3)
        self.result_label.show()

        content.show()
        container.pack_start(content, True, True, 12)
        self.window.add(container)

    def generate_otp(self, widget, data = None):

        # generate epoch number
        #  int(time.time()) convert time to int to remove decimal digit
        # int(time.time()) / 10 to remove 1 last digit
        epoch = str(int(time.time()) / 10)

        # print "epoch: " + epoch
        # print "secret key: " + self.secret_key
        # print "pin: " + self.pin_entry.get_text()

        secret = self.get_secret()
        if secret == None:
            return None

        md = md5.new()
        md.update(epoch + secret + self.pin_entry.get_text())
        result = md.hexdigest()
        self.result_label.set_text(result[0:6])

    def main(self):
        self.window.show()
        gtk.main()

    def profile(self, action, data = None):
        self.profile_window.show()

    def about(self):
        pass

    def populate_profile(self):
        store = self.profile_entry.get_model()
        store.clear()

        cursor = self.connection.cursor()
        cursor.execute("SELECT name, secret, show_secret FROM profiles")

        for name, secret, show_secret in cursor:
            store.append([name, secret, show_secret])

        cursor.close()

    def get_secret(self):
        model = self.profile_entry.get_model()
        active = self.profile_entry.get_active()

        if len(model) < 1:
            dialog = gtk.MessageDialog(
                self.window,
                gtk.DIALOG_MODAL,
                gtk.MESSAGE_WARNING,
                gtk.BUTTONS_OK,
                "You don't have any profile, please crete your profile."
            )
            response = dialog.run()
            if response:
                dialog.destroy()

            return None


        if active < 0:
            dialog = gtk.MessageDialog(
                self.window,
                gtk.DIALOG_MODAL,
                gtk.MESSAGE_WARNING,
                gtk.BUTTONS_OK,
                "Select a profile!"
            )
            response = dialog.run()
            if response:
                dialog.destroy()

            return None

        return model[active][1]


if __name__ == '__main__':
    otp_generator = OTPGenerator()
    otp_generator.main()



