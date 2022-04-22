import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import csv
from datetime import datetime
CREDENTIALS_FILE = 'akes-project-4037cc052234.json'
spreadsheetId = '1TkBDXHKLVHVmuilU2Iuak34kmjuQPKX40LhbReXc4DE'
sheetId = 1968705244

class Script:
    def __init__(self, file, CREDENTIALS_FILE, spreadsheetId, sheetId):
        self.file = file
        self.spreadsheetId = spreadsheetId
        self.sheetId = sheetId
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
        self.len = len(self.withFile())  # Len for a butchUpdate

        newName = str(datetime.now())
        newName = newName[:-10]
        newName = newName.replace("-", "/")
        newName = newName.replace(" ", " - ")
        
        self.newName = newName

        
    def withFile(self):
        in_file = [] 
        with open(self.file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';') 
            for row in csv_reader:
                in_file.append(row)
                in_file[-1].pop(-1)
        return in_file
    
    
    def cells_with_func(self):
        func_cells = []
        def func(func):
            func_cells_ = []
            n=5
            for i in range(self.len):
                func_cells_.append(func.format(n = n))
                n+=1
            return func_cells_
        func_cells.append(func('=СУММ(G{n}:I{n})'))
        func_cells.append(func('=СУММ(S{n}:U{n})'))
        func_cells.append(func('=AL{n}-AK{n}'))
        func_cells.append(func('=(AL{n}-AK{n})/AK{n}'))
        return func_cells

    
    def copy(self):
        request = self.service.spreadsheets().sheets().copyTo(spreadsheetId = self.spreadsheetId, sheetId = self.sheetId, body =
        {
            'destination_spreadsheet_id': self.spreadsheetId
        }
                                                 )
        response = request.execute()
        return response['sheetId']

    
    def new_name(self):
        response = self.service.spreadsheets().batchUpdate(spreadsheetId = self.spreadsheetId, body = {
            "requests" : [{
                "updateSheetProperties": {
                    "properties": {
                        "sheetId" : self.copy(),
                        "title" : self.newName
                        },
                    "fields": "title"
                    }}]
            }).execute()


    def main___(self):
        self.new_name()
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{self.newName}!A5:AJ{self.len+4}",
             "majorDimension": "ROWS",
             "values": self.withFile()},      
                        
            {"range": f"{self.newName}!AK5:AN{self.len+4}",
             "majorDimension": "COLUMNS",
             "values": self.cells_with_func()}   
            ]
        }).execute()
        
        
    
        
    

        
