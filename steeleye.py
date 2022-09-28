import pandas as pd
import xml.etree.ElementTree as Tree
import os
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile


class XmltoCsv:

    def __init__(self, path=None, url=None) -> None:

        '''
        Downloads the XML Zip, extracts the XML file and saves it at the mentioned path.
        
        Parameters:
        
        :param url: URL to download Zip File from
        :param path: Path to save the extracted XML at
        '''
        self.path = path
        self.url = url
        self.download()

    def download(self):
        # specifying the zip file name
        file_name = self.url
        
        # opening the zip file in READ mode
        with urlopen(file_name) as response:
            with ZipFile(BytesIO(response.read())) as zip:

                # extracting all the files

                zip.extractall(self.path)
    

    def parse(self) -> None:
        '''
        Uses the path property of the class to get the required path.
        Writes the data in the following tags to a csv file:
        FinInstrmGnlAttrbts.Id,
        FinInstrmGnlAttrbts.FullName,\n
        FinInstrmGnlAttrbts.ClssfctnTp,\n
        FinInstrmGnlAttrbts.CmmdtyDerivind,\n
        FinInstrmGnlAttrbts.NtnlCcy,\n
        Issr\n
        \n
        Returns: None
        '''
        filepath = None
        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                if ".xml" in f:
                    filepath = os.path.join(self.path, f)
        # Getting xml tree

        tree = Tree.parse(filepath)
        # Get the root of tree
        root = tree.getroot()
        # Parent node to look at
        parent = 'TermntdRcrd'
        
        # Desired Child 1
        pattern = 'FinInstrmGnlAttrbts'
        # Desired Child 2
        tag = 'Issr'
        # Initialising the required arrays
        children = ['Id', 'FullNm', 'ClssfctnTp', 'CmmdtyDerivInd', 'NtnlCcy']
        cols = [pattern + '.' + k for k in children]
        cols.append(tag)
        # Get the rows
        rows = list()
        for i in root.iter():
            # If parent is found
            if parent in i.tag:
                # Initialise array of required elements
                entry = [None for x in range(len(children) + 1)]
                for child in i:
                    # If required child has been found
                    if pattern in child.tag:
                        # Get the required grand-children
                        for c in child:
                            for k in range(len(children)):
                                # If grandchildren found, update entry
                                if children[k] in c.tag:
                                    entry[k] = c.text
                    # If Issr found
                    if tag in child.tag:
                        entry[5] = child.text
                # Add to list of rows
                rows.append(entry)
        # Create Dataframe
        df = pd.DataFrame(data=rows, columns=cols)
        # Save to csv
        df.to_csv(os.path.join(self.path, 'ans.csv'), index=False)


if __name__ == '__main__':
    # Get the path of the incput file
    path = '/Users/siddharthanand/Downloads/steeleye'
    # Get the download url
    url = 'http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip'
    # Execute function
    p = XmltoCsv(path=path, url=url)
    p.parse()