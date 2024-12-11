import sqlalchemy as sqla
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://doadmin:AVNS_dHqY101i_n8FteRE3-j@messengerapp-db-do-user-18147258-0.j.db.ondigitalocean.com:25060/defaultdb')
inspection = sqla.inspect(engine)
