from justpy import Div
import justpy as jp
import pandas as pd

class AgGridTbl(jp.AgGrid):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.load_pandas_frame(self.df)
        # print(self.options.rowData)

        self.options.defaultColDef.filter = True
        self.options.defaultColDef.sortable = True
        self.options.defaultColDef.resizable = True
        self.options.defaultColDef.cellStyle['textAlign'] = 'center'
        self.options.defaultColDef.headerClass = 'font-bold'

        # self.options.columnDefs[0].cellClass = ['text-black', 'bg-blue-500', 'hover:bg-blue-200']
        # for col_def in self.options.columnDefs[1:]:
        #     col_def.cellClassRules = {
        #         'font-bold': 'x < 20',
        #         'bg-red-300': 'x < 20',
        #         'bg-yellow-300': 'x >= 20 && x < 50',
        #         'bg-green-300': 'x >= 50'
        #     }

        # self.date.on('input', self.date_change)
        # self.on('input', self.input_change)

    @staticmethod
    def date_change(self, msg):
        parent = self.parent
        self.parent.value = self.value
        self.parent.date.value = self.value

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value
        #save the value
        #datesetting['tab_'+msg.id] = self.value
        print(f'input for tab_{msg.id} was changed to {self.value}')

def qtab_click(self, msg):
    """function runs when user clicks a QTab"""
    if (self.value[-1] == '1'):
        msg.page.components[1].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: block;"
        msg.page.components[2].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: none;"
    else:
        msg.page.components[1].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: none;"
        msg.page.components[2].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: block;"
    print(f'tab name={self.value} was clicked' )

engie_df = pd.read_csv('demo_data.csv', encoding="ISO-8859-1")
# critical_df = engie_df[engie_df['ActivityType']=='Critical']
# lookahead_df = engie_df[engie_df['ActivityType']=='LA']
mygroup_df = engie_df[engie_df['Responsibility']=='Engie MECH']
#tab_details = {'All':engie_df, 'My Group':mygroup_df, 'Critical':critical_df, 'Lookahead':lookahead_df}

def percent_changed(self, msg):
    print(msg)


def main():
    wp = jp.QuasarPage()

    # create tabs
    tabs = jp.QTabs(a=wp, classes='text-white shadow-2 q-mb-md', style="background-color: #00305e;", 
                    align='justify', narrow_indicator=True, dense=True)

    tab1 = jp.QTab(a=tabs, name='tab_1', label='All')
    # Need to select this tab - the next line is temporary
    tab1.set_focus = True
    all = AgGridTbl(a=wp, df=engie_df, style="height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;")

    tab2 = jp.QTab(a=tabs, name='tab_2', label='My group')
    mygroup = AgGridTbl(a=wp, df=mygroup_df, style="height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: block;")    
    # need to hide the table after rendering but uncommenting the next line messes up the col widths
    #mygroup.style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: none;"

    mygroup.options.columnDefs[6].editable = True

    mygroup.on('cellValueChanged', percent_changed)

    tabs.on('input', qtab_click)

    tabcontent = jp.Div(a=wp)

    return wp

jp.justpy(main)

