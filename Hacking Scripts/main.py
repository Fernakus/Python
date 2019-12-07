"""
-------------------------------------------------------
main.py
Running exploit functions
-------------------------------------------------------
Author:  Matthew Ferlaino
__updated__ = "2019-02-08"
-------------------------------------------------------
"""
# Imports
from exploitFunctions import exploitFunctions
import random

# Main Method
def main():
    # Variables
    exploitObj = exploitFunctions()
    list = []
    
    # Populate List
    for i in range(20):
        list.append(random.randrange(-20,20))
    
    # Sort
    list.sort()
    
    # Call writeOut()
    exploitObj.unixWriteOut(list)
    
    
# Call main
main()