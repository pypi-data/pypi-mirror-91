#! python3
# Combines all the pafs in the current working directory into a single pdf

import PyPDF2, os, sys, logging

class Merge (): 
    """
    Merge all pdfs in the current folder, or specific list of files, 
    by name, into a single pdf file
    """

    def __init__ (self, file_output = "", replace = False, debug = False):
        """
        Constructor of class. Generate empty list of files an get dir path and file ouput
        """

        # Debug configuration
        logging.basicConfig( level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s' )
        if not debug: 
            logging.disable()

        self.pdfFiles = []
        self.fileOutput = file_output
        self.replace = replace

        self.__verify_outputh_file()

    def merge_file_list (self, file_list): 
        """
        Merge a specific list of pdf files inside the output file
        """

        # verify attribs
        if type (file_list) != list: 
            raise AttributeError (file_list)

        self.pdfFiles = file_list

        # Short files
        self.pdfFiles.sort(key = str.lower)

        self.__make_file()
    
    def merge_folder (self, folder):
        """
        Merge all files from a specific folder and save inside the output file
        """

        # Verify is folder exist
        if not os.path.isdir (folder): 
            raise FileNotFoundError(folder)
        
        # Get files
        for filename in os.listdir(folder):
            if filename.endswith('.pdf'): 
                self.pdfFiles.append(os.path.join(folder, filename))
        
        # Order files
        self.pdfFiles.sort(key = str.lower)

        self.__make_file()

    def __verify_outputh_file (self): 
        """
        Verify the name of the output file and if the file will be replace or not
        """

        # verify path and make file name
        if os.path.isdir (self.fileOutput): 
            self.fileOutput = os.path.join(self.fileOutput, 'mergeFiles.pdf')
        else: 
            if not self.fileOutput.endswith('.pdf'): 
                self.fileOutput += '.pdf'

        # Verify replca outputh file
        if os.path.isfile(self.fileOutput):
            if self.replace: 
                logging.debug ("Replacing file")
            else: 
                self.fileOutput = 'File "{}" already exist'.format (self.fileOutput)
                raise ValueError(self.fileOutput)

    def __make_file (self):
        """
        Make pdf output file with each page of the file list 
        """

        pdfWriter = PyPDF2.PdfFileWriter()

        # loop through all the pdf files
        if self.pdfFiles: 
            for currentFile in self.pdfFiles: 
                pdfFileObj = open (currentFile, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                # loop through all the pages (except the first) and add them
                logging.debug ("Merging {}... ".format (currentFile))
                if pdfReader.numPages: 
                    for pageNum in range (0, pdfReader.numPages): 
                        pageObj = pdfReader.getPage(pageNum)
                        pdfWriter.addPage (pageObj)            
            
            # Save the resulting pdf to a file
            pdfOutput = open (self.fileOutput, 'wb')
            pdfWriter.write(pdfOutput)
            pdfOutput.close()

            logging.debug ('Done. Pages are now in {} file'.format (os.path.basename(self.fileOutput)))
        else: 
            logging.debug ("Dosent exist pdf files in this folder.")




