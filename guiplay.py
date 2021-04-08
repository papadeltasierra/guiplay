import os
from tkinter import Tk, BooleanVar, Menu, Canvas, DISABLED
from tkinter.ttk import Style, Notebook, Frame, Label
from functools import partial
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Preferences():
   """Class to read, store and write preferences."""
   PROGRAM_NAME = "singles"
   PROGRAM_VERSION = "0.0.1"
   NAME = "name"
   VERSION = "version"
   LAYOUT = "layout"
   WIDTH = "width"
   HEIGHT = "height"
   XOFFSET = "xoffset"
   YOFFSET = "yoffset"
   THEME = "theme"
   RECENT = "recent"
   DEFAULT_WIDTH = 1000
   DEFAULT_HEIGHT = 500
   DEFAULT_XOFFSET = 100
   DEFAULT_YOFFSET = 100
   XML = "xml"

   def __init__(self):
      """Read preferences from config file if available else create defaults."""
      try:
         print("Reading...")
         self._read_preferences()
      except FileNotFoundError:
         print("Defaults...")
         self._defaults()

   def _read_preferences(self):
      """Read current preferences."""
      with open(self._filename(), "r") as source:
         self.preferences = load(source, Loader=Loader)

   def write_preferences(self):
      try:
         print(self.preferences)
         with open(self._filename(), "w") as target:
            target.write(dump(self.preferences, Dumper=Dumper))

      except Exception:
         pass

   def _filename(self):
      """Determine the name of the configuration file."""
      filename = "{name}.{ext}".format(name=Preferences.PROGRAM_NAME, ext=Preferences.XML)
      if os.name == "posix":
         # Unix style naming.
         filename = os.path.join("etc", Preferences.PROGRAM_NAME, filename)
      elif os.name == "nt":
         # Windows style naming
         filename = os.path.join(os.path.expanduser("~"), filename)
      else:
         # Other - use current directory.
         filename = "{name}.{ext}".format(name=os.splitext(program)[0], ext=Preferences.XML)

      print(filename)
      return filename

   def _defaults(self):
      """Set default configurations."""
      self.preferences = {}
      self.preferences[Preferences.NAME] = Preferences.PROGRAM_NAME
      self.preferences[Preferences.VERSION] = Preferences.PROGRAM_VERSION
      self.preferences[Preferences.LAYOUT] = {}
      self.preferences[Preferences.LAYOUT][Preferences.WIDTH] = Preferences.DEFAULT_WIDTH
      self.preferences[Preferences.LAYOUT][Preferences.HEIGHT] = Preferences.DEFAULT_WIDTH
      self.preferences[Preferences.LAYOUT][Preferences.XOFFSET] = Preferences.DEFAULT_XOFFSET
      self.preferences[Preferences.LAYOUT][Preferences.YOFFSET] = Preferences.DEFAULT_YOFFSET
      self.preferences[Preferences.THEME] = None
      self.preferences[Preferences.RECENT] = []


preferences = Preferences()

root = Tk()
root.geometry("1000x500+100+100")

style = Style()
themes = style.theme_names()

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def ontheme(theme):
   global style

   for show_theme in themes:
      show_themes[show_theme].set(False)
   show_themes[theme].set(True)
   print(theme)
   style.theme_use(theme)

def themestate(theme):
   print("Checking state for: %s" % theme)
   return show_themes[theme]



show_all = BooleanVar()
show_all.set(True)


show_themes = {theme: BooleanVar() for theme in themes}
for show_theme in show_themes:
   show_themes[show_theme].set(False)

if len(themes) > 0:
   show_themes[themes[0]].set(True)
   style.theme_use(themes[0])

root.title("singles")
# root.iconbitmap('path/to/icon/bitmap')




menubar = Menu(root)

filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.entryconfig("Save", state=DISABLED)
filemenu.entryconfig("Save as...", state=DISABLED)
filemenu.entryconfig("Close", state=DISABLED)
filemenu.add_separator()

submenu = Menu(menubar, tearoff=False)
themes_menu = Menu(submenu, tearoff=False)
for theme in themes:
   themes_menu.add_checkbutton(label=theme.capitalize(), onvalue=1, offvalue=0, variable=show_themes[theme], command=partial(ontheme, theme))
submenu.add_cascade(label='Themes', menu=themes_menu)
submenu.add_command(label="Settings")

filemenu.add_cascade(label='Preferences', menu=submenu, underline=0)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)

viewmenu = Menu(menubar, tearoff=False)
viewmenu.add_command(label="Experimental", command=donothing)
viewmenu.add_command(label="Simulations", command=donothing)
viewmenu.add_command(label="Difference", command=donothing)
viewmenu.entryconfig("Experimental", state=DISABLED)
viewmenu.entryconfig("Simulations", state=DISABLED)
viewmenu.entryconfig("Difference", state=DISABLED)
# viewmenu.entryconfig(themes, state=DISABLED)

menubar.add_cascade(label="View", menu=viewmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

# Add a couple of tabbed pages.
tabControl = Notebook(root)
tab1 = Frame(tabControl)
# tab2 = Frame(tabControl)

Label(tab1, text="Welcome to GeeksForGeeks").grid(column=0, row=0, padx=30, pady=30)
# Label(tab2, text="Lets dive into the world of computers").grid(column=0, row=0, padx=30, pady=30)
canvas = Canvas(tabControl)
canvas.create_line(15, 25, 200, 25)
canvas.create_line(300, 35, 300, 200, dash=(4, 2))
canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

tabControl.add(tab1, text='Tab 1')
#tabControl.add(tab2, text='Tab 2')
tabControl.add(canvas, text='Tab 2')
tabControl.pack(expand=1, fill="both")

root.config(menu=menubar)
root.mainloop()

preferences.write_preferences()