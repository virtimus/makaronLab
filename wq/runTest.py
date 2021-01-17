import wq

#as wqApp


app = wq.App()

# Then a frame.
frm = wq.MainWindow(title="Hello World")

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()