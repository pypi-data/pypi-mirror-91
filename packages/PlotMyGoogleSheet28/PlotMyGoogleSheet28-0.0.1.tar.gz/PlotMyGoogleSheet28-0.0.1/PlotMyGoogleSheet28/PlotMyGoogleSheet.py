import gspread
import matplotlib.pyplot as plt
from gspread_dataframe import get_as_dataframe
import seaborn as sns

class PlotMyGoogleSheet():

    # Constructor
    def __init__(self, link):

        # Authenticating using serive account
        # Open the file using the sheet URL.
        # Select only sheet1
        self.sh = gspread.service_account(filename='credentials.json').open_by_url(link).sheet1 

    # Line plot b/w col1 and col2 using matplotlib
    def plot(self, x, y):
        
        # Sheet to Dataframe
        df = get_as_dataframe(self.sh) # It will return the worksheets contents as a Dataframe
        df = df.dropna(how = "all", axis = 1) # Do not include unnamed columns
        
        sns.set_style('darkgrid')
        plt.figure(figsize = (15, 15))
        sns.lineplot(x = df[x], y = df[y])
        plt.xlabel(x)
        plt.ylabel(y)        
        plt.savefig(x+' VS '+y+'.png') # Save the figure
        plt.show()      # Render the figure
        print('Figure saved...')

    # Return column names of our sheet
    def get_cols(self):

        # Sheet to Dataframe
        df = get_as_dataframe(self.sh) # It will return the worksheets contents as a Dataframe
        df = df.dropna(how = "all", axis = 1) # Do not include unnamed columns

        return df.columns.to_list()
