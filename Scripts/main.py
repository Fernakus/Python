"""
-------------------------------------------------------
main.py
-------------------------------------------------------
Author:  Matthew Ferlaino
Email:   mferlaino73@gmail.com
Date:     Nov. 27, 2019
-------------------------------------------------------
"""

# Imports
from CCCPenetrationLib import CCCPenetrationLib

# Main Method
def main():
    # Variables
    penetrationLibrary = CCCPenetrationLib()
    
    d = penetrationLibrary.encrypt("hello")
    
    print(penetrationLibrary.decrypt(d))
# Call main
main()
    
    
    
    