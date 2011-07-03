#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import time
import md5

class OTPGenerator:
    
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('OTP Generator')
        self.window.connect('destroy', lambda x: gtk.main_quit())
        self.window.set_border_width(0)

        ui = """
            <ui>
                <menubar name="MenuBar">
                    <menu action="Application">
                        <menuitem action="Account" />
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
                ("Application", None, "A_pplication", None, None, None),
                ("Account", None, "_Account", "<control>a", "Account Setting", self.account),
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

        self.content = gtk.VBox(False)

        self.secret_key = '1234567890123456'
        pin_label = gtk.Label('Pin')
        self.content.pack_start(pin_label, False, False, 3)
        pin_label.show()

        self.pin_entry = gtk.Entry(4)
        self.pin_entry.set_text("0000")
        self.content.pack_start(self.pin_entry, False, False, 3)
        self.pin_entry.show()

        self.generate_button = gtk.Button('Generate')
        self.generate_button.connect('clicked', self.generate_otp)
        self.content.pack_start(self.generate_button, False, False, 3)
        self.generate_button.show()
        

        self.result_label = gtk.Label('')
        self.content.pack_start(self.result_label, False, False, 3)
        self.result_label.show()

        self.content.show()
        container.pack_start(self.content, True, True, 12)
        self.window.add(container)

    def generate_otp(self, widget, data = None):

        # generate epoch number
        #  int(time.time()) convert time to int to remove decimal digit
        # int(time.time()) / 10 to remove 1 last digit
        epoch = str(int(time.time()) / 10)

        # print "epoch: " + epoch
        # print "secret key: " + self.secret_key
        # print "pin: " + self.pin_entry.get_text()

        md = md5.new()
        md.update(epoch + self.secret_key + self.pin_entry.get_text())
        result = md.hexdigest()
        self.result_label.set_text(result[0:6])

    def main(self):
        self.window.show()
        gtk.main()

if __name__ == '__main__':
    otp_generator = OTPGenerator()
    otp_generator.main()



