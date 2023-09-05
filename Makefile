CC=python
DESIGNER=designer-qt5
CGUI=pyuic5

MAINFILE=main.py

# GUI files
GUIAPP=src/GUI/app.ui
GUIAPPCOMPILED=src/GUI/app_ui.py

all: run

# just run the code for development and testing
run:
	$(MAKE) build-gui
	$(CC) $(MAINFILE)

# Edit GUI with program
# TODO: think how to make this for WINDOWS and MACOS
edit-gui:
	$(DESIGNER) $(GUIAPP) & disown

# build the GUI from the .ui files
build-gui:
	$(CGUI) $(GUIAPP) > $(GUIAPPCOMPILED)
