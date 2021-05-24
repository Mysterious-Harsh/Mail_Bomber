import os
import pygubu

PROJECT_PATH = os.path.dirname( __file__ )
PROJECT_UI = os.path.join( PROJECT_PATH, "UI/indicator.ui" )


class Indicator:

    def __init__( self, mainwindow ):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path( PROJECT_PATH )
        builder.add_from_file( PROJECT_UI )
        self.mainwindow = mainwindow
        self.indicator_f = builder.get_object( "indicator_f" )
        builder.connect_callbacks( self )
        self.get_widget_objects()

    def get_widget_objects( self ):
        self.start_ltv = self.builder.get_variable( "start_ltv" )
        self.end_ltv = self.builder.get_variable( "end_ltv" )
        self.start_l = self.builder.get_object( "start_l" )
        self.end_l = self.builder.get_object( "end_l" )
        self.to_l = self.builder.get_object( "to_l" )

    def config( self, start, end ):
        self.start_ltv.set( start )
        self.end_ltv.set( end )
        self.start_l.config( width=8 )
        self.end_l.config( width=8 )
        self.to_l.config( width=2 )

    def update( self, start ):
        self.start_ltv.set( start )

    def run( self ):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = Indicator( root )
    app.run()
