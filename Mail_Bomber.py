import os
import pygubu
from tkinter import ttk, filedialog, messagebox
from tkinter import *
from Add_Email import AddEmail
from Indicator import Indicator
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
# import time

PROJECT_PATH = os.path.dirname( __file__ )
PROJECT_UI = os.path.join( PROJECT_PATH, "UI/mail_bomber.ui" )


class MailBomber:

    def __init__( self ):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path( PROJECT_PATH )
        builder.add_from_file( PROJECT_UI )
        self.mainwindow = builder.get_object( 'mainwindow' )
        self.mainwindow.title( "Mail Bomber" )
        self.mainwindow.tk.call(
            "wm", "iconphoto", self.mainwindow._w, PhotoImage( file="images/icon.png" )
            )
        builder.connect_callbacks( self )
        self.set_variables()
        self.get_widget_objects()
        self.config()
        self.fill_start_end()
        # self.indi()

    def set_variables( self ):
        self.path = "Email_List.db"

    def config( self ):

        self.s_w = self.mainwindow.winfo_screenwidth()
        self.s_h = self.mainwindow.winfo_screenheight()
        self.wow = 700
        self.how = 580
        x_c = ( ( self.s_w / 2 ) - ( self.wow / 2 ) )
        y_c = ( ( self.s_h / 2 ) - ( self.how / 2 ) )
        self.mainwindow.geometry( "%dx%d+%d+%d" % ( self.wow, self.how, x_c, y_c ) )

        self.style = ttk.Style( self.mainwindow )
        # print( self.style.theme_names() )
        # self.style.theme_use( "winnative" )
        self.style.configure(
            "TLabelframe", background="#44ccff", highlightthickness=5, relief="flat"
            )
        self.style.configure( "TFrame", background="#44ccff", highlightthickness=5, relief="flat" )
        self.style.configure(
            "TLabelframe.Label",
            background="#081944",
            foreground="#ffffff",
            font=( 'Arial', 14, 'bold' ),
            width=self.wow,
            anchor="center",
            relief="flat"
            )
        self.style.configure(
            "Treeview",
            fieldbackground="#ffffff",
            background="#ffffff",
            foreground="#000000",
            font=( "Arial", 11, "bold" ),
            borderwidth=5,
            relief="flat"
            )
        self.style.configure( "Treeview.Heading", font=( "Arial", 12, "bold" ) )

        self.style.configure(
            "TButton",
            background="#ffffff",
            foreground="#000000",
            font=( "Arial", 11, "bold" ),
            relief="flat",
            highlightthickness=5,
            padding=5,
            highlightcolor="blue",
            bordercolor="#000000",
            takefocus=True,
            width=12
            )
        # self.style.map( "TButton", background=[ ( 'active', 'blue' ) ] )
        self.style.configure(
            "TLabel",
            padding=2,
            font=( "Arial", 11, "bold" ),
            relief="flat",
            width=14,
            takefocus=False,
            borderwidth=3,
            cursor="arrow",
            anchor="center"
            )

        self.style.configure(
            "TEntry", fieldbackground="#99ddff", font=( "Arial", 11, "bold" ), width=40
            )
        self.attachment_e.config( state="readonly" )
        self.background_img_e.config( state="readonly" )
        self.background = []
        self.to_l.config( width=5 )

        # self.company_LB.heading("#0", text="Company")
    def fill_start_end( self ):
        self.start_e.delete( 0, 'end' )
        self.start_e.insert( 0, '0' )
        self.checkORcreate()
        Emails = self.email_list_DB.execute( "select email from emails" ).fetchall()
        self.email_list_DB.close()
        self.end_e.delete( 0, 'end' )
        self.end_e.insert( 0, str( len( Emails ) ) )

    def get_widget_objects( self ):
        self.mail_bomber_f = self.builder.get_object( "mail_bomber_f" )
        self.email_e = self.builder.get_object( "email_e" )
        self.password_e = self.builder.get_object( "password_e" )
        self.subject_e = self.builder.get_object( "subject_e" )
        self.attachment_e = self.builder.get_object( "attachment_e" )
        self.message_e = self.builder.get_object( "message_e" )
        self.background_img_e = self.builder.get_object( "background_img_e" )
        self.start_e = self.builder.get_object( "start_e" )
        self.end_e = self.builder.get_object( "end_e" )
        self.to_l = self.builder.get_object( "to_l" )

        pass

    def get_widget_values( self ):
        self.email = self.email_e.get()
        self.password = self.password_e.get()
        self.subject = self.subject_e.get()
        self.attachment = self.attachment_e.get()
        # self.background = self.background_img_e.get()
        self.message = self.message_e.get( "1.0", "end" )
        self.start = self.start_e.get()
        self.end = self.end_e.get()

    def add_attachment( self, event=None ):
        self.filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=( ( "all files", "*.*" ), ( "jpeg files", "*.jpg" ) )
            )
        print( self.filename )
        self.attachment_e.config( state="enabled" )
        self.attachment_e.insert( 0, self.filename )
        self.attachment_e.config( state="readonly" )
        pass

    def add_background( self, event=None ):
        self.background.append(
            filedialog.askopenfilename(
                initialdir="/home/blackthunder/Downloads",
                title="Select file",
                filetypes=(
                    ( "image files", ".jpg .png .jpeg .PNG .JPG .JPEG .gif .GIF" ),
                    ( "all files", "*.*" )
                    )
                )
            )
        print( self.background )
        self.background_img_e.config( state="enabled" )
        self.background_img_e.insert( 0, ';'.join( self.background ) )
        self.background_img_e.config( state="readonly" )
        pass

    def close( self ):
        self.mainwindow.destroy()

    def checkORcreate( self ):
        self.email_list_DB = sqlite3.connect( "Email_List.db" )
        self.email_list_DB.execute( """create table if not exists emails (email text)""" )
        if not os.path.exists( "Message.txt" ):
            messagefile = open( "Message.txt", "w" )
            messagefile.write( "Hello {}" )
            messagefile.close()

    def only_email( self ):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if ( re.search( regex, self.email ) ):
            return True
        else:
            return False

        pass

    def only_digits( self, key, string ):
        key = key[ :-1 ]
        # print(key, string)
        if key.isdigit():
            return True
        elif key == "":
            return True
        else:
            return False

    def send( self ):
        self.get_widget_values()
        self.fill_start_end()
        # self.disable()
        if self.only_email():

            # indicator = Indicator(self.mainwindow)
            # indicator.config(self.start, self.end)

            self.checkORcreate()
            Emails = self.email_list_DB.execute(
                "select email from emails where rowid between ? and ?", ( self.start, self.end )
                ).fetchall()
            self.email_list_DB.close()
            print( Emails )

            fromaddr = self.email
            # toaddr = "EMAIL address of the receiver"

            # instance of MIMEMultipart
            msgroot = MIMEMultipart( "related" )

            # storing the senders email address
            msgroot[ 'From' ] = fromaddr

            # storing the receivers email address

            # storing the subject
            msgroot[ 'Subject' ] = self.subject

            # string to store the body of the mail
            body = self.message
            with open( "Message.txt", 'r' ) as f:
                temp = f.readlines()
                # print(message.format(body))
            for i in range( 0, len( self.background ) ):
                if not self.background[ i ] == '':
                    temp[ 0 ] = temp[ 0 ] + "<img src='cid:image{}'>".format( str( i ) )

            message = ''.join( temp )
            # print(message)

            # attach the body with the msg instance
            # msgroot.attach( MIMEText( body, 'plain' ) )

            msgalt = MIMEMultipart( "alternative" )
            msgroot.attach( msgalt )
            # msgalt.attach( MIMEText( r"<b>some <i>WELLTECH Minerals</i><br>{}</b><br><img src='cid:image1'>".format(body), 'html' ) )
            msgalt.attach( MIMEText( message.format( body ), 'html' ) )

            # open the file to be sent
            if not self.attachment == '':
                filename = self.attachment.split( '/' )[ -1 ]
                attachment = open( self.attachment, "rb" )

                # instance of MIMEBase and named as p
                p = MIMEBase( 'application', 'octet-stream' )

                # To change the payload into encoded form
                p.set_payload( ( attachment ).read() )

                # encode into base64
                encoders.encode_base64( p )

                p.add_header( 'Content-Disposition', "attachment; filename= %s" % filename )

                # attach the instance 'p' to instance 'msg'
                msgroot.attach( p )

            for i in range( 0, len( self.background ) ):
                if not self.background[ i ] == '':
                    backgroundimg = open( self.background[ i ], "rb" )
                    msgimg = MIMEImage( backgroundimg.read() )
                    backgroundimg.close()
                    ID = "<image{}>".format( str( i ) )
                    msgimg.add_header( "Content-ID", ID )
                    msgroot.attach( msgimg )

            if os.path.exists( "images/logo.png" ):
                logo = open( "images/logo.png", "rb" )
                msgimg = MIMEImage( logo.read() )
                logo.close()
                ID = "<logo>"
                msgimg.add_header( "Content-ID", ID )
                msgroot.attach( msgimg )

                # creates SMTP session
            s = smtplib.SMTP( 'smtp.gmail.com', 587 )

            # start TLS for security
            s.starttls()

            # Authentication
            s.login( fromaddr, self.password )

            # Converts the Multipart msg into a string
            text = msgroot.as_string()

            # sending the mail
            # x = 0
            for toaddr in Emails:
                # indicator.update(x+1)
                print( toaddr[ 0 ] )
                msgroot[ 'To' ] = toaddr[ 0 ]
                s.sendmail( fromaddr, toaddr, text )

                # terminating the session
            s.quit()
            messagebox.showinfo( "Success", "Sent !" )
            # self.enable()
        else:
            messagebox.showerror( "Error", "Invalid Email" )
            # self.enable()
            self.email_e.delete( 0, 'end' )
        # self.enable()

    def disable( self ):
        for child in self.mail_bomber_f.winfo_children():
            child.configure( state='disabled' )

    def enable( self ):
        for child in self.mail_bomber_f.winfo_children():
            child.configure( state='normal' )

    def add_email( self ):
        self.add_mail = AddEmail( self.mainwindow )

    def run( self ):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = MailBomber()
    app.run()
