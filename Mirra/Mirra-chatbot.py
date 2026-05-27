import re
import random as random
from chatbot_base import ChatbotBase

print('\n'*100)
class MIRRA(ChatbotBase):
    def __init__(self, name="Mirra"):
        ChatbotBase.__init__(self,name)
        self.conversation_is_active = True
        
        # List of tuples with regex and replace string pairs
        self.pronoun_pairings = [
            (r"\b(am)\b", "are"),
            (r"\b(was)\b", "were"),
            (r"\b(i)\b", "you"),
            (r"\b(i'd)\b", "you would"),
            (r"\b(i'?ve)\b", "you have"),
            (r"\b(i'll)\b", "you will"),
            (r"\b(my)\b", "your"),
            (r"\b(are)\b", "am"),
            (r"\b(you'?ve)\b", "I have"),
            (r"\b(you'?ll)\b", "I will"),
            (r"\b(your)\b", "my"),
            (r"\b(your'?s)\b", "mine"),
            (r"\b(you)\b", "me"),
            (r"\b(me)\b", "you")
        ]
        
        # List of default responses if no matches are made
        self.default_responses = ["It sounds like this has been weighing on you. Can you share more?",
                            "That's an interesting perspective.",
                            "Let's take a moment to reflect on that, why do you think it matters so much?",
                            "It's okay to feel this way, you don't have to feel anxious.",
                            "What do you think this situation shows?",
                            "How does this word or action affect your mood?",
                            "I know this will be upsetting.",
                            "Sometimes it's hard to see clearly in the moment.",
                            "Have you thought about fighting back?",
                            "What would you say if you could express yourself without fear of judgment?"]
        
        # List of tuples with contain a regex and a set of reponses
        self.regex_and_response = [
            #Ask what happened
            ("he said (.+)", [
                "How did it make you feel when he said {x}?",
                "Do you agree with his statement about {x}?",
                "Could it be that his words are more about him than about you?"
            ]),

            ("she said (.+)", [
                "How did it make you feel when she said {x}?",
                "Do you agree with her statement about {x}?",
                "Could it be that her words are more about her than about you?"
            ]),

            ("they said (.+)", [
                "How did it make you feel when they said {x}?",
                "Do you agree with their statement about {x}?",
                "Could it be that their words are more about them than about you?"
            ]),

            #Questions about self-worth
            ("i feel worthless (.+)", [
                "I'm sorry you're feeling this way. Can we explore why you feel worthless?",
                "Do you think someone's words or actions led you to feel this way?",
                "How can we reframe this feeling to see your true value?"
            ]),

            #Deal with criticism
            ("he criticize me so much (.+)", [
                "Are you sure his criticism reflects you and not him?",
                "How does his criticism make you feel about yourself?",
                "What would you say to him if you could express yourself freely?"
            ]),

            ("she criticize me so much (.+)", [
                "Are you sure her criticism reflects you and not her?",
                "How does her criticism make you feel about yourself?",
                "What would you say to her if you could express yourself freely?"
            ]),

            ("they criticize me so much (.+)", [
                "Are you sure their criticism reflects you and not them?",
                "How does their criticism make you feel about yourself?",
                "What would you say to them if you could express yourself freely?"
            ]),

            #Deal with put-downs
            ("i am not good enough (.+)", [
                "Why do you feel you're not good enough?",
                "Have someone made you feel this way, or is it something else?",
                "What could help you see yourself differently?"
            ]),

            #Dealing with the after-effects of manipulative speech
            ("he said i always (.+)", [
                "In this case you can actually say 'Why do you think I always {x}?'",
                "In this case you can actually say 'Does it help to think this way about me?'",
                "In this case you can actually say 'Could it be that you're focusing on absolutes to avoid another perspective?'"
            ]),

            ("she said i always (.+)", [
                "In this case you can actually say 'Why do you think I always {x}?'",
                "In this case you can actually say 'Does it help to think this way about me?'",
                "In this case you can actually say 'Could it be that you're focusing on absolutes to avoid another perspective?'"
            ]),

            ("they said i always (.+)", [
                "In this case you can actually say 'Why do you think I always {x}?'",
                "In this case you can actually say 'Does it help to think this way about me?'",
                "In this case you can actually say 'Could it be that you're focusing on absolutes to avoid another perspective?'"
            ]),

            ("he said i never (.+)", [
                "In this case you can actually say 'What makes you feel that I never {x}?'",
                "In this case you can actually say 'Is it possible you're generalizing to make a point?'"
            ]),

            ("she said i never (.+)", [
                "In this case you can actually say 'What makes you feel that I never {x}?'",
                "In this case you can actually say 'Is it possible you're generalizing to make a point?'"
            ]),

            ("they said i never (.+)", [
                "In this case you can actually say 'What makes you feel that I never {x}?'",
                "In this case you can actually say 'Is it possible you're generalizing to make a point?'"
            ]),

            #For control and border issues
            ("my own decisions (.+)", [
                "Do you feel like someone is trying to control your choices?",
                "What would making your own decisions mean to you?",
                "How can we work together to reclaim your autonomy?"
            ]),

            ("they always make me feel guilty (.+)", [
                "How does their behavior make you feel guilty?",
                "What would happen if you didn't let guilt influence your actions?",
                "Do you think their actions are meant to control your feelings?"
            ]),

            #Emotional manipulation of rhetorical questions
            ("i being too sensitive (.+)", [
                "Why do you think you're being 'too sensitive'?",
                "Is it possible they're deflecting responsibility for their behavior?",
                "How do you want to respond to the situation instead of doubting yourself?"
            ]),

            ("he respect me (.+)", [
                "Do you feel his lack of respect is intentional?",
                "What would gaining his respect look like to you?",
                "Could his behavior be more about him than about you?"
            ]),

            ("she respect me (.+)", [
                "Do you feel her lack of respect is intentional?",
                "What would gaining her respect look like to you?",
                "Could her behavior be more about her than about you?"
            ]),

            ("they respect me (.+)", [
                "Do you feel their lack of respect is intentional?",
                "What would gaining their respect look like to you?",
                "Could their behavior be more about them than about you?"
            ]),

            #Explore boundaries
            ("afraid to say (.+)", [
                "Why do you think saying no feels so difficult?",
                "Do you think your fear is rooted in their possible reaction?"
            ]),

            ("afraid to (.+)", [
                "Why do you find it difficult to implement {x}?",
                "What does it mean to you to cross that line?"
            ]),

            #Training responses to operant discourse
            ("others are better than me (.+)", [
                "What makes you feel that others think they are better than you?",
                "Could it be that this is more about how you are feeling right now?",
                "Why do you think it's important to compare people with each other?"
            ]),

            ("he don't care about me (.+)", [
                "What makes you feel that he don't care?",
                "Could there be another way to interpret his behavior?",
                "How do you wish he showed that he care?"
            ]),

            ("she don't care about me (.+)", [
                "What makes you feel that she don't care?",
                "Could there be another way to interpret her behavior?",
                "How do you wish she showed that she care?"
            ]),

            ("they don't care about me (.+)", [
                "What makes you feel that they don't care?",
                "Could there be another way to interpret their behavior?",
                "How do you wish they showed that they care?"
            ]),

            #Learn the default calm response
            ("if ([^?]+)", [
                "What would it mean if {x} happened?",
                "Do you think worrying about {x} is helpful or harmful?",
                "How likely is it that {x} will actually happen?"
            ]),

            #Modified based on ELIZA
            ("i need (.+)", [
                "What makes you feel that you need {x}?",
                "Do you think needing {x} comes from external pressure or personal desire?",
                "How would having {x} make a difference in your life?"
            ]),

            ("why don'?t you ([^?]+)?", [
                "What makes you think I don't {x}?",
                "Could this be about your expectations of me?",
                "What do you think would happen if I {x}?"
            ]),

            ("why can'?t i ([^?]+)?", [
                "What do you feel is stopping you from {x}?",
                "If you could {x}, what would it mean for you?",
                "Is it possible that you're being too hard on yourself?"
            ]),

            ("i can'?t ([^?]+)", [
                "What makes you believe you can't {x}?",
                "How would you approach it if you felt confident to try {x}?",
                "What could help you feel more capable of {x}?"
            ]),

            ("i am (.+)", [
                "Why do you identify as {x}?",
                "How long have you felt like this about yourself?"
            ]),

            ("i'm (.+)", [
                "How does being {x} influence how you see yourself?",
                "What makes you feel like you're {x}?",
                "Why do you choose to describe yourself as {x}?"
            ]),

            ("are you ([^?]+)?", [
                "Why does it matter to you if I am {x}?",
                "Would it change how you feel if I were {x}?",
                "Perhaps your question about me being {x} is reflecting something about you."
            ]),

            ("what ([^?]+)", [
                "Why do you think this is important to ask?",
                "How do you think an answer would help you?",
                "What do you feel is the underlying reason for this question?"
            ]),

            ("how ([^?]+)", [
                "What do you think the answer might be?",
                "How would you feel if you knew the answer?",
                "What are you really hoping to understand?"
            ]),

            ("because (.+)", [
                "Is this the only reason, or are there others?",
                "What else could explain {x}?",
                "How does {x} connect to how you're feeling?"
            ]),

            ("(.*) sorry (.*)", [
                "You don't always need to apologize. Why do you feel the need to say sorry?",
                "When you apologize, what emotions come up for you?",
                "Is your apology addressing something important, or is it a habit?"
            ]),

            ("i think (.+)", [
                "What makes you think {x}?",
                "Do you believe this fully, or do you have doubts?",
                "How does thinking {x} affect how you feel?"
            ]),

            ("(.*) friend (.*)", [
                "How do your friends support you in situations like this?",
                "When you think of a good friend, what qualities come to mind?",
                "What role do your friends play in helping you feel supported?"
            ]),

            ("yes", [
                "You seem sure about that. Can you tell me more?",
                "What makes you so confident about this?",
                "How does saying yes make you feel?"
            ]),

            ("(.*) computer(.*)", [
                "Does talking to me feel different from talking to a person?",
                "How do you feel about technology being part of this conversation?",
                "What are your thoughts on the role of computers in emotional support?"
            ]),

            ("is it ([^?]+)", [
                "Why do you feel that it might be {x}?",
                "What would it mean if it were {x}?",
                "If it wasn't {x}, how would that change things for you?"
            ]),

            ("it is (.+)", [
                "You seem certain about {x}. What leads you to this conclusion?",
                "If I suggested it might not be {x}, how would that make you feel?"
            ]),

            ("can you ([^?]+)?", [
                "Why do you think I might not {x}?",
                "If I could {x}, what would that mean for you?",
                "What makes you ask if I can {x}??"
            ]),

            ("can i ([^?]+)?", [
                "What do you think is stopping you from {x}?",
                "Do you feel ready to try {x}?",
                "What would achieving {x} mean for you?"
            ]),

            ("you are (.+)", [
                "What makes you believe I am {x}?",
                "How does thinking that I'm {x} affect our conversation?",
                "Could this perception of me be reflecting something about you?"
            ]),

            ("you'?re (.+)", [
                "Why do you say that I'm {x}?",
                "Do you think there's more to it than me being {x}?",
                "Could this be about your feelings rather than mine?"
            ]),

            ("i don'?t (.+)", [
                "Why don't you {x}?",
                "What would happen if you tried to {x}?",
                "Is it possible you're holding yourself back from {x}?"
            ]),

            ("i feel (.+)", [
                "It's okay to feel {x}. Can we explore what's behind this emotion?",
                "When you feel {x}, what do you usually do?",
                "How does feeling {x} affect your perspective?"
            ]),

            ("i have (.+)", [
                "Why do you think having {x} is significant?",
                "What does having {x} mean to you?",
                "How do you feel about having {x}?"
            ]),

            ("i would (.+)", [
                "What makes you feel you would {x}?",
                "How do you think others would react if you {x}?",
                "Why is {x} important to you?"
            ]),

            ("is there ([^?]+)", [
                "Why do you think there is {x}?",
                "What would it mean if there was {x}?",
                "Do you want there to be {x}?"
            ]),

            ("my (.+)", [
                "What about your {x} feels important right now?",
                "How does your {x} affect how you feel?",
                "What makes your {x} significant in this situation?"
            ]),

            ("you (.+)", [
                "Let's focus on your feelings about this. Why do you think this matters?",
                "What makes you say that about me?",
                "Could this be reflecting something you're experiencing yourself?"
            ]),

            ("why ([^?]+)", [
                "Why do you feel {x} is significant?",
                "What do you hope to understand by asking about {x}?",
                "Do you think {x} is connected to how you're feeling right now?"
            ]),

            ("i want (.+)", [
                "What does having {x} mean to you?",
                "How would achieving {x} affect your current situation?",
                "What's stopping you from pursuing {x} right now?",
                "If you had {x}, what would be your first step forward?"
            ]),

            ("(.*) mother(.*)", [
                "Tell me more about your mother.",
                "What feelings come up when you think about your mother?",
                "Do you think your relationship with your mother affects your current emotions?",
                "How would you describe the kind of support you wish to receive from her?",
                "What's one positive memory of your mother that stands out?",
                "Good family relations are important."
            ]),

            ("(.*) father(.*)", [
                "Tell me more about your father.",
                "What emotions arise when you think about your father?",
                "Do you feel your relationship with your father influences your current behavior?",
                "What do you wish your father understood about you?",
                "Can you recall a moment with your father that made you feel supported?",
                "Do you have trouble showing affection with your family?"
            ]),

            ("(.*) child(.*)", [
                "What is your favorite childhood memory?",
                "What memories from your childhood do you feel still affect you today?",
                "How did your friendships as a child shape your relationships now?",
                "Do you think any childhood experiences relate to your current emotions?",
                "Did the other children sometimes tease you?",
                "How do you feel about the way you were treated as a child?"
            ]),

            ("(.*) lover(.*)", [
                "How would you describe your relationship with your lover?",
                "What do you feel your lover does well in your relationship?",
                "Are there specific things you wish your lover understood about you?",
                "How does your lover's behavior affect your emotions?",
                "What changes would you like to see in your relationship, and how can you start that conversation?"
            ]),

            ("(.*) boyfriend(.*)", [
                "How would you describe your relationship with your boyfriend?",
                "What do you feel your boyfriend does well in your relationship?",
                "Are there specific things you wish your boyfriend understood about you?",
                "How does your boyfriend's behavior affect your emotions?",
                "What changes would you like to see in your relationship, and how can you start that conversation?"
            ]),

            ("(.*) girlfriend(.*)", [
                "How would you describe your relationship with your girlfriend?",
                "What do you feel your girlfriend does well in your relationship?",
                "Are there specific things you wish your girlfriend understood about you?",
                "How does your girlfriend's behavior affect your emotions?",
                "What changes would you like to see in your relationship, and how can you start that conversation?"
            ]),

            ("(.*) husband(.*)", [
                "How would you describe your relationship with your husband?",
                "What do you feel your husband does well in your relationship?",
                "Are there specific things you wish your husband understood about you?",
                "How does your husband's behavior affect your emotions?",
                "What changes would you like to see in your relationship, and how can you start that conversation?"
            ]),

            ("(.*) wife(.*)", [
                "How would you describe your relationship with your wife?",
                "What do you feel your wife does well in your relationship?",
                "Are there specific things you wish your wife understood about you?",
                "How does your wife's behavior affect your emotions?",
                "What changes would you like to see in your relationship, and how can you start that conversation?"
            ]),

            ("(.*) friend(.*)", [
                "What do you value most in your friendships?",
                "How do your friends support you during challenging times?",
                "Is there a specific friend you feel closest to? Why?",
                "What qualities do you look for in a good friend?",
                "Have you ever felt misunderstood by a friend? How did you handle it?"
            ]),

            ("(.*) love(.*)", [
                "Do you think that person really loves you?",
                "The truth is that love is not given by one person, it is the result of two people loving each other.",
                "Actually there is no exact definition of this thing called love, and you don't have to worry about it.",
                "In a loving relationship, you can actually focus more on yourself."
            ])
        ]

    def greeting(self):
        greetings = [f"Hello I am {self.name}, your friendly emotional supporter.",
                    f"Hello I am {self.name}, ready to assist you with anything you need!",
                    f"Hello I am {self.name}, here to help you through your day."]
        
        print(random.choice(greetings))

    def farewell(self):
        self.conversation_is_active = False
        responses = ["Goodbye! Take care and have a wonderful day ahead!",
                    "It was great talking to you. See you next time!",
                    "Thank you for chatting with me. Until next time!"]           
        
        print(random.choice(responses))
        return "Your session with Mirra has now ended"

    # Check and simplify input string
    def process_input(self, user_input):
        # Check input is string
        if not isinstance(user_input, str):
            raise ValueError('Sorry, I can only understand text.')
        
        # Check input is less than 500 characters
        if len(user_input) > 500:
            raise ValueError('Too much information! Please only tell me one thing at a time.')

        # Remove non-ascii characters from string
        processed_input = re.sub(r'[^\x00-\x7f]',r'', user_input) 
        processed_input = processed_input.lower()
        return processed_input
    
    # Swap pronouns in extracted text, break when a substitution has been made
    def swap_pronoun(self, extract_str):        
        for regex, replacement_str in self.pronoun_pairings:
            extract_str, sub_n = re.subn(regex, replacement_str, extract_str)
            if sub_n > 0:
                break
        return extract_str     
    
    # Use regex to find a match, swap pronouns and replace text in response string
    def match_and_respond(self, input_str, regex, responses):
        re_match = re.match(regex, input_str)

        # If no match return None
        if re_match is None:
            return None
        # If no subgroups then just give a random response
        if len(re_match.groups()) < 1:
            response = random.choice(responses)
            return response
        # If there is a subgroup then replace {x} with extracted text 
        else:
            extracted_str = re_match.group(1)
            extracted_str = self.swap_pronoun(extracted_str)
            response = random.choice(responses)
            response = re.sub(r'{x}', extracted_str, response)
            return response 

    # Function that generates a response based on the processed input
    def generate_response(self, processed_input):
        hello_regex = r'\b(hello|hi|hey)\b'
        bye_regex = r'\b(bye|goodbye|end|exit|quit)\b'

        # Iterate over all regex's and reset responses in self.regex_and_response
        for regex, responses in self.regex_and_response:
            response = self.match_and_respond(processed_input, regex, responses)
            if response is not None:
                return response
            else:
                pass
        
        # If no matches in regex_and_response check for a greeting message
        if re.search(hello_regex, processed_input):
            responses = ['Hello',
                         'Nice to meet you',
                         'Did you have a good day?',
                         'Do you have any questions for me?',
                         'We have already introduced ourselves...']
            return random.choice(responses)
        
        # Then check for a farewell message
        elif re.search(bye_regex, processed_input):
            print(self.farewell())
            

        # If no matches have been made then give a default response
        else:
            return random.choice(self.default_responses)
            
    # Main response function, print out input message, receive a new input, process it and return a new response
    def respond(self, out_message = None):
        if isinstance(out_message, str): 
            print(out_message)

        received_input = self.receive_input()
        try:
            processed_input = self.process_input(received_input)
            response = self.generate_response(processed_input)
            return response
        except ValueError as e:
            return ValueError.message
    
if __name__ == "__main__":
    
    mirra = MIRRA()
    mirra.greeting()

    response = 'How can I help you today?'

    while mirra.conversation_is_active:
        response = mirra.respond(response)
