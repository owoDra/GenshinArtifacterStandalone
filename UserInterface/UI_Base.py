class BaseUI:
    def __init__(self):
        self.PendingDestroy = False;
        self.Window = self.Construct()
        
        while not self.PendingDestroy:
            Event, Values = self.Window.read()
            self.Update(Event, Values)
    
    def Construct(self):
        return None
    
    def Update(self, Event, Values):
        pass
        
    def Close(self):
        self.PendingDestroy = True
        self.Window.close()
        