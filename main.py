import justpy as jp

class QInputDate(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD HH:mm', name='date', a=c2)

        self.date.parent = self
        self.date.value = self.value
        self.prepend_slot = date_slot
        self.date.on('input', self.date_change)
        self.on('input', self.input_change)

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
    # do something here

    msg.page.components[1].show=False
    msg.page.components[2].show=False
    msg.page.components[3].show=False

    msg.page.components[int(self.value[-1])].show=True
    print(f'tab name={self.value} was clicked' )

datesetting = {}

def main():
    wp = jp.QuasarPage()

    # create tabs
    tabs = jp.QTabs(a=wp, classes='text-white shadow-2 q-mb-md', style="background-color: #00305e;", 
                    align='justify', narrow_indicator=True, dense=True)

    tab1 = jp.QTab(a=tabs, name='tab_1', label='All')

    datesetting['tab_1'] = QInputDate(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='')

    tab2 = jp.QTab(a=tabs, name='tab_2', label='My group')
    datesetting['tab_2'] = QInputDate(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='')

    tab3 = jp.QTab(a=tabs, name='tab_3', label='Critical')
    datesetting['tab_3'] = QInputDate(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='')
    datesetting['tab_2'].show = False
    datesetting['tab_3'].show = False

    tabs.on('input', qtab_click)

    tabcontent = jp.Div(a=wp)
    return wp

jp.justpy(main)

