from flask import session as flasksession, request
import twilio.twiml
from twilio.rest import TwilioRestClient
import constants as c
from specificsearch import SearchForVenue
from user_report_model import Status, Session as SQLsession, connect
from datetime import datetime
from database_update import UpdateDatabase
import re

def update_db_from_twilio(venuename, venuecity):
    
    return SearchForVenue().likely_venues(venuename, venuecity)


class Twilio(object):
    """docstring for Twilio"""
    def __init__(self):
        super(Twilio, self).__init__()
    
    def conversation_counter(self, body, response):
        self.counter                = flasksession.get('counter', 0)
        self.counter               += 1
        flasksession['counter']     = self.counter

        

        if self.counter == 1:
            return Twilio().new_user_report(body, response)
        
        if self.counter == 2:
            return Twilio().corrected_report(body, response)
        
        if self.counter == 3:
            return Twilio().corrected_report(body, response)
        
        if self.counter > 3:
            flasksession.clear()
            with response.message() as message:
                message.body = "{0}".format(c.HELP_MESSAGE)
                flasksession.clear()
            return str(response)

    def new_user_report(self,body,response):
        body = filter(None, re.split("[:, ;/-]", body))

        if body[-1] == 'slammed':
            status_code = 1
            body = body [:-1]
        elif body[-1] == 'full':
            status_code = 0
            body = body[:-2]
        else:
            with response.message() as message:
                message.body = "{0}".format(c.HELP_MESSAGE)
                flasksession.clear()

        
        try:
            SearchForVenue().test_user_input(body[0]+' '+body[1]+' '+body[2])
            city=body[0]+' '+body[1]+' '+body[2]
            venue_name = body[3:]
            print venue_name
            venue_string = ''
            for i in venue_name:
                venue_string = venue_string+i +' '
            venue_string = venue_string.strip()
        except:
            try:
                SearchForVenue().test_user_input(body[0]+' '+body[1])
                city = body[0]+' '+body[1]
                venue_name = body[2:]
                venue_string = ''
                for i in venue_name:
                    venue_string = venue_string+i +' '
                venue_string = venue_string.strip()
            except:
                try:
                    SearchForVenue().test_user_input(body[0])
                    city=body[0]
                    venue_name = body[1:]
                    venue_string = ''
                    for i in venue_name:
                        venue_string = venue_string+i +' '
                    venue_string = venue_string.strip()
                except:
                    with response.message() as message:
                        message.body = "{0}".format(c.HELP_MESSAGE)
                        flasksession.clear()  

        venues = update_db_from_twilio(venue_string, city)

        flasksession['status_code']=status_code
        
        flasksession['first_id'] = UpdateDatabase().add_new_rating(venues[0]['name'], venues[0]['id'], status_code)
        print flasksession['first_id']
            # UNICODE #
        alternate_options = []        
        for i in range(len(venues)):
            alternate_options.append(((venues[i]['name']).encode(), venues[i]['location']['formattedAddress'][0], venues[i]['id']))
            if i == 3:
                break

        alternate_options = list(enumerate(alternate_options))
        flasksession['alternate_options'] = alternate_options
    
        alternate_string = ''
        for i in range(1, len(alternate_options)):
            alternate_string = alternate_string + str(alternate_options[i][0]) + ": " + alternate_options[i][1][0] + ", " + alternate_options[i][1][1] + "\n"


    # Setting up variables to be used in Response Message. primary_venue_name
    # is the first response from the foursquare API and is the assumed correct
    # match for the search, unless user indicates otherwise.
        primary_venue_name      = (venues[0]['name']).encode()
        primary_venue_address   = (venues[0]['location']['formattedAddress'][0]).encode()
   
        slammed_confirmation_message    = """Thanks for letting us know that %s at %s is THE WORST. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)
        safe_confirmation_message       = """Thanks for letting us know that %s at %s is a Safe Zone. We'll let the other misanthropes know.""" % (primary_venue_name, primary_venue_address)
    # print len(venues)

    # Check to see if more than one venue in response. There will be no
    # alternates offered if query only results in one response.
        if len(venues) > 1:
            with response.message() as message:
                if status_code == 1:
                    message.body = "{0}\n{1}\n{2}".format(slammed_confirmation_message,
                                                c.ALTERNATE_INTRO, alternate_string)
                    return unicode(response).encode("utf-8")
                elif status_code == 0:
                    message.body = "{0}\n{1}\n{2}".format(safe_confirmation_message,
                                                c.ALTERNATE_INTRO, alternate_string)
                    return unicode(response).encode("utf-8")

    # For queries that result in a single response. No alternates provided.
        elif len(venues) == 1:
            with response.message() as message:
                if status_code == 1:
                    message.body = "{0}".format(slammed_confirmation_message)
                elif status_code == 0:
                    message.body = "{0}".format(safe_confirmation_message)

        else:
            with response.message() as message:
                message.body = "{0}".format(c.HELP_MESSAGE)

        
        flasksession.clear()
        return unicode(response).encode("utf-8")

            
    def corrected_report(self, body, response):
        alternate_options = flasksession.get('alternate_options', 0)
        status_code = flasksession.get('status_code', 0)

        first_id = flasksession.get('first_id', 0)
        alternate_enumerated_options = ['1','2','3']

        if body in alternate_enumerated_options:
            body = int(body)
            response_list = []
            for i in alternate_options:
                response_list.append(i[1])

            updated_response_message = """Got it, you meant %s at %s.""" % (response_list[body][0],
                                                                                response_list[body][1])

            UpdateDatabase().delete_by_id(first_id)
            UpdateDatabase().add_new_rating(response_list[body][0], response_list[body][2], status_code)

            with response.message() as message:
                        message.body = "{0}".format(updated_response_message)
            flasksession.clear()
        
        else:
            try:
                body = int(body)
                with response.message as message:
                    message.body = "Sorry! %r is not a valid option. Please pick 1, 2, or 3." % body
            except ValueError:
                return Twilio().new_user_report(body, response)
                flasksession.clear()


        return unicode(response).encode("utf-8")


