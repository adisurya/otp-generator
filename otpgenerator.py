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
        self.window.set_border_width(12)
        self.main_box = gtk.VBox(False)

        self.secret_key = '1234567890123456'
        pin_label = gtk.Label('Pin')
        self.main_box.pack_start(pin_label, False, False, 3)
        pin_label.show()

        self.pin_entry = gtk.Entry(4)
        self.pin_entry.set_text("0000")
        self.main_box.pack_start(self.pin_entry, False, False, 3)
        self.pin_entry.show()

        self.generate_button = gtk.Button('Generate')
        self.generate_button.connect('clicked', self.generate_otp)
        self.main_box.pack_start(self.generate_button, False, False, 3)
        self.generate_button.show()
        

        self.result_label = gtk.Label('')
        self.main_box.pack_start(self.result_label, False, False, 3)
        self.result_label.show()

        self.main_box.show()
        self.window.add(self.main_box)

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



