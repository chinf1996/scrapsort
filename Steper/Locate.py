from steper import Steper

class Locate:
    """The class can locate to a specified location"""
    _lenStep = 1
    steper = None
    def __init__(self, lenStep=1):
        """Get the length of the stepper motor (mm)"""
        self._lenStep = lenStep
        self.steper = Steper()
    
    def Go(self, distance):
        """Go to the specified distance, Let the stepper motor take (distance/lenStep) steps"""
        _steps = distance/int(self._lenStep)
        self.steper.NonlinearSpeed(int(_steps))
        
    