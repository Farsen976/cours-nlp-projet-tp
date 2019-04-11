import logging
from botocore.vendored import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

## ----- TODO : Change this with your instance ip address ----- ##
URL = "http://ec2-34-242-143-111.eu-west-1.compute.amazonaws.com:5001/board"
## ------------------------------------------------------------ ##

def cell_slot_to_number(cell_slot):
    row, column = 1, 1  # Default is middle
    
    if 'top' in cell_slot:
        row = 0
    elif 'bottom' in cell_slot:
        row = 2
    
    if 'left' in cell_slot:
        column = 0
    elif 'right' in cell_slot:
        column = 2
        
    cell_number = row*3 + column
    return cell_number
    
def cell_number_to_slot(cell_number):
    slots = [
        "top-left", "top", "top-right",
        "left", "middle", "right",
        "bottom-left", "bottom", "bottom-right"
    ]
    return slots[cell_number]

def handle_play(event):
    ## ----- TODO : Build the application logic with the backend and answer to the user ----- ##
    cell = event['currentIntent']['slots']["Cell"]  # Something similar to get the cell told by the user (You should change "Cell" by the name of your slot)
    cell_number = cell_slot_to_number(cell)
    
    params = {"move": cell_number}
    r = requests.put(URL, params=params)
    message = r.text
    res = r.json()
    print(res["winner"], res, r.text)
    
    #message = res['winner'] if res['winner'] != null else cell_number_to_slot(res['computer_move'])
    ## -------------------------------------------------------------------------------------- ##
    
    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }
    
def handle_restart(event):
    ## ----- TODO : Restart the game and answer to the user ----- ##
    r = requests.delete(URL)
    message = "Game started !" if r.status_code == 200 else "Error occured"
    
    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }
    ## ---------------------------------------------------------- ##

def handle_default(event):
    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': "Intent processing not implemented in lambda yet."
            }
        }
    }


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    logger.debug('userId={}'.format(event['userId']))
    logger.debug('intentName={}'.format(event['currentIntent']['name']))

    ## ----- TODO :  Change the checks by those of your intents ----- ##
    if event['currentIntent']['name'] == "FLD_CellToPlay":
        return handle_play(event)
    elif event['currentIntent']['name'] == "FLD_RestartGame":
        return handle_restart(event)
    ## -------------------------------------------------------------- ##
    else:
        return handle_default(event)
