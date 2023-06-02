from spyre import server

import pandas as pd
import os
import re

class StockExample(server.App):
    title = "NOAA data vizualisation"

    inputs = [
                {
                    "type":'dropdown',
                    "label": 'Parameter',
                    "options" : [ {"label": "VCI", "value":"VCI"},
                                  {"label": "TCI", "value":"TCI"},
                                  {"label": "VHI", "value":"VHI"}],
                    "key": 'sel_column',
                    "action_id": "update_data"
                },
                {
                    "type": 'text',
                    "label": 'Year',
                    "value": '2023',
                    "key": 'sel_year',
                    "action_id": "update_data"
                },
                {
                    "type": 'dropdown',
                    "label": 'Province',
                    "options": [
                        {"label": "Cherkasy", "value": "Cherkasy"},
                        {"label": "Chernihiv", "value": "Chernihiv"},
                        {"label": "Chernivtsi", "value": "Chernivtsi"},
                        {"label": "Crimea", "value": "Crimea"},
                        {"label": "Dnipropetrovs'k", "value": "Dnipropetrovs'k"},
                        {"label": "Donets'k", "value": "Donets'k"},
                        {"label": "Ivano-Frankivs'k", "value": "Ivano-Frankivs'k"},
                        {"label": "Kharkiv", "value": "Kharkiv"},
                        {"label": "Kherson", "value": "Kherson"},
                        {"label": "Khmel'nyts'kyy", "value": "Khmel'nyts'kyy"},
                        {"label": "Kiev", "value": "Kiev"},
                        {"label": "Kiev City", "value": "Kiev City"},
                        {"label": "Kirovohrad", "value": "Kirovohrad"},
                        {"label": "Luhans'k", "value": "Luhans'k"},
                        {"label": "L'viv", "value": "L'viv"},
                        {"label": "Mykolayiv", "value": "Mykolayiv"},
                        {"label": "Odessa", "value": "Odessa"},
                        {"label": "Poltava", "value": "Poltava"},
                        {"label": "Rivne", "value": "Rivne"},
                        {"label": "Sevastopol'", "value": "Sevastopol'"},
                        {"label": "Sumy", "value": "Sumy"},
                        {"label": "Ternopil'", "value": "Ternopil'"},
                        {"label": "Zakarpathia", "value": "Zakarpathia"},
                        {"label": "Vinnytsya", "value": "Vinnytsya"},
                        {"label": "Volyn", "value": "Volyn"},
                        {"label": "Zaporizhzhya", "value": "Zaporizhzhya"},
                        {"label": "Zhytomyr", "value": "Zhytomyr"}
                    ],
                    "key": 'sel_prov',
                    "action_id": "update_data"
                }
            ]
                    

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]

    def getData(self, params):
        sel_column = params.get('sel_column', 'VHI')
        sel_prov = params.get('sel_prov', 'Odessa')
        sel_year = int(params.get('sel_year', 2022))
        dir = "frames"
        dflist = []
        for filename in os.listdir(dir):
            province = re.search(r"obl_(\d+)_\d+", filename).group(1)
            filename = f"{dir}/{filename}"
            headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'] 
            df = pd.read_csv(filename, header = 1, names = headers)
            df = df.drop(columns=['empty'])
            df['province'] = province
            dflist.append(df)

        df=dflist[0]    
        for dfi in dflist[1:]:
            df = pd.concat([df, dfi], ignore_index=True)
        text=""" 1: Cherkasy
        2: Chernihiv
        3: Chernivtsi
        4: Crimea
        5: Dnipropetrovs'k
        6: Donets'k
        7: Ivano-Frankivs'k
        8: Kharkiv
        9: Kherson
        10: Khmel'nyts'kyy
        11: Kiev
        12: Kiev City
        13: Kirovohrad
        14: Luhans'k
        15: L'viv
        16: Mykolayiv
        17: Odessa
        18: Poltava
        19: Rivne
        20: Sevastopol'
        21: Sumy
        22: Ternopil'
        23: Zakarpathia
        24: Vinnytsya
        25: Volyn
        26: Zaporizhzhya
        27: Zhytomyr"""
        province_ids = {}
        for line in text.split('\n'):
            if line.strip():
                value = line.split(':')[1].strip()
                key = line.split(':')[0].strip()
                province_ids[key] = value
        df['province']=df['province'].map(province_ids)
        selected=(df[(df['province']==sel_prov)&(df['Year']==sel_year)&(df[sel_column]!=-1)][["Week",sel_column]])
        return df[(df['province']==sel_prov)&(df['Year']==sel_year)]

    def getPlot(self, params):
        sel_column = params.get('sel_column', 'VHI')
        sel_prov = params.get('sel_prov', 'Odessa')
        sel_year = params.get('sel_year', 2022)
        selected=self.getData(params)
        selected=selected[["Week",sel_column]]
        # selected=(df[(df['province']==sel_prov)&(df['Year']==sel_year)&(df['VHI']!=-1)][["Week",sel_column]])
        # min_vhi=selected.loc[selected[sel_column].idxmin()].to_dict()
        # max_vhi=selected.loc[selected[sel_column].idxmax()].to_dict()
        # print(f'Selected: Province = {sel_prov}, Year = {sel_year}\n\n',selected)
        # print(f'\nMIN {sel_column}: {min_vhi}\nMAX {sel_column}: {max_vhi} ')
        fig=selected.plot(x='Week', y=sel_column)
        fig.set_title(f"{sel_column} {sel_prov} {sel_year}")
        fig.set_ylabel(sel_column)
        fig.set_xlabel("Week")
        outfig = fig.get_figure()
        return outfig

app = StockExample()
app.launch(port=9093)