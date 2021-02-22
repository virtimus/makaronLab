import q3

print(dir(q3))

import q3.Signal

import q3.Timer

#as q3App


app = q3.App()

# Then a frame.
frm = q3.MainWindow(title="Hello World")

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()