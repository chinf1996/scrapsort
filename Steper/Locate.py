from steper import Steper

class Locate:
    """The class can locate to a specified location"""
    _steps = 0
    _lenStep = 1
    def __init__(self, lenStep=1):
        """Get the length of the stepper motor (mm)"""
        _lenStep = lenStep
    
    
    def Go(self, distance):
        """Go to the specified distance, Let the stepper motor take (distance/lenStep) steps"""
        _steps = distance/int(_lenStep)
        Steper.NonlinearSpeed(int(_steps))
        
    