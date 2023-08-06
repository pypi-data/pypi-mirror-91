This package allows all user to plot a graph between any two columns of your google sheet.<br/><br/>

# Installation using pip:<br/>
```
    pip install PlotMyGoogleSheet28
```

# Methods Available:<br/>
    + .get_cols() : This method will return a list of all column lables present in the selected google sheet.

    + .plot(x, y) : This method will generate a graph between column1(x_axis) and column2(y_axis) and will save it as an image file on the local disk.

# Code Example<br/>
```
    from PlotMyGoogleSheet28 import *

    object = MyFirstPlot(url)

    # Method 1
    columns = object.get_cols()

    # Method 2
    object.plot(x_axis_column_name, y_axis_column_name)
```


