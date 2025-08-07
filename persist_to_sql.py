import logging
import json
import azure.functions as func

persist_sql = func.Blueprint()

@persist_sql.event_hub_message_trigger(arg_name = 'myhub',
                                       event_hub_name = 'weatherstreamingeventhub', 
                                       connection = 'WeatherAPIFuncEHConnectStrListen'
                                       )
@persist_sql.sql_output(arg_name = 'outputTable', command_text = '[dbo].[weather2]',
                        connection_string_setting = 'SqlConnectionString')
def persist_sql_trigger(myhub: func.EventHubEvent, outputTable: func.Out[func.SqlRow]):
    try:
        event_body = myhub.get_body().decode('utf-8')
        event_data_json = json.loads(event_body)
        
        if event_data_json is not None:
            location = event_data_json['location']
            name = location['name']
            region = location['region']
            
            current = event_data_json['current']                 
            temp_c = current['temp_c']
            temp_f = current['temp_f']
            wind_mph = current['wind_mph']
            last_updated = current['last_updated']
    
        row = {           
            'name': name,
            'region': region,
            'temp_c': temp_c,
            'temp_f': temp_f,
            'wind_mph': wind_mph,
            'last_updated': last_updated
        }
        outputTable.set(func.SqlRow(row))
        return logging.info(f'successful insert into SQL table')
    except Exception as ex:
        logging.error(f'Exception occurred: {str(ex)}')
        raise ex
        

    
