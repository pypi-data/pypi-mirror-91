#!/usr/bin/env python3
"""
krapplet: A password manager written as a gnome-keyring applet
krapplet.py is the main program
(c) 2020-2021 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

BSD_LICENSE = """Copyright 2020-2021 Johannes Willem Fernhout <hfern@fernhout.info>. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this
   list of conditions and the following disclaimer in the documentation and/or
   other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

# standard Python modules
import sys
import os
import signal
import string
import secrets
import random
import locale
import webbrowser
import subprocess
from datetime import datetime


# Non-Python dependencies. Not sure if they are installed
# import GTK3
try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib, Gdk
except:
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent", file=sys.stderr)
    sys.exit(1)

# import secretstorage, the Python API for gnome-keyring
try:
    import secretstorage
except:
    sys.stderr.write("Please install the secretstorage package", file=sys.stderr)
    sys.exit(2)

# application constants:
APP_response_delete = 1
FRAME_LABEL_XALIGN  = 0.025
APP_EMBED_TIMEOUT   = 5000                       # 5 seconds
pw_special_chars = "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
iconname = "krapplet"
#icon_filename_48x48 = "resources/krapplet-key-icon-48x48.png"
#icon_filename_96x96 = "resources/krapplet-key-icon-96x96.png"


# utility functions:
def add_item2menu( mnu=None, label=None, action=None, data=None):
    """ adds a menuitem to a menu (mnu), optionally with an activate action
        and data to be passed to the action """
    if  mnu == None or label == None:
        print( "add_item2menu: mnu nor label can be None" )
        raise AssertionError
    mni =  Gtk.MenuItem( label=label )
    if action:
        if data:
            mni.connect( "activate", action, data )
        else:
            mni.connect( "activate", action )
    mnu.append( mni )

def add_separator2menu( mnu ):
     "add_separator2menu: adds a separator to a menu """
     mni =  Gtk.SeparatorMenuItem()
     mnu.append( mni )


def show_info_or_error_message( active_widget, primary_msg, secondary_msg, msg_type, title, buttons ):
    """Shows an error or info  message dialog"""
    dialog = Gtk.MessageDialog( title=title, transient_for=active_widget, flags=0, 
                                message_type=msg_type, buttons=buttons, text=primary_msg)
    if secondary_msg:
        dialog.format_secondary_text( secondary_msg )
    dialog.run()
    dialog.destroy()

def show_error_message( active_widget, primary_msg, secondary_msg ):
    """Shows an error message dialog"""
    show_info_or_error_message( active_widget, primary_msg, secondary_msg, 
                                Gtk.MessageType.ERROR, "ERROR", Gtk.ButtonsType.CLOSE )
"""
    dialog = Gtk.MessageDialog( title="ERROR", transient_for=active_widget, flags=0, 
                                message_type=Gtk.MessageType.ERROR, 
                                buttons=Gtk.ButtonsType.CLOSE, text=primary_msg)
    if secondary_msg:
        dialog.format_secondary_text( secondary_msg )
    dialog.run()
    dialog.destroy() """

def show_info_message( active_widget, primary_msg, secondary_msg ):
    """ Shows an informational message dialog """
    show_info_or_error_message( active_widget, primary_msg, secondary_msg, 
                                Gtk.MessageType.INFO, "Informational", Gtk.ButtonsType.CLOSE )
"""
    dialog = Gtk.MessageDialog( title="Informational", transient_for=active_widget, flags=0, 
                                message_type=Gtk.MessageType.INFO, 
                                buttons=Gtk.ButtonsType.CLOSE, text=primary_msg,)
    if secondary_msg:
        dialog.format_secondary_text( secondary_msg )
    dialog.run()
    dialog.destroy() """

def abs_path(rel_path):
    """ returns the absolute path for a file, given the relative path to this ,py file """
    packagedir = os.path.dirname( __file__ )
    joinedpath = os.path.join( packagedir, rel_path )
    path =  os.path.abspath( joinedpath )
    return path

def icon_path( iconname, res ):
    """ finds the path to an icon, based on std Gtk functions, so looking in standard 
    locations like $HOME/.icons, $XDG_DATA_DIRS/icons, and /usr/share/pixmaps """
    icon_theme = Gtk.IconTheme.get_default()
    icon = icon_theme.lookup_icon( iconname, res, 0)
    if icon:
        path = icon.get_filename()
        return path
    else:
        return ""
    
def copy_text2clipboard( txt ):
    """ copy_text2clipboard copies the txt parameter to the cliboard """
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text( txt, -1 )

def timestamp( since_epoch ):
    """returns a string according to local locale based on seconds since epoch 1-JAN-1970"""
    if since_epoch:
        dt = datetime.fromtimestamp( since_epoch )
        dstr = dt.strftime( locale.nl_langinfo( locale.D_T_FMT ))
        return dstr
    else:
        return ""

def int2( str ):
    try:
        return int( str )
    except:
        return 0

def sigint_handler(sig, frame):
    """ Signal handler for SIGINT, or Ctrl-C, to avoid standard Python stack dump """
    print( "Signal", sig, "received, terminating" )
    Gtk.main_quit()

#class NewPasswordDialog(Gtk.Dialog):
class PasswordGeneratorDialog(Gtk.Dialog):
    """ NewPasswordDialog: dialog window to generate a new password """
    def __init__(self, parent ):
        Gtk.Dialog.__init__( self, title="Generate password", flags=0)
        self.add_buttons( Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                          Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.tot_len = 12
        self.AZ_len = self.az_len = self.nm_len = self.sp_len = 2
        self.show_window()
        self.set_transient_for( parent )

    def show_window( self ):
        """ show_window builds up a window based on the values i
            of self.new_keyname/new_attribs/new_secret """
        self.set_default_size(100, 100)
        box = self.get_content_area()
        frame = Gtk.Frame( label="Parameters", label_xalign=FRAME_LABEL_XALIGN  )
        box.add( frame )
        self.grid = Gtk.Grid( row_spacing=2, column_spacing=5 ) 
        frame.add( self.grid )

        prompt_length = Gtk.Label( label="Total length", xalign=0 )
        self.entry_lenght = Gtk.Entry( text=str(self.tot_len), input_purpose=Gtk.InputPurpose.DIGITS, xalign=0, width_request=3 )
        self.entry_lenght.connect( "insert_text", self.validate, 2 )
        prompt_AZ = Gtk.Label( label="Uppercase", xalign=0 )
        self.entry_AZ =  Gtk.Entry( text=str(self.AZ_len), input_purpose=Gtk.InputPurpose.DIGITS, xalign=0 )
        self.entry_AZ.connect( "insert_text", self.validate, 2 )
        prompt_az = Gtk.Label( label="Lowercase", xalign=0 )
        self.entry_az =  Gtk.Entry( text=str(self.az_len), input_purpose=Gtk.InputPurpose.DIGITS, xalign=0 )
        self.entry_az.connect( "insert_text", self.validate, 2 )
        prompt_nm = Gtk.Label( label="Numeric", xalign=0 )
        self.entry_nm =  Gtk.Entry( text=str(self.nm_len), input_purpose=Gtk.InputPurpose.DIGITS, xalign=0 )
        self.entry_nm.connect( "insert_text", self.validate, 2 )
        prompt_sp = Gtk.Label( label="special", xalign=0 )
        self.entry_sp =  Gtk.Entry( text=str(self.sp_len), input_purpose=Gtk.InputPurpose.DIGITS, xalign=0 )
        self.entry_sp.connect( "insert_text", self.validate, 2 )
        empty_line = Gtk.Label()

        self.grid.attach_next_to( prompt_length, None, Gtk.PositionType.BOTTOM, 1, 1 )
        self.grid.attach_next_to( self.entry_lenght, prompt_length, Gtk.PositionType.RIGHT, 1, 1 )
        self.grid.attach_next_to( prompt_AZ, prompt_length, Gtk.PositionType.BOTTOM, 1, 1 )
        self.grid.attach_next_to( self.entry_AZ, prompt_AZ, Gtk.PositionType.RIGHT, 1, 1 )
        self.grid.attach_next_to( prompt_az, prompt_AZ, Gtk.PositionType.BOTTOM, 1, 1 )
        self.grid.attach_next_to( self.entry_az, prompt_az, Gtk.PositionType.RIGHT, 1, 1 )
        self.grid.attach_next_to( prompt_nm, prompt_az, Gtk.PositionType.BOTTOM, 1, 1 )
        self.grid.attach_next_to( self.entry_nm, prompt_nm, Gtk.PositionType.RIGHT, 1, 1 )
        self.grid.attach_next_to( prompt_sp, prompt_nm, Gtk.PositionType.BOTTOM, 1, 1 )
        self.grid.attach_next_to( self.entry_sp, prompt_sp, Gtk.PositionType.RIGHT, 1, 1 )
        box.add( empty_line )
        self.show_all()

    def update_from_window( self ):
        self.tot_len = int2( self.entry_lenght.get_text())
        self.AZ_len  = int2( self.entry_AZ.get_text())
        self.az_len  = int2( self.entry_az.get_text())
        self.nm_len  = int2( self.entry_nm.get_text())
        self.sp_len  = int2( self.entry_sp.get_text())
        
    def validate( self, widget, new_text, new_text_length, position, maxlen ):
        """ validates keyboard input for numberic, and nrof digits, and
            enables/disables the OK button based on the input given"""
        field_contents = widget.get_text()
        newpos = widget.get_position() 
        if new_text.isnumeric() and (new_text_length + len(field_contents)) <= maxlen:
            field_contents = field_contents[:newpos] + new_text + field_contents[newpos:]
        widget.handler_block_by_func( self.validate )
        widget.set_text( field_contents )
        widget.handler_unblock_by_func( self.validate )
        GLib.idle_add(widget.set_position, newpos+1)
        widget.stop_emission_by_name( "insert_text" )
        self.update_from_window()
        enabled = (self.tot_len >= (self.AZ_len + self.az_len + self.nm_len + self.sp_len)) and \
                  (self.AZ_len or self.az_len or self.nm_len or self.sp_len)
        self.set_response_sensitive( Gtk.ResponseType.OK, enabled )

    def generate_new_password( self ):

        def part_passwd( length, chars ):
            """passwd create string of random chars from a set of chars"""
            pw = ""
            for i in range(length):
                pw += secrets.choice( chars )
            return pw
            
        def shuffle_word(word):
            """shuffle_word shuffles the letters of a word"""
            word = list(word)
            random.shuffle(word)
            return ''.join(word)

        self.update_from_window()
        ex_len       = self.tot_len - self.AZ_len - self.az_len - self.nm_len - self.sp_len

        AZ_str = part_passwd( self.AZ_len, string.ascii_uppercase )
        az_str = part_passwd( self.az_len, string.ascii_lowercase )
        nm_str = part_passwd( self.nm_len, string.digits )
        sp_str = part_passwd( self.sp_len, pw_special_chars )
        ex_str = ""
        if ex_len > 0:
            if self.AZ_len: ex_str += string.ascii_uppercase
            if self.az_len: ex_str += string.ascii_lowercase
            if self.nm_len: ex_str += string.digits
            if self.sp_len: ex_str += pw_special_chars
            ex_str = part_passwd( ex_len, ex_str )
        pw = shuffle_word( AZ_str + az_str + nm_str + sp_str + ex_str )
        return pw


class KeyDialog(Gtk.Dialog):
    """ KeyDialog: shows a dialog window for keys """
    def __init__(self, parent, key ):
        Gtk.Dialog.__init__( self, title="Edit key", flags=0 )
        self.add_buttons( Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                          Gtk.STOCK_DELETE, APP_response_delete,
                          Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.key = key
        self.extra_attribs = 0
        if self.key:
            self.old_keyname = self.new_keyname = key.get_label()
            self.old_attribs = self.new_attribs = key.get_attributes()
            self.old_secret  = self.new_secret  = key.get_secret().decode("utf-8") 
            self.old_created = key.get_created()
            self.old_modified= key.get_modified()
        else:
            self.old_keyname = self.new_keyname = "New key"
            self.old_attribs = self.new_attribs = {}
            self.new_attribs[ "URL" ] = "https://"
            self.new_attribs[ "username" ] = ""
            self.old_secret  = self.new_secret  = ""
            self.old_created = self.old_modified = 0
        self.secret_visibilty = False
        self.box = None
        self.show_window()

    def show_window( self ):
        """ KeyDialog.show_window builds up a window based on the values i
            of self.new_keyname/new_attribs/new_secret """
        self.set_default_size(150, 100)
        content_area = self.get_content_area()
        if self.box:
            self.box.destroy()
        self.box = Gtk.Box( orientation = Gtk.Orientation.VERTICAL )
        content_area.add( self.box )
        key_frame = Gtk.Frame( label="Key", label_xalign=FRAME_LABEL_XALIGN )
        key_grid = Gtk.Grid( row_spacing=2, column_spacing=5 ) 
        self.box.add( key_frame ) 
        key_frame.add( key_grid )

        self.newkey_entry = Gtk.Entry( text=self.new_keyname,xalign=0 )
        self.newkey_entry.set_max_width_chars( 64 )
        key_grid.attach_next_to( self.newkey_entry, None, Gtk.PositionType.RIGHT, 2, 1 )
        last_prompt = self.newkey_entry

        if self.old_created:
            created_prompt =  Gtk.Label( label=" Created", xalign=0 )
            created_value  =  Gtk.Label( label=timestamp( self.old_created), xalign=0)
            key_grid.attach_next_to( created_prompt, last_prompt, Gtk.PositionType.BOTTOM, 1, 1 )
            key_grid.attach_next_to( created_value, created_prompt,  Gtk.PositionType.RIGHT, 1, 1 )
            modified_prompt =  Gtk.Label( label=" Modified", xalign=0 )
            modified_value  =  Gtk.Label( label=timestamp( self.old_modified ), xalign=0)
            key_grid.attach_next_to( modified_prompt, created_prompt, Gtk.PositionType.BOTTOM, 1, 1 )
            key_grid.attach_next_to( modified_value, modified_prompt, Gtk.PositionType.RIGHT, 1, 1 )
            last_prompt = modified_prompt

        self.box.add( Gtk.Label())
        attr_frame = Gtk.Frame( label="Attributes", label_xalign=FRAME_LABEL_XALIGN )
        attr_grid = Gtk.Grid( row_spacing=2, column_spacing=5 ) 
        self.box.add( attr_frame )
        attr_frame.add( attr_grid )
        self.attr_prompt = {}
        self.attr_value  = {}
        last_prompt = None
        launch_button_active = False
        for attr in self.new_attribs:
            if  attr != "xdg:schema":
                self.attr_prompt[attr] = Gtk.Entry( text=attr, xalign=0, max_width_chars=20 )
                self.attr_prompt[attr].set_max_width_chars( 20 )
                self.attr_value[attr]  = Gtk.Entry( text=self.new_attribs[ attr ], xalign = 0 )
                self.attr_value[attr].set_max_width_chars( 42 )
                attr_grid.attach_next_to( self.attr_prompt[attr], last_prompt, Gtk.PositionType.BOTTOM, 1, 1 )
                attr_grid.attach_next_to( self.attr_value[attr], self.attr_prompt[attr], Gtk.PositionType.RIGHT, 1, 1 )
                if attr == "URL":
                    launch_button_active = True
                last_prompt = self.attr_prompt[attr]
                last_entry  = self.attr_value[attr]
        if self.extra_attribs:
            self.extra_attr_prompt = Gtk.Entry( xalign = 0 )
            self.extra_attr_prompt.set_max_width_chars( 20 )
            self.extra_attr_entry  = Gtk.Entry( xalign = 0 )
            self.extra_attr_entry.set_max_width_chars( 42 )
            attr_grid.attach_next_to( self.extra_attr_prompt, last_prompt, Gtk.PositionType.BOTTOM, 1, 1 )
            attr_grid.attach_next_to( self.extra_attr_entry, self.extra_attr_prompt, Gtk.PositionType.RIGHT, 1, 1 )
            last_prompt = self.extra_attr_prompt
            last_entry  = self.extra_attr_entry
        attr_button_box = Gtk.Box()
        if launch_button_active:
            launch_button = Gtk.Button(label="Launch" )
            launch_button.connect( "clicked", self.launch )
            attr_button_box.pack_end( launch_button, False, False, 0 )
        add_button = Gtk.Button(label="Add" )
        add_button.connect( "clicked", self.add_attr )
        attr_button_box.pack_end( add_button, False, False, 2 )
        attr_grid.attach_next_to( attr_button_box, last_prompt, Gtk.PositionType.BOTTOM, 2, 1 )

        self.box.add( Gtk.Label())
        secr_frame = Gtk.Frame( label="Secret", label_xalign=FRAME_LABEL_XALIGN )
        secr_grid = Gtk.Grid( row_spacing=2, column_spacing=5 ) 
        self.box.add( secr_frame )
        secr_frame.add( secr_grid )
        self.secret_value = Gtk.Entry( text=self.new_secret, xalign=0, visibility=self.secret_visibilty )
        self.secret_value.set_max_width_chars( 64 )

        secret_copy_button = Gtk.Button(label="Copy" )
        secret_copy_button.connect( "clicked", self.copy_secret2clipboard )
        visi_text = "Hide" if self.secret_visibilty else "Show"
        visi_button = Gtk.Button(label=visi_text )
        visi_button.connect( "clicked", self.toggle_secret_visibility )
        gen_button = Gtk.Button(label="Generate")
        gen_button.connect( "clicked", self.generate_password )
        secret_promptbox = Gtk.Box(spacing=2)
        secret_promptbox.pack_end( visi_button, False, False, 0)
        secret_promptbox.pack_end( secret_copy_button, False, False, 0)
        secret_promptbox.pack_end( gen_button, False, False, 0)

        secr_grid.attach_next_to( self.secret_value, None, Gtk.PositionType.RIGHT, 1, 1 )
        secr_grid.attach_next_to( secret_promptbox, self.secret_value, Gtk.PositionType.BOTTOM, 1, 1 )
        last_prompt = secret_promptbox
        emptyline = Gtk.Label()
        self.box.add( emptyline )
        self.show_all()

    def generate_password( self, button ):
        """ action function for generate password """
        self.update_key_from_window()
        self.active_widget = dialog = PasswordGeneratorDialog( self )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.new_secret = dialog.generate_new_password()
        dialog.destroy()
        self.active_widget = self
        self.secret_visibilty = False
        self.show_window()

    def launch( self, button ):
        """ tries to find an attrib["URL"] and lauches it in a webbrowser """
        self.update_key_from_window()
        url = self.new_attribs["URL"]
        webbrowser.open( url, new=0, autoraise=True) 

    def update_key_from_window( self ):
        """ copies the values from screen to internal structures """
        self.new_keyname = self.newkey_entry.get_text()
        screen_attribs = {}
        for attr in self.new_attribs:
            if  attr != "xdg:schema":
                prompt = self.attr_prompt[attr].get_text()
                if prompt != "":
                    value  = self.attr_value[attr].get_text()
                    screen_attribs[prompt] = value
        if self.extra_attribs:
            prompt = self.extra_attr_prompt.get_text()
            if prompt != "":
                value  = self.extra_attr_entry.get_text()
                screen_attribs[prompt] = value
            self.extra_attribs = False
        self.new_secret = self.secret_value.get_text()
        self.new_attribs = screen_attribs
            
    def toggle_secret_visibility( self, button ):
        """ toggles the visibiity of the password """
        self.update_key_from_window()
        self.secret_visibilty = not self.secret_visibilty
        self.show_window()


    def add_attr( self, button ):
        """ adds an attribute line to the window """
        self.update_key_from_window()
        self.extra_attribs = True
        self.show_window()

    def copy_secret2clipboard( self, widget ):
        self.update_key_from_window()
        copy_text2clipboard( self.new_secret )

    def deletekey( self):
        self.key.delete()

    def savekey( self):
        self.update_key_from_window()
        if self.old_keyname != self.new_keyname:
            self.key.set_label(self.new_keyname)
        if self.old_attribs != self.new_attribs:
            self.key.set_attributes(self.new_attribs)
        if self.old_secret  != self.new_secret:
            self.key.set_secret( self.new_secret.encode("utf-8"))

    def create_newkey( self, collection):
        self.update_key_from_window()
        self.key = collection.create_item( label=self.new_keyname, 
                                           attributes=self.new_attribs, 
                                           secret=self.new_secret.encode("utf-8"))


class AddKeyRingDialog(Gtk.Dialog):
    """ AddKeyRingDialog: window class to add a keyring, prompts for keyring name """
    def __init__(self, parent ):
        Gtk.Dialog.__init__( self, title="New keyring", flags=0 )
        self.add_buttons( Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                          Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        box = self.get_content_area()
        keyringname_prompt = Gtk.Label( label="Keyring name", xalign=0)
        self.keyringname_input  = Gtk.Entry( text="New keyring", xalign = 0 )
        grid = Gtk.Grid( row_spacing=2, column_spacing=5 ) 
        box.add( grid )
        grid.attach_next_to( keyringname_prompt, None, Gtk.PositionType.BOTTOM, 1, 1 )
        grid.attach_next_to( self.keyringname_input, keyringname_prompt, Gtk.PositionType.RIGHT, 1, 1 )
        self.set_position( Gtk.WindowPosition.MOUSE )
        self.show_all()

    def get_newkeyringname( self ):
        """ get_newkeyringname: returns the entered name for a new keyring"""
        return self.keyringname_input.get_text() 

class StatusIcon:
    """Main entry point, creates a tray icon, and handles rightclicks"""
    def __init__(self):
        self.dbus_open = False
        self.statusicon = Gtk.StatusIcon()
        self.statusicon.set_from_file( icon_path( iconname, 48 ))
        self.statusicon.connect("popup-menu", self.right_click_event)
        self.statusicon.set_title( "Password manager" )
        self.statusicon.set_tooltip_text( "krapplet: a password manager" )
        self.statusicon.set_visible( True )
        self.embedded = False
        GLib.idle_add( self.embed_check )
        GLib.timeout_add( APP_EMBED_TIMEOUT, self.embed_timeout )
        self.active_widget = None
        #self.statusicon.set_name( "krapplet" )    # Issue https://gitlab.com/hfernh/krapplet/-/issues/22

    def embed_check( self ):
        """ keep calling until we are embedded """
        if self.statusicon.is_embedded():
            self.embedded = True
            return False                    # don't call again
        return True

    def embed_timeout( self ):
        """ if still not emebedded then exit program """
        if self.embedded:
            return False                    # don't call again
        else:
            print( "Error: could not embed in systray", file=sys.stderr)
            Gtk.main_quit()
            return True

    def right_click_event(self, icon, button, time):
        """ shows the popop menu """
        if self.active_widget:              # is there is an active window then put 
            self.active_widget.present()    # focus on it, rather then display a new one
            return
        if self.dbus_open:
            self.connection.close()
        self.connection = secretstorage.dbus_init()
        self.dbus_open = True
        self.menu = Gtk.Menu() 
        self.collections = secretstorage.get_all_collections( self.connection )
        for collection in self.collections:
            collection_label = collection.get_label()
            if len(collection_label):                  # sometime we encounter empty keyrings, ignore them
                item = Gtk.MenuItem( label=collection_label )
                submenu = Gtk.Menu()
                if collection.is_locked():
                    add_item2menu( mnu=submenu, label="Unlock", action=self.unlock_keyring, data=collection)
                else:
                    nrof_keys = 0
                    try:
                        for key in collection.get_all_items():
                            if key.is_locked():
                                lock_return = key.unlock()
                            add_item2menu( mnu=submenu, label=key.get_label(), action=self.key_dialog, data=key )
                            nrof_keys += 1

                    except secretstorage.exceptions.ItemNotFoundException:     # sometimes gnome-keyring gets confused
                        show_error_message( self.active_widget, "Item not found exception", 
                                                                "Restarting gnome-keyring; this will lock all keyrings" )
                        msg = subprocess.check_output( ["gnome-keyring-daemon", "-r", "-d"], stderr=subprocess.STDOUT )
                        show_info_message( self.active_widget, "Output of gnome-restart command", msg.decode("utf-8"))
                    except:
                        show_error_message( self.active_widget, 
                                            "Unexpected error occured, please report this error", sys.exc_info()[0])
                    if nrof_keys: 
                        add_separator2menu( submenu )
                    add_item2menu( mnu=submenu, label="Add key", action=self.add_key, data=collection )
                    add_item2menu( mnu=submenu, label="Remove keyring", action=self.remove_keyring, data=collection )
                    add_item2menu( mnu=submenu, label="Lock keyring", action=self.lock_keyring, data=collection )
                item.set_submenu( submenu )
                self.menu.append(item)
        add_separator2menu( self.menu )
        add_item2menu( mnu=self.menu, label="Add keyring", action=self.add_keyring, data=None )
        add_item2menu( mnu=self.menu, label="About", action=self.show_about_dialog, data=None )
        add_item2menu( mnu=self.menu, label="Quit", action=Gtk.main_quit, data=None )
        self.menu.show_all()
        self.menu.popup(None, None, None, self.statusicon, button, time)

    def unlock_keyring( self, widget, collection):
        """Unocks a keyring"""
        collection.unlock()

    def lock_keyring( self, widget, collection):
        """Locks a keyring"""
        collection.lock()

    def remove_keyring( self, widget, collection):
        """Removes a keyring, when it is empty. If not it shows an error message"""
        keycount = 0
        for key in collection.get_all_items():
            keycount += 1
        if keycount:
            show_error_message( self.active_widget, 
                                "Error deleting  keyring", 
                                "Keys are still attached to keyring" )
        else:
            collection.delete()

    def key_dialog( self, widget, key ):
        """Pops up a window showing a key, with all the attribs"""
        self.active_widget = dialog = KeyDialog( self, key )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.savekey()
        elif response == APP_response_delete:
            dialog.deletekey()
        copy_text2clipboard( "" )
        dialog.destroy()
        self.active_widget = None

    def add_key( self, widget, collection):
        """Add_key adds a key to a keyrng"""
        self.active_widget = dialog = KeyDialog( self, None )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.create_newkey( collection )
        dialog.destroy() 
        self.active_widget = None

    def add_keyring( self, widget ):
        """Pops up a window asking for a new keyring name"""
        self.active_widget = dialog = AddKeyRingDialog( self )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            keyringname = dialog.get_newkeyringname()
            try:
                secretstorage.create_collection( self.connection, keyringname )
            except Exception as e:
                show_error_message( self.active_widget, "Error saving new keyring", str( e ))
        dialog.destroy()
        self.active_widget = None

    def show_about_dialog(self, widget):
        """Shows the about dialog"""
        image = Gtk.Image()
        #image.set_from_file( abs_path( icon_filename_96x96 ))
        image.set_from_file( icon_path( iconname, 96 ))
        icon_pixbuf = image.get_pixbuf()

        self.active_widget = about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_logo( icon_pixbuf )
        about_dialog.set_program_name( "krapplet" )
        about_dialog.set_version( "Version 0.2.0" )
        about_dialog.set_comments("A password manager written as a gnome-keyring applet")
        about_dialog.set_authors(["Johannes Willem Fernhout"])
        about_dialog.set_copyright( "(c) 2020-2021 Johannes Willem Fernhout" )
        about_dialog.set_license( BSD_LICENSE )
        about_dialog.set_website("https://gitlab.com/hfernh/krapplet")
        about_dialog.set_website_label("krapplet on GitLab")
        about_dialog.show_all()
        about_dialog.run()
        about_dialog.destroy()
        self.active_widget = None

    def __del__(self):
        """ exit code, just some housekeeping """
        if self.dbus_open:
            self.connection.close() 



def main():
    """ krapplet main """
    # ignore GTK deprecation warnings gwhen not in development mode
    # for development mode, run program as python3 -X dev krapplet
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    ico = StatusIcon()
    signal.signal(signal.SIGINT, sigint_handler)
    Gtk.main()

if __name__ == "__main__":
    main()
