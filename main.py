from timerGUI import timerGUI

mainGUI = timerGUI()

mainGUI.root.after(1, mainGUI.update)
mainGUI.root.mainloop()