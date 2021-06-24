from justpy import Div, WebPage, Ul, Li, A, justpy
import justpy as jp
import pandas as pd

class Tabs(Div):

    tab_label_classes = 'overflow-hidden cursor-pointer bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold'
    tab_label_classes_selected = 'overflow-hidden cursor-pointer bg-white inline-block border-l border-t border-r rounded-t py-2 px-4 text-blue-700 font-semibold'
    item_classes = 'flex-shrink mr-1'
    item_classes_selected = 'flex-shrink -mb-px mr-1'
    wrapper_style = 'display: flex; position: absolute; width: -webkit-fill-available; height: 100%;  align-items: top; justify-content: bottom; background-color: #fff;'

    def __init__(self, **kwargs):

        self.tabs = []  # list of {'id': id, 'label': label, 'content': content}
        self.value = None  # The value of the tabs component is the id of the selected tab
        self.grid = None  # The value of the tabs component is the id of the selected tab
        self.content_height = 1000
        self.last_rendered_value = None
        self.animation = False
        self.animation_next = 'slideInRight'
        self.animation_prev = 'slideOutLeft'
        self.animation_speed = 'faster'  # '' | 'slow' | 'slower' | 'fast'  | 'faster'

        super().__init__(**kwargs)

        self.tab_list = Ul(classes="flex flex-wrap border-b", a=self)
        self.content_div = Div(a=self)
        self.delete_list = []


    def __setattr__(self, key, value):
        if key == 'value':
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def add_tab(self, id, label, content):
        self.tabs.append({'id': id, 'label': label, 'content': content})
        if not self.value:
            self.value = id
        if not self.grid:
            self.grid = content.components[0]

    def get_tab_by_id(self, id):
        for tab in self.tabs:
            if tab['id'] == id:
                return tab
        return None

    # def set_content_div(self, tab):
    #     self.content_div.add(tab['content'])
    #     self.content_div.set_classes('relative overflow-hidden border')
    #     self.content_div.style = f'height: {self.content_height}px'

    def set_content_animate(self, tab):
        self.wrapper_div_classes = self.animation_speed  # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_next, temp=True,
                                   style=f'{self.wrapper_style} z-index: 0;', a=self.content_div)
            self.wrapper_div.add(tab['content'])
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_prev, temp=True,
                                   style=f'{self.wrapper_style} z-index: 0;', a=self.content_div)
            self.wrapper_div.add(self.get_tab_by_id(self.previous_value)['content'])
        else:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, temp=True, a=self.content_div,
                                   style=self.wrapper_style)
            self.wrapper_div.add(tab['content'])

        self.content_div.set_classes('relative overflow-hidden border')
        #self.content_div.style = f'width: 100, height: {self.content_height}px'
        self.content_div.style = f'height: {self.content_height}px'


    def model_update(self):
        print(self.model[0].data)
        val = self.model[0].data[self.model[1]]
        print(self.model[0].data)
        if self.get_tab_by_id(val):
            self.value = val

    def delete(self):
        for c in self.delete_list:
            c.delete_flag = True
            c.delete()
            c.needs_deletion = False

        if self.delete_flag:
            for tab in self.tabs:
                tab['content'].delete()
                tab['content'] = None
        super().delete()

    @staticmethod
    async def tab_click(self, msg):
        if self.tabs.value != self.tab_id:
            previous_tab = self.tabs.value
            self.tabs.value = self.tab_id
            if hasattr(self.tabs, 'model'):
                self.tabs.model[0].data[self.tabs.model[1]] = self.tabs.value
            # Run change if it exists
            if self.tabs.has_event_function('change'):
                msg.previous_tab = previous_tab
                msg.new_tab = self.tabs.value
                msg.id = self.tabs.id
                msg.value = self.tabs.value
                msg.grid = self.tabs.grid
                msg.class_name = self.tabs.__class__.__name__
                return await self.tabs.run_event_function('change', msg)
        else:
            return True  # No need to update page

    def convert_object_to_dict(self):
        if hasattr(self, 'model'):
            self.model_update()
        self.set_classes('flex flex-col')
        self.tab_list.delete_components()
        self.content_div.components = []
        for tab in self.tabs:
            if tab['id'] != self.value:
                tab_li = Li(a=self.tab_list, classes=self.item_classes)
                li_item = A(text=tab['label'], classes=self.tab_label_classes, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
            else:
                tab_li = Li(a=self.tab_list, classes=self.item_classes_selected)
                li_item = A(text=tab['label'], classes=self.tab_label_classes_selected, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
                if self.animation and (self.value != self.last_rendered_value):
                    self.set_content_animate(tab)
                else:
                    self.set_content_div(tab)
            li_item.tab_id = tab['id']
            li_item.tabs = self
            #div = self.components[1].components[0].components[0].components[0]
            print(self.grid.options.rowData)

            #div.options.rowData = self.grid.options.rowData
            li_item.on('click', self.tab_click)
        self.last_rendered_value = self.value
        d = super().convert_object_to_dict()

        return d

class TabsPills(Tabs):
    tab_label_classes = 'cursor-pointer inline-block border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-1 px-3'
    tab_label_classes_selected = 'cursor-pointer inline-block border border-blue-500 rounded py-1 px-3 bg-blue-500 text-white'
    item_classes = 'flex-shrink mr-3'
    item_classes_selected = 'flex-shrink -mb-px mr-3'

# https://dog.ceo/api/breed/papillon/images/random
pics_french_bulldogs = ['5458', '7806', '5667', '4860']
pics_papillons = ['5037', '2556', '7606', '8241']

def tab_change(self, msg):
    # print(msg.page.components[0])
    # print(msg.page.components[0].components[0])
    foo = msg.page.components[0].components[0].components[1].components[0].components[0]
    print(foo.components[0].id)
    #foo.components[0] = msg.grid
    #print(foo.components[0].id)
    print('in change', msg)

engie_df = pd.read_csv('demo_data.csv', encoding="ISO-8859-1")
critical_df = engie_df[engie_df['ActivityType']=='Critical']
lookahead_df = engie_df[engie_df['ActivityType']=='LA']
mygroup_df = engie_df[engie_df['Responsibility']=='Engie MECH']

tab_details = {'All':engie_df, 'My Group':mygroup_df, 'Critical':critical_df, 'Lookahead':lookahead_df}

def tab_comp_test():
    wp = jp.WebPage(data={'tab': 'id2556'})

    d_flex = Div(classes='flex', a=wp)  # Container for the two dog pictures tabs

    t = Tabs(a=d_flex, classes=' w-screen m-4', animation=True, content_height=550, model=[wp, 'tab'], change=tab_change)
    for tab in tab_details.keys():
        d = jp.Div(style=Tabs.wrapper_style)
        # din = jp.Div(style=f'text-align: center, width: -webkit-fill-available',a=d)
        # jp.Img(src=f'https://images.dog.ceo/breeds/papillon/n02086910_{pic_id}.jpg', a=din)
        grid = tab_details[tab].jp.ag_grid(a=d)
        #grid.options.pagination = True
        #grid.options.paginationAutoPageSize = True
        grid.options.defaultColDef.filter = True
        grid.options.defaultColDef.sortable = True
        grid.options.defaultColDef.resizable = True
        grid.options.defaultColDef.cellStyle['textAlign'] = 'center'
        #grid.options.defaultColDef.headerClass['font-bold'] = True

        grid.options.columnDefs[0].cellClass = ['text-white', 'bg-blue-500', 'hover:bg-blue-200']
        for col_def in grid.options.columnDefs[1:]:
            col_def.cellClassRules = {
                'font-bold': 'x < 20',
                'bg-red-300': 'x < 20',
                'bg-yellow-300': 'x >= 20 && x < 50',
                'bg-green-300': 'x >= 50'
            }
        t.add_tab(f'id{tab}', f'{tab}', d)

    input_classes = "w-1/3 m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    in1 = jp.Input(classes=input_classes, model=[wp, 'tab'], a=wp)

    return wp

justpy(tab_comp_test)