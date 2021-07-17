from sqlalchemy import create_engine, Table, MetaData
import pandas as pd

keep_columns = ['ActivityID',  'ACtivityDesc', 'progress' ,  'kiritsch' ,  'Groep' ,  'Responsibility' , 
                 'startdatum', 'einddatum', 'Lijn' ,   'LA' ,  'PreDesc' ]

try:
    db_connection_str = 'mysql+pymysql://able3:Etraas-Demo@localhost/able3'
    db_engine = create_engine(db_connection_str)

    connection = db_engine.connect()
    metadata = MetaData()
    activities = Table('activities', metadata, autoload=True, autoload_with=db_engine)

    user_df = pd.read_sql('SELECT * FROM sec_users', con=db_engine)
    engie_df = pd.read_sql('SELECT * FROM activities', con=db_engine)

    for column in engie_df.columns:
        if column not in keep_columns:
            engie_df.drop(column, axis=1, inplace=True)

except Exception as e:
    print("Exeception occured:{}".format(e))
