"""
-------------------------------------------------------
CCCPenetrationLib.py
-------------------------------------------------------
Author:  Matthew Ferlaino
Email:   mferlaino73@gmail.com
Date:     Nov. 27, 2019
-------------------------------------------------------
"""
# Imports
from threading import Thread
import datetime
import os
import socket
import crypt
import zipfile

# Class
class CCCPenetrationLib:
    # Global Variables
    services = "Services.txt"
    vulnerableFTPServers = "VulnerableFTPBanners.txt"
    masterPasswordFile = "MasterPasswordList.txt"
    passwordHashFile = "PasswordHashesList.txt"
    
    """
    -----------------------------------------------------
    Below Resides All Methods For This Library
    -----------------------------------------------------
    Methods Include:
        1)  unixWriteOut()
        2)  dosWriteOut()
        3)  encrypt()
        4)  decrypt()
        5)  connectToIp()
        6)  isVulnerableFTP()
        7)  JTRTestPass() 
        8)  JTRPasswordCrack()   
        9)  createHashedPasswordFile()
        10) JTRExtractZipPassword()
        11) JTRCrackZipPassword()
        12) pinger()

    ----------------------------------------------------
    """
    
    # unixWriteOut()
    def unixWriteOut(self, dictionary):
        # Home Directory
        homeDir = str(os.path.expanduser("~/Desktop"))
    
        # Open File
        log = open(homeDir + '/JTRLog.txt', 'a')
        
        # Heading
        log.write("Written On: " + str(datetime.datetime.now()) + "\n")
        
        # Loop through data and print
        for i in dictionary:
            log.write(str(i) + "\n")
    
        # Close File 
        log.write("\n")   
        log.close()    
        
        return

    # dosWriteOut
    def dosWriteOut(self, dictionary):
        # Home Directory
        homeDir = str(os.path.expanduser("~/Desktop"))
    
        # Open File
        log = open(homeDir + '\ JTRLog.txt', 'a')
        
        # Heading
        log.write("---------------------------------------------\n")
        log.write("Written By: JohnTheRipper\n")
        log.write("Written On: ")
        log.write(str(datetime.datetime.now()))
        log.write("\n")
        log.write("---------------------------------------------\n")
    
        # Loop through data and print
        for i in dictionary:
            log.write(str(i) + "\n")
    
        # Close File    
        log.close()    
        
        return
    
    # encrypt()
    def encrypt(self, toBeEncrypted):        
        return crypt.crypt(toBeEncrypted, "$$@@LLTTYYPP0000NN")

    # decrypt()    
    def decrypt(self, toBeDecrypted):        
        return crypt.crypt(toBeDecrypted, "$$@@LLTTYYPP0000NN")
    
    # connectToIP()    
    def connectToIP(self, ipAddress):
        # Instatiate        
        socket.setdefaulttimeout(2)
        sock = socket.socket()
        
        try:        
            # Connect
            sock.connect((ipAddress, 21))
        
            # Grab Response
            banner = sock.recv(1024)
        
            # Print 
            print("[Connecting --> " + str(ipAddress) + "]: " + str(banner))
            self.unixWriteOut(["[Connecting --> " + str(ipAddress) + "]: " + str(banner)])
            return banner
        
        except Exception as ex:
            print("[Connecting --> " + str(ipAddress) + "]: " + str(ex))
            self.unixWriteOut(["[Connecting --> " + str(ipAddress) + "]: " + str(ex)])
            return
      
    # isVulnerableFTP()    
    def isVulnerableFTP(self, banner):
        file = open(self.vulnerableFTPServers, 'r')
        
        for line in file.readline():
            if banner.strip('\n') in line:
                print("[" + str(banner) + "]: is vulnerable!")
                
            self.unixWriteOut(["[" + str(banner) + "]: is vulnerable!"])
            
            file.close()
            return True

        else:
            print("[" + str(banner) + "]: is not vulnerable.")            
            self.unixWriteOut(["[" + str(banner) + "]: is not vulnerable."])
            
            file.close()
            return False
    
    # JTRTestPass()    
    def JTRTestPass(self, cryptPass):
        # Parse salt
        salt = cryptPass[0:2]
        
        # Open dictionary
        passwordHashes = open(self.passwordHashFile, "r")
        
        # Preform dictionary attack
        for word in passwordHashes.readlines():
            word = word.strip('\n')
            
            # Performing crypt
            cryptWord = crypt.crypt(word,salt) 
            
            # Found password  
            if (cryptWord == cryptPass):
                print ("[***] Found Password: " + word + "\n")
                self.unixWriteOut(["[***] Found Password: " + word + "\n"])
                return True
            
        
        print ("[***] Password Not Found.\n")
        self.unixWriteOut(["[***] Password Not Found.\n"])
        return
    
    # JTRPasswordCrack()    
    def JTRPasswordCrack(self, cryptPass):
        # Open Password File
        passwordFile = open(self.masterPasswordFile, "r")
        
        # Loop through passwords
        for line in passwordFile.readlines():
            
            # Call JTRTestPass()
            print("[***] Cracking Password: " + line)
            self.JTRTestPass(cryptPass)
            self.unixWriteOut(["[***] Cracking Password: " + line])
        return
    
    # createHashedPasswordFile()
    def createHashedPasswordFile(self, dictionaryFile):
        # Passwords
        compromisedPasswords = open(dictionaryFile, "r")
        hashedPasswords = open("hashedPasswordsFile.txt", "w")
        
        # Hashing
        for password in compromisedPasswords:
            print(password)
            hashedPasswords.write(self.encrypt(password))
        
        # Close
        hashedPasswords.close()
        compromisedPasswords.close()
        self.unixWriteOut(["[***] Created hashed password file.\n"])
        
        return
    
    # JTRExtractZipPassword()    
    def JTRExtractZipPassword(self, zipFile, password):
        try:
            # Extract password from zip
            zipFile.extractall(pwd=password)
            
            print("[***] Extracted password hash for: [" + zipFile + "]: " + password)
            self.unixWriteOut(["[***] Extracted password hash for: [" + zipFile + "]: " + password])
            
            return password
        
        except Exception as ex:
            print(["[***] " + ex])
            self.unixWriteOut(["[***] " + ex])
            return
        
        return
        
    # JTRCrackZipPassword()    
    def JTRCrackZipPassword(self, zipFileHanlde):
        zFile = zipfile.ZipFile(zipFileHanlde)
        passwordFile = open(self.masterPasswordFile)
        
        # Multi-threaded
        for line in passwordFile.readlines():
            JTRThread = Thread(target=self.JTRExtractZipPassword, args=(zFile, line.strip('\n')))
            JTRThread.start()
            JTRThread.join()
            
        passwordFile.close() 
        return 
    
    # pinger()    
    def pinger(self, ipToPing):
        self.connectToIP(ipToPing)
        return 
        
        
    