from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import pymongo
import ssl

class LeadFormFirstPart(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "lead_form_p1"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["name", "email", "phone",]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "name": [
                self.from_text(),
            ],
            "email": [
                self.from_text(),
            ],
            "phone": [
                self.from_text (),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        #dispatcher.utter_template("utter_resume_link", tracker)  
        #dispatcher.utter_message("Please enter the Google Drive link of your Resume or CV", tracker)
        return []

class LeadFormSecondPart1(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "lead_form_p21"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["educational_qualification"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "educational_qualification": [
                self.from_text(),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        return []

class LeadFormSecondPart(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "lead_form_p2"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["resume_link"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "resume_link": [
                self.from_text(),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        return []

hr_answer=""
def save_candidate_data(tracker: Tracker):
    applicant_name = tracker.get_slot("name")
    phone_number = tracker.get_slot("phone")
    email_id = tracker.get_slot("email")
    education = tracker.get_slot("educational_qualification")
    resume_link = tracker.get_slot("resume_link")
    #resume_score = tracker.get_slot("resume_score")
    hr_answer = tracker.get_slot("hr_answer")
    #hr_answer_score = tracker.get_slot("hr_answer_score")
    #why_us = tracker.get_slot("why_us")

    candidate_data = [applicant_name, phone_number, email_id, education, resume_link,
              hr_answer]
    client = pymongo.MongoClient("mongodb+srv://Aayus:HP234567890@cluster0.gvafl.mongodb.net/Candidate_Data?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
    db = client["Candidate_Data"]
    col = db["data"]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Rasa_Chatbot"]
    mycol = mydb["data"]

    ToAdd = { "Name": applicant_name, "Phone": phone_number,
               "Email": email_id, "Education": education, "Resume": resume_link,
               "HR Answer": hr_answer }

    x = mycol.insert_one(ToAdd)

    print(candidate_data) # to print on action server

class LeadFormThirdPart(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "lead_form_p3"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["hr_answer"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "hr_answer": [
                self.from_text(),
            ],

        }

            
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        print(tracker)

        save_candidate_data(tracker)
        dispatcher.utter_template("utter_lead_q2", tracker)
        return []
