from UserInterface.UI_SetUID import UI_SetUID
from UserInterface.UI_Generator import UI_Generator

def OpenSetUID(Arg = None):
    UI_SetUID(OpenGenerator)

def OpenGenerator(Data):
    UI_Generator(OpenSetUID, Data)

OpenSetUID()