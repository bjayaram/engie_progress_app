from justpy import Div
import justpy as jp
import pandas as pd

from sql import activities, connection, user_df, engie_df

login_form_html = """
<div class="w-full max-w-xs">
  <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
        Username
      </label>
      <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"  type="text" placeholder="Username" name="user_name">
    </div>
    <div class="mb-6">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
        Password
      </label>
      <input class="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" name="password" type="password" placeholder="******************">
    </div>
    <div class="flex items-center justify-between">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" name="sign_in_btn">
        Sign In
      </button>
    </div>
  </form>

  <p class="text-center text-gray-500 text-xs">
    Terms and Conditions apply
  </p>
</div>
"""

alert_html = """
<div role="alert" class="m-1 p-1 w-1/3">
  <div class="bg-red-500 text-white font-bold rounded-t px-4 py-2">
    Password is incorrect
  </div>
  <div class="border border-t-0 border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700">
    <p>Please enter password again.</p>
  </div>
</div>
"""

alert_dialog_html = """
<div class="q-pa-md q-gutter-sm">
    <q-dialog name="alert_dialog" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Alert</div>
        </q-card-section>

        <q-card-section>
          Percent value was edited.
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
</div>
"""

users = {}

async def login_test(request):
    wp = jp.WebPage()
    session_id = request.session_id
    if session_id in users:
        if users[session_id]['logged_in']:
            jp.Div(a=wp, text=f'Your session id is: {session_id}', classes='m-1 p-1 text-xl ')
            jp.Div(a=wp, text=f'You are already logged in...', classes='m-1 p-1 text-2l')
            log_out_btn = jp.Button(text='Logout', classes=jp.Styles.button_bordered + ' m-1 p-1', a=wp)
            log_out_btn.s_id = session_id

            def log_out(self, msg):
                users[self.s_id]['logged_in'] = False
                msg.page.redirect = '/login_test'

            log_out_btn.on('click', log_out)

            logged_in = True
        else:
            logged_in = False
    else:
        users[session_id] = {}
        users[session_id]['logged_in'] = False
        logged_in = False
    if not logged_in:
        return await login_page(request)  # Return different page if not logged in
    return wp

accounts = {"bjayaram":"BJ","etraas":"EngieHVAC"}

@jp.SetRoute('/login')
async def login_page(request):
    try:
        if users[request.session_id]['logged_in']:
            return await login_test(request)
    except:
        pass
    wp = jp.WebPage()
    wp.display_url = 'login_page'  # Sets the url to display in browser without reloading page
    jp.Div(text='Please login', a=wp, classes='m-2 p-2 w-1/4 text-xl font-semibold')
    login_form = jp.parse_html(login_form_html, a=wp, classes='m-2 p-2 w-1/2')
    alert = jp.parse_html(alert_html, show=False, a=wp)
    
    pdf_div = jp.Div(text='', a=wp, classes='m-2 p-2 w-1/4', 
            style='border: 2px solid lightblue; height: 100px; padding: 10px 0; display: flex; justify-content: center;')
    pdf1_link = jp.A(text='PDF File1', href='https://www.learningcontainer.com/wp-content/uploads/2019/09/sample-pdf-file.pdf', download='update_data.csv', a=pdf_div,
             classes='inline-block m-2 p-2 text-blue text-xl', style="color:blue; padding: 0.5rem;")
    pdf1_link.on('click', change_link_text)

    pdf2_link = jp.A(text='PDF File2', href='https://www.learningcontainer.com/wp-content/uploads/2019/09/sample-pdf-file.pdf', download='update_data.csv', a=pdf_div,
             classes='inline-block m-2 p-2 text-blue text-xl', style="color:blue; padding: 0.5rem;")
    pdf2_link.on('click', change_link_text)

    session_div = jp.Div(text='', classes='m-1 p-1 text-xl', a=wp)
    sign_in_btn = login_form.name_dict['sign_in_btn']
    sign_in_btn.user_name = login_form.name_dict['user_name']
    sign_in_btn.session_id = request.session_id
    sign_in_btn.alert = alert

    async def sign_in_click(self, msg):
        
        if (login_form.name_dict['user_name'].value not in user_df['login'].values):
            session_div.text = request.session_id + ' account not valid'
            self.alert.show = True

        #if login_form.name_dict['password'].value == eval('accounts["'+login_form.name_dict['user_name'].value+'"]'):
        if login_form.name_dict['password'].value == user_df[user_df['login']==login_form.name_dict['user_name'].value].pswd.values[0]:
            session_div.text = request.session_id + ' logged in successfully'
            self.alert.show = False
            return await login_successful(wp, request.session_id, login_form.name_dict['user_name'].value)
        else:
            session_div.text = request.session_id + ' login not successful'
            self.alert.show = True

    sign_in_btn.on('click', sign_in_click)

    return wp

async def login_successful(wp, s_id, user):
    wp.delete_components()
    wp.selected_rows = {}
    users[s_id]['logged_in'] = True
    wp.display_url = 'login_successful'
    #return await main(s_id, user)

    wp.redirect = "/main"


class AgGridTbl(jp.AgGrid):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.load_pandas_frame(self.df)
        # print(self.options.rowData)

        self.options.defaultColDef.filter = True
        self.options.defaultColDef.sortable = True
        self.options.defaultColDef.resizable = True
        self.options.defaultColDef.cellStyle['textAlign'] = 'center'
        #self.options.defaultColDef.headerClass = 'font-bold'

        self.options.columnDefs[0].cellClass = ['text-black', 'bg-blue-500', 'hover:bg-blue-200']
        for col_def in self.options.columnDefs[1:]:
            col_def.cellClassRules = {
                'font-bold': 'x < 20',
                'bg-red-300': 'x < 20',
                'bg-yellow-300': 'x >= 20 && x < 50',
                'bg-green-300': 'x >= 50'
            }

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
  
    if self.value[-1] == '1':
        msg.page.components[3].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: block;"
        msg.page.components[4].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: none;"
    else:
        msg.page.components[3].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: none;"
        msg.page.components[4].style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;display: block;"
    
    print(f'tab name={self.value} was clicked' )

#engie_df = pd.read_csv('demo_data.csv', encoding="ISO-8859-1")
# critical_df = engie_df[engie_df['ActivityType']=='Critical']
# lookahead_df = engie_df[engie_df['ActivityType']=='LA']
mygroup_df = engie_df[engie_df['Responsibility']=='MECH']

def percent_changed(self, msg):
    myval = mygroup_df[mygroup_df['ActivityID']==msg.data['ActivityID']]
    engie_df.at[myval.index, 'progress'] = msg.newValue

    # c = jp.parse_html(alert_dialog_html, a=msg.page)
    # c.name_dict['alert_dialog'].value = True

    stmt = activities.update().\
        where(activities.c.ActivityID == msg.data['ActivityID']).\
        values(progress=msg.newValue)

    try:
        connection.execute(stmt)
    except:
        print('Error while updating mysql db')


def change_link_text(self, msg):
    self.style="color:black; padding: 1.5rem;"  

@jp.SetRoute('/dload_file')
def save_csv(request):
    wp = jp.WebPage()
    wp.html = str(engie_df.to_csv())
    return wp

@jp.SetRoute('/main')
async def main(request):
    wp = jp.QuasarPage()
    if not request.session_id:
        wp.redirect = '/login_test'

    header_div = jp.QDiv(text='Update Activities', a=wp, classes='m-2 p-2 w-1/4 text-xl font-semibold', style='text-align: center; font-size: large;')
    
    menu_div = jp.QDiv(a=wp, classes='m-2 p-2 w-1/2 full-height', style="display: flex; justify-content: flex-end")

    btns_div = jp.QDiv(a=menu_div, classes='m-1 p-1', style='float: right;')

    save_csv_link = jp.A(text='Download File', href='/dload_file', download='update_data.csv', a=btns_div,
             classes='inline-block m-2 p-2 text-blue text-2xl', style="padding: 1.5rem;")
    save_csv_link.on('click', change_link_text)

    log_out_btn = jp.QButton(text='Logout', classes=jp.Styles.button_bordered + ' text-black m-1 p-1', style='align: right;', a=btns_div)
    log_out_btn.s_id = request.session_id

    def log_out(self, msg):
        users[self.s_id]['logged_in'] = False
        msg.page.redirect = '/login_test'

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

    mygroup.options.columnDefs[2].editable = True

    mygroup.on('cellValueChanged', percent_changed)
    tabs.on('input', qtab_click)
    log_out_btn.on('click', log_out)

    tabcontent = jp.Div(a=wp)

    return wp

jp.justpy(login_test)

