from .Die import Die

class DiceSet:
    """ Simple set of dice with custom number of sides.
    Any dice set can have any number of dice and each dice having the same number of sides.

    Attributes:
        dice (int) representing the number of dice in the box
        sides (int) representing the number of sides each die has
    """
    
    def __init__(self, dice=1, sides=6):
        
        self.dice = self.create_dice_box(dice, sides)
        self.sides = sides
       
    
    def create_dice_box(self, dice, sides):
        """ Function to create a list of Die objects.
        To be used to store the list of dice in the DiceSet object.

        Args: 
            dice (int): number of dice in the dice set
            sides (int): number of sides each die has
        
        Returns: 
            list(Die): list of Die objects in the dice set

        """
            
        dice_list = []
        
        for i in range(dice):
            die = Die(sides)
            dice_list.append(die)
        
        return dice_list
    
    
    def roll(self, verbose=False):
        """ Function to roll the dice set.

        Args: 
            verbose (optional): if True, verbose will also print the list of outcomes
        
        Returns: 
            list(int): list of outcomes for each die roll

        """
            
        rolls = [die.roll() for die in self.dice]
        
        if verbose:
            print(rolls)
            
        return rolls
    
    
    def __repr__(self):

        """ Function to output the characteristics of the dice set

        Args:
            None
        
        Returns:
            string: characteristics of the dice set

        """

        return "dice set of {} dice with {} sides".format(len(self.dice), self.sides)