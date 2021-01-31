import time 
import asyncio
import re
from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import List, Dict, Optional

app = FastAPI()

@app.get('/healthcheck', status_code=200)
async def healthcheck():
    return 'Ecce Response Server is all ready to go!'


def pause_list() -> List:
    """
    Returns a list of utterances after which to pause because of 
    Twillio bug in order of delivery for media messages 
    """
    pause_list = ['utter_ask_fractions_parts_mcq_1',
    'utter_ask_fractions_parts_mcq_2',
    'utter_ask_fractions_parts_mcq_3',
    'utter_ask_fractions_wholes_nrq_3'
    ]

    return pause_list

def look_up_response(template : str) -> Dict: 
    """
    Return a Dictionary ready to be sent back to Rasa
    """
    # TODO - Turn this into a DataBase Query
    response_dict = response_dict = {'utter_ask_first_form_age': [{'text': 'How old are you?'}],
    'utter_ask_first_form_userName': [{'text': 'What is your name?'}],
    'utter_ask_fractions_halves_frq_1': [{'text': '*WHY* do you think this split '
                                                "is 'fair'?"}],
    'utter_ask_fractions_halves_mcq_1': [{'image': 'https://ecceapi.herokuapp.com/media/fractions_halves_mcq_1.png',
                                        'text': 'Imagine it is lunch time at '
                                                '{school} and {friend_1} forgot '
                                                'to bring their tiffin. You '
                                                'decide to split your last '
                                                '{object_1} with your friend.\n'
                                                'Which way of splitting do you '
                                                'think is fair to the both of '
                                                'you?'}],
    'utter_ask_fractions_parts_mcq_3': [{'text': 'After showing off your fraction '
                                                'skills to {friend_2}, they are '
                                                'upset you get more than they do '
                                                ':( Now, {friend_2} wants to RE '
                                                'SPLIT the {object_2} EQUALLY '
                                                '(into halves). Do you get more '
                                                'or less than before?'}],
    'utter_ask_fractions_parts_mcq_4': [{'text': 'So is ½ of the 6 {object_2} '
                                                'more or less than ⅓ of the 6 '
                                                '{object_2}?'}],
    'utter_ask_fractions_parts_nrq_1': [{'text': 'I love {object_2} too 😋!\n'
                                                '{friend_2} has 6 {object_2}. '
                                                'How many do you each get if you '
                                                'split them equally between the '
                                                'three of you?'}],
    'utter_ask_fractions_parts_story_form_object_2': [{'text': 'Right after you '
                                                                'and {friend_1} '
                                                                'finished your '
                                                                'yummy (and '
                                                                'equal!) '
                                                                '{object_1}, '
                                                                '{friend_2} sits '
                                                                'at your table. '
                                                                '{friend_2} says '
                                                                'they will share 1 '
                                                                'of the 4 '
                                                                'snacks.They have '
                                                                'biscuits, grapes, '
                                                                'and chocolates. '
                                                                'Which is your '
                                                                'favorite?'}],
    'utter_ask_fractions_wholes_frq_1': [{'text': 'Now that you are splitting a '
                                                'box of 4 mangoes, what would '
                                                'you consider as the whole?'}],
    'utter_ask_fractions_wholes_nrq_1': [{'text': 'The farmer is splitting the 12 '
                                                'mangoes, which is the whole, '
                                                'into 3 boxes, so into 3 equal '
                                                'parts. How many mangoes are in '
                                                'each box?'}],
    'utter_ask_fractions_wholes_nrq_2': [{'text': 'In fractions, how much of the '
                                                '*whole* is in each box?'}],
    'utter_ask_fractions_wholes_nrq_4': [{'text': 'In fractions what share did '
                                                'each member of your family '
                                                'get?'}],
    'utter_ask_fractions_wholes_nrq_5': [{'text': 'Now that you’ve got one mango '
                                                'all to yourself, you want to '
                                                'cut your mango into 6 equal '
                                                'pieces. What fraction of the '
                                                'whole mango is each piece?'}],
    'utter_ask_friend_1': [{'text': 'Which of your friends do you like to eat '
                                    'with the most?'}],
    'utter_ask_rephrase': [{'text': "I'm sorry, I didn't quite understand that. "
                                    'Could you rephrase?'}],
    'utter_check_in': [{'text': 'Does that make sense?'},
                        {'text': 'Do you understand?'},
                        {'text': 'Is that clear?'},
                        {'text': 'Got it?'}],
    'utter_confirm': [{'text': 'Are you sure you want to stop? 🥺'},
                    {'text': 'Do you want to take a break?'},
                    {'text': 'So are you done for now?'}],
    'utter_correct': [{'text': 'That was right!'},
                    {'text': 'Right on {userName} :)'},
                    {'text': "Yes that's so right!"},
                    {'text': 'Nice one'}],
    'utter_encouragment': [{'text': "That's awesome"},
                            {'text': 'Yes! Lets do it'},
                            {'text': 'You are doing amazing'}],
    'utter_end_chat_session': [{'text': "You've done an awesome job! Lets chat "
                                        'again soon.'}],
    'utter_first_time_confirm': [{'text': 'Is this information correct?\n'
                                        'Name: {userName}\n'
                                        'Age: {age}'}],
    'utter_fractions_demo_conclusion': [{'text': 'Thats the end of the demo '
                                                'lesson. We want enable '
                                                'educators to make lessons like '
                                                'these with no code.'}],
    'utter_fractions_halves_conclusion': [{'text': 'In fractions we would say '
                                                    'that you and {friend_1} each '
                                                    'got *one half (½)* of the '
                                                    '*whole*'}],
    'utter_fractions_halves_conclusion_animation': [{'image': 'https://ecceapi.herokuapp.com/media/fractions_halves_animation.mp4',
                                                    'text': 'Check out this '
                                                            'animation'}],
    'utter_fractions_halves_frq_1_explanation': [{'text': 'Because when you split '
                                                        '{object_1} like that, '
                                                        'both you and '
                                                        '{friend_1} get the '
                                                        'same, or an equal, '
                                                        'amount. You are '
                                                        'splitting the '
                                                        '{object_1} into two '
                                                        'halves!'}],
    'utter_fractions_halves_introduction': [{'text': 'Yay! Fractions from the '
                                                    'start it is. To start we '
                                                    'are going to talk about '
                                                    'sharing food.'}],
    'utter_fractions_parts_conclusion': [{'text': 'And that is PARTS!'}],
    'utter_fractions_parts_mcq_1_explanation': [{'image': 'https://ecceapi.herokuapp.com/media/audio/fractions_parts_mcq_1_explanation.mp3',
                                                'text': 'Listen to this!'}],
    'utter_fractions_parts_mcq_1_options': [{'text': 'Lets try again. This time '
                                                    "I'll give you options - 1/6 "
                                                    ', 2/3 , 1/3, 1'}],
    'utter_fractions_parts_mcq_2_explanation': [{'image': 'https://ecceapi.herokuapp.com/media/fractions_parts_mcq_2_explanation.mp4',
                                                'text': 'This animation might '
                                                        'help!'}],
    'utter_fractions_parts_mcq_3_explanation': [{'text': 'You are splitting the '
                                                        'food into two equal '
                                                        'parts instead of three! '
                                                        'Because there are fewer '
                                                        'people to share with, '
                                                        'now each person gets '
                                                        'more.'}],
    'utter_fractions_parts_mcq_4_explanation': [{'image': 'https://ecceapi.herokuapp.com/media/audio/fractions_parts_mcq_4_explanation.mp3',
                                                'text': 'Check this out'}],
    'utter_fractions_parts_nrq_1_explanation': [{'image': 'https://ecceapi.herokuapp.com/media/audio/fractions_parts_nrq_1_explanation.ogg',
                                                'text': 'Listen to this!'}],
    'utter_fractions_wholes_conclusion': [{'text': 'Did you realise that the '
                                                    'whole changed depending on '
                                                    "what you're splitting?!"}],
    'utter_fractions_wholes_conclusion_1': [{'text': 'When the farmer was '
                                                    'splitting 12 mangoes into 3 '
                                                    'equal boxes, you identified '
                                                    '12 mangoes as the whole!'}],
    'utter_fractions_wholes_conclusion_2': [{'text': 'Later, when you had to '
                                                    'share the box of 4 mangoes '
                                                    'with your family, you '
                                                    'identified 4 mangoes as the '
                                                    'new whole!'}],
    'utter_fractions_wholes_conclusion_3': [{'text': 'Finally, when you were '
                                                    'ready to eat one mango - '
                                                    'you cut it into 6 slices. 1 '
                                                    'mango was now the whole you '
                                                    'are splitting into 6 '
                                                    'parts!In fact, Fractions '
                                                    'are how you divide/split '
                                                    '*any whole*'}],
    'utter_fractions_wholes_frq_1_explanation': [{'image': 'https://ecceapi.herokuapp.com/media/audio/fractions_wholes_frq_1_explanation.ogg',
                                                'text': 'Hear why!'}],
    'utter_fractions_wholes_introduction': [{'text': 'A farmer has a total of 12 '
                                                    'MANGOES 🥭🥭🥭 He needs to '
                                                    'split them into 3 boxes, '
                                                    'equally. You can help him '
                                                    'with FRACTIONS!'}],
    'utter_fractions_wholes_introduction_hint': [{'text': 'Whenever we are '
                                                        'dealing with fractions '
                                                        'it’s always a good '
                                                        'idea to figure out '
                                                        'what the *whole* is '
                                                        'and what the *part* '
                                                        'is.'}],
    'utter_fractions_wholes_nrq_1_explanation': [{'text': '12 split equally into '
                                                        '3 parts is 4. You can '
                                                        'check that this is '
                                                        'right by adding '
                                                        'together all 3 equal '
                                                        'parts - 4 mangoes + 4 '
                                                        'mangoes + 4 mangoes is '
                                                        '12 mangoes!'}],
    'utter_fractions_wholes_nrq_2_explanation': [{'text': 'Each box is 1 part out '
                                                        'of 3 boxes.  or ⅓ of '
                                                        'the whole.'}],
    'utter_fractions_wholes_nrq_3_explanation': [{'text': '1 mango each since 4 '
                                                        'mangoes split among 4 '
                                                        'people (equally) is '
                                                        '1!'}],
    'utter_fractions_wholes_nrq_4_explanation': [{'text': 'Each got 1 out of 4 '
                                                        'parts, and so the '
                                                        'fraction is ¼'}],
    'utter_fractions_wholes_nrq_5_explanation': [{'text': 'You are cutting the '
                                                        'mango into 6 equal '
                                                        'parts so the fraction '
                                                        'is 1/6'}],
    'utter_goodbye': [{'text': 'Bye! 👋🏾'},
                    {'text': 'Bye bye. Chat with you soon :)'}],
    'utter_greet': [{'text': 'Hello!'}, {'text': 'Hey {userName}'}],
    'utter_greet_first_time': [{'text': 'Hello! 👋🏾 My name is Ecce. I am your new '
                                        'digital, personal tutor 🙋🏽\u200d♀️ Lets '
                                        'get chatting!'}],
    'utter_greet_first_time_followup': [{'text': 'I do not think we have met '
                                                'before. Before we start, lets '
                                                'get to know each other a little '
                                                'bit.'}],
    'utter_incorrect': [{'text': 'Not quite right {userName} 🧐'},
                        {'text': 'Almost there but not yet 🧐'},
                        {'text': 'So close! I am sure you will get it next time '
                                '🧐'},
                        {'text': 'Nope. Nice try though! 🧐'}],
    'utter_lesson_options': [{'text': 'In our lesson on fractions, you can start '
                                    'from the beginning from HALVES or jump to '
                                    'our later lesson on WHOLES if fractions '
                                    'are not new :) So which will it be?'}],
    'utter_please_rephrase': [{'text': "I'm sorry, I didn't quite understand "
                                        'that. Could you rephrase?'}],
    'utter_ask_fractions_parts_mcq_1': [{'text': 'Tell us in fractions, what '
                                                    'part of the whole (6 '
                                                    '{object_2}) did you get?'}],
    'utter_ask_fractions_parts_mcq_2': [{'text': '{friend_1} gives you their '
                                                    'share. Now you have 2 out '
                                                    'of the 3 equal parts. In '
                                                    'fractions we would say you '
                                                    'have ⅔ (two-thirds) of the '
                                                    'whole. Do you get more or '
                                                    'less than {friend_2}?'}],
    'utter_ask_fractions_wholes_nrq_3': [{'text': 'After splitting the '
                                                        'mangoes evenly among your '
                                                        'family of 4, how many '
                                                        'mangoes does each person '
                                                        'get?'}],
    'utter_start_next': [{'text': 'Would you like to go to the next lesson?'},
                        {'text': 'You are doing great. Want to start the next '
                                'lesson?'},
                        {'text': 'Should we keep going?'}],
    'utter_wrong_format': [{'text': 'There is something wrong about the value. '
                                    '{err}'}],
    'utter_you_are_welcome': [{'text': 'You are welcome {userName}!'},
                            {'text': 'The pleasure is all mine!'},
                            {'text': 'You are very welcome!! :)'}]
    }
    # TODO: Handle error case when not found in list
    return response_dict[template][0]

def check_text_slots(response_dict) -> bool:
    """ 
    Takes in response_dict and check if it contains 
    string pattern '{' TEXT '}'
    Returns true if found, else false
    """
    if re.findall("(?<=\{)(.*?)(?=\})", response_dict['text']):
        print(f"Filling slot for {response_dict['text']}")
        return True
    else:
        False
def fill_slots(response_dict : Dict, tracker_slot_dict : Dict):
    """ 
    Takes in a response_dict with text and the tracker after checking slots need to be filled
    Returns response dict with slots filled if they are in the tracker
    """
    filled_response_dict = response_dict
    slots_to_fill = re.findall("(?<=\{)(.*?)(?=\})", response_dict['text'])
    # Remove duplicates 
    slots_to_fill = list(set(slots_to_fill))
    for slot in slots_to_fill:
        if slot in tracker_slot_dict.keys():
            filled_response_dict['text'] = filled_response_dict['text'].replace("{" + str(slot) + "}", str(tracker_slot_dict[slot]))
    print(filled_response_dict['text'])
    return filled_response_dict


class NlgPost(BaseModel):
    template: str
    arguments: Optional[Dict]
    tracker : Optional[Dict]
    channel : Optional[Dict]

@app.get("/")
def root():
    return {"message": "hello world again"}

@app.post("/nlg/")
def print_and_respond(item : NlgPost):
    print(item.template)
    response_dict = look_up_response(item.template)
    if 'text' in response_dict.keys() and check_text_slots(response_dict):
        response_dict = fill_slots(response_dict, item.tracker['slots'])
    if item.template in pause_list():
        time.sleep(5) # Add delay between each explanation
        print(f"slept for {item.template}")
    return response_dict

@app.get("/users/{user_id}")
def get_user(user_id: str):
    """
    We expect a user_id and return a json blob
    """
    return {"user_id": user_id}


@app.get("/sleep_slow")
def sleep_slow():
    r = time.sleep(1)
    return {"status": "done"}

@app.get("/sleep_fast")
async def sleep_fast():
    r = await asyncio.sleep(1)
    return {"status":"done"}


