import pandas as pd
from flask import current_app


def __find_and_add_new_rows(connection, new_rows_dataframe):
    current_app.logger.info('   - Adding new rows to matches and user_info tables')

    # The matches and user_info tables are linked in the postgres database via the matches table ID,
    # so adding a new row to matches should happen concurrently with the write to user_info.
    # We could add some custom logic to handle this step, but at least in the short term until MVP
    # review, it would be easier to write the extra columns into a joint table, then split them
    # afterwards (and more maintainable than figuring out how to manually assign the automatic (nextval?)
    # matches ID from postgres and sqlalchemy).
    new_rows_dataframe = new_rows_dataframe.where(pd.notnull(new_rows_dataframe), None)  # np.nan -> None
    new_rows_dataframe['new_row_flag'] = True
    connection.execute('ALTER TABLE matches ADD COLUMN name VARCHAR, ADD COLUMN email VARCHAR, ADD COLUMN source VARCHAR, ADD COLUMN new_row_flag BOOLEAN')
    new_rows_dataframe.to_sql('matches', connection, index=False, if_exists='append')
    
    # Using the temporary table (with auto-assigned matches._id) to write to user_info, and remove
    # the temporarily added columns from matches.
    new_matches_rows = pd.read_sql('SELECT * FROM matches WHERE new_row_flag IS NOT NULL', connection)
    new_user_info_columns = new_matches_rows.rename(columns={'_id': 'matches_id'})[['matches_id', 'name', 'email', 'source']]
    new_user_info_columns.to_sql('user_info', connection, index=False, if_exists='append')
    connection.execute('ALTER TABLE matches DROP COLUMN email, DROP COLUMN name, DROP COLUMN source, DROP COLUMN new_row_flag')
    


def __find_and_update_rows(connection, rows_to_update):
    current_app.logger.info('   - Updating rows to matches table')
    matches_df = pd.read_sql('select * from matches', connection)
    matches_df.update(rows_to_update)
    #todo: replace with ORM insert (currently doesn't use the correct schema)
    matches_df.to_sql('matches', connection, index=False, if_exists='replace')


def __create_new_user(connection, matches_id, name, email, source):
    # TODO: Take a list of users
    current_app.logger.info('   - Creating new User')
    user_df = pd.read_sql(
        'select * from user_info',
        connection
    )
    user_id = None
    try:
        user_id = user_df[user_df.matches_id == matches_id][user_df.source == source]['_id'][0]
    except KeyError:
        pass

    if user_id is not None:
        new_user = pd.DataFrame({
            '_id': [user_id],
            'matches_id': [matches_id],
            'name': [name],
            'email': [email],
            'source': [source]
        })
    else:
        new_user = pd.DataFrame({
            'matches_id': [matches_id],
            'name': [name],
            'email': [email],
            'source': [source]
        })
    user_df.update(new_user)
    user_df.to_sql('user', connection, index=False, if_exists='replace')


def start(connection, rows_for_matches_df):
    # Create a simple table with the following values:
    # ------------> matches_id (primary key), shelterluvpeople_id, volgistics_id, salesforce_id, created_date, archived_date
    # shelterluvpeople[[id]]
    # volgistics[[number]]
    # salesforcecontacts[[account_id]]

    current_app.logger.info('Start creating Matches table')

    if "new_matches" in rows_for_matches_df:
        new_rows_dataframe = pd.DataFrame(rows_for_matches_df["new_matches"])
        __find_and_add_new_rows(connection, new_rows_dataframe)

    if "updated_rows" in rows_for_matches_df:
        updated_rows_dataframe = pd.DataFrame(rows_for_matches_df["updated_rows"])
        __find_and_update_rows(connection, updated_rows_dataframe)

    current_app.logger.info('   - Finished creating Matches table')
