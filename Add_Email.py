import os
import pygubu
import sqlite3
from tkinter import messagebox
from tkinter import ttk
import re

PROJECT_PATH = os.path.dirname( __file__ )
PROJECT_UI = os.path.join( PROJECT_PATH, "UI/add_email.ui" )


class AddEmail:

	def __init__( self, mainwindow ):

		self.builder = builder = pygubu.Builder()
		builder.add_resource_path( PROJECT_PATH )
		builder.add_from_file( PROJECT_UI )
		self.mainwindow = mainwindow
		self.add_email_f = builder.get_object( "add_email_f" )
		builder.connect_callbacks( self )
		self.get_widget_objects()
		self.config()
		self.showEmails()

	def get_widget_objects( self ):

		self.email_e = self.builder.get_object( "email_e" )
		self.treeview = self.builder.get_object( "treeview" )
		self.scroll = self.builder.get_object( "scrollbar" )

		self.email_e.focus_set()

	def config( self ):
		self.email_list_DB = sqlite3.connect( "Email_List.db" )
		self.email_e.bind( "<Return>", self.add_email )

		self.treeview.configure( xscrollcommand=self.scroll.set )
		self.treeview[ "columns" ] = ( "1", "2" )

		# Defining heading
		self.treeview[ 'show' ] = 'headings'

		# Assigning the width and anchor to  the
		# respective columns
		self.treeview.column( "1", width=50 )
		self.treeview.column( "2", width=500 )

		# Assigning the heading names to the
		# respective columns
		self.treeview.heading( "1", text="ID" )
		self.treeview.heading( "2", text="Email" )

	def get_widget_value( self ):
		self.email = self.email_e.get()
		print( self.email )

	def checkORcreate( self ):
		self.email_list_DB.execute( """create table if not exists emails (email text)""" )

	def only_email( self ):
		regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		if ( re.search( regex, self.email ) ):
			return True
		else:
			return False

		pass

	def showEmails( self ):
		for i in self.treeview.get_children():
			self.treeview.delete( i )
		cursor = self.email_list_DB.execute( "SELECT rowid,email  from emails" )
		for row in cursor:
			self.treeview.insert(
			    "", row[ 0 ], row[ 0 ], text=row[ 1 ], values=( row[ 0 ], row[ 1 ] )
			    )

	def add_email( self, event=None ):
		self.checkORcreate()
		self.get_widget_value()
		flag = self.only_email()
		if flag:
			self.email_list_DB.execute( """insert into emails values (?)""", ( self.email, ) )
			self.email_list_DB.commit()

		else:
			messagebox.showerror( "Error", "Invalid Email" )
		self.email_e.delete( 0, "end" )
		self.email_e.focus_set()
		self.showEmails()
		pass

	def delete_email( self ):
		n = self.treeview.selection()
		if n != ():
			n = int( n[ 0 ] )
			print( n )
			self.email_list_DB.execute( """delete from emails where rowid= ?""", ( n, ) )
			self.email_list_DB.commit()
			self.email_list_DB.execute( "VACUUM" )

			self.showEmails()

	def close( self ):
		self.email_list_DB.close()
		self.add_email_f.destroy()

	def run( self ):
		self.mainwindow.mainloop()


if __name__ == '__main__':
	root = tk.Tk()
	app = AddEmail( root )
	app.run()
