import logging
import azure.functions as func

weather_data_persist = func.Blueprint()


# app = func.FunctionApp()
# Comment out bottom if above has been commented out. 
# app.register_functions(weather_data_persist.blueprint)

# app comes from top level function_app.
@weather_data_persist.function_name(name="EventHubTrigger1")
@weather_data_persist.event_hub_message_trigger(arg_name="myhub", 
                               event_hub_name="weatherstreamingeventhub",
                               connection="WeatherAPIFuncEHConnectStr") 
def event_hub_persist(myhub: func.EventHubEvent):
    print(myhub.body_as_str())
    logging.info('Python EventHub trigger processed an event: %s',
    myhub.get_body().decode('utf-8'))
    
