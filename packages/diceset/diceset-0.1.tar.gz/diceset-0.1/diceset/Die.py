import random

class Die:
    """ Die object with a specified number of sides.
    
    Attributes:
        sides (int) representing the number of sides the die has
    """

    def __init__(self, sides=2):
        
        self.sides = sides

    def roll(self):
        """Function to roll the die.

        Args: 
            None

        Returns: 
            int: the outcome of the die roll

        """
            
        random.seed()
        return random.randrange(1, self.sides + 1)
    
    
    def __repr__(self):
        """Function to output the characteristics of the die.

        Args:
            None
        
        Returns:
            string: characteristics of the die

        """

        return "{} sided die".format(self.sides)