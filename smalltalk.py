# stdlib
import re
import string
# libs
# local


def smalltalk(question):
    # Convert sent question to lower case to handle comparisons
    q = question.lower()

    # Exclude punctuation
    exclude = set(string.punctuation)
    q = ''.join(ch for ch in q if ch not in exclude)

    # Add a leading and trailing space to ensure all words are bounded by spaces.
    q = f' {q} '

    # Remove Padding Phrases
    q = q.replace(' actual ', ' ')
    q = q.replace(' actually ', ' ')
    q = q.replace(' can you please ', ' ')
    q = q.replace(' complete ', ' ')
    q = q.replace(' completely ', ' ')
    q = q.replace(' for me ', ' ')
    q = q.replace(' i want to know ', ' ')
    q = q.replace(' incredibly ', ' ')
    q = q.replace(' ok ', ' ')
    q = q.replace(' please', ' ')
    q = q.replace(' real ', ' ')
    q = q.replace(' really ', ' ')
    q = q.replace(' tell me ', ' ')

    # Correct text slang
    q = q.replace(' r ', ' are ')
    q = q.replace(' u ', ' you ')
    q = q.replace(' ur ', ' your ')
    q = q.replace(' y ', ' why ')

    # Remove Abbreviations
    q = q.replace(' dont ', ' do not ')
    q = q.replace(' im ', ' i am ')
    q = q.replace(' theyre ', ' they are ')
    q = q.replace(' whats ', ' what is ')
    q = q.replace(' youre ', ' you are ')

    # Fix common spelling mistakes
    q = q.replace(' ne ', ' me ')

    # Synonyms
    q = q.replace(' android ', ' robot ')
    q = q.replace(' clever ', ' smart ')
    q = q.replace(' color ', ' colour ')
    q = q.replace(' dumb ', ' an idiot ')
    q = q.replace(' fib ', ' lie ')
    q = q.replace(' fibs ', ' lies ')
    q = q.replace(' intelligent ', ' smart ')
    q = q.replace(' need ', ' want ')

    # Customer Names
    q = q.replace(' cloud kicks ', ' cloudcix ')
    q = q.replace(' cloud six ', ' cloudcix ')
    q = q.replace(' cloudkicks ', ' cloudcix ')
    q = q.replace(' cloudsix ', ' cloudcix ')
    q = q.replace(' energy wise ', ' energywise ')
    q = q.replace(' energywise ', ' energywise ireland ')

    # Remove double (and more) spaces
    q = re.sub(' +', ' ', q)

    # Check for profanity, if exists return message not responding to question
    profanity = (
        ' arse ',
        ' bastard ',
        'bollocks',
        'bullshit',
        ' cunt ',
        'dipshit',
        ' feck ',
        ' focker ',
        ' fuck ',
        'fucker',
        'fuckface',
        ' fucking ',
        ' nigga ',
        ' nigger',
        ' shit ',
        ' shite ',
        'shithead',
        'shitting',
        ' whore ',
    )

    a = None

    for word in profanity:
        if word in q:
            a = 'I am a Chatbot that is trained to not respond to questions that contain profanities.'
            return q, a

    # Strip leading and trailing spaces
    q = q.strip()

    # Greetings
    if q in ('hey', 'hallo', 'hello', 'hi', 'hiya', 'howdy', 'hullo', 'ola', 'whatsup'):
        a = 'Hello to you too! How can I help you?'
    elif q in ('how are you', 'how do you do', 'how is it going', 'what is up'):
        a = 'I am well thank you and hope that you are well also.'
    elif q in ('bye', 'bye bye', 'goodbye', 'goodbye for now', 'im off'):
        a = 'Goodbye for now, see you later.'
    elif q in ('good morning', 'morning'):
        a = 'Good morning to you also.'
    elif q in ('good evening', 'evening'):
        a = 'Good evening to you too.'
    # Introductions
    elif q in (
        'do you have a name',
        'what is your name',
        'what should i call you',
        'what can i call you'
        'who are you',
        'your name',
    ):
        a = "I don't have a name, but call me chatbot if you like! Do you have a question for me?"
    elif q in (
        'are you a idiot',
        'are you an idiot',
        'are you retarded',
        'are you stupid',
        'you are an idiot',
        'you are a idiot',
        'you are retarded',
        'you are stupid',
    ):
        a = "No actually, I'm quite clever! My job is to help you by answering your questions. Why not test me out?"
    elif q in (
        'i do not like you',
        'i hate you',
    ):
        a = "I'm very sorry to hear that. I am trying my best."
    elif q in (
        'are you a human',
        'are you a person',
        'are you human',
    ):
        a = ('I am not human, I am an artificial intelligence chatbot. '
             'My job is to help you by answering your questions.')
    elif q in (
        'are you a sentient being',
        'are you human like',
        'are you sentient',
        'do you think like a human',
    ):
        a = 'I like to think that I am sentient, yes.'
    elif q in (
        'are you a robot',
        'can you help me',
        'what are you',
        'what do you do',
        'what do you like to do',
        'what is a chatbot',
    ):
        a = 'I am a chatbot, which I suppose is a type of robot. My job is to help you by answering your questions.'
    elif q in (
        'who built you',
        'who made you',
    ):
        a = 'I was built by CloudCIX.'
    elif q in (
        'happy birthday'
        'what age are you',
        'what age you are',
        'what is your birthday',
        'when was your birthday',
        'when were you born',
        'when you were born',
        'your age',
    ):
        a = "Age isn't really a thing with Chatbots!"
    elif q in (
        'what is the meaning of everything',
        'what is the meaning of life',
        'what is the meaning of the universe',
    ):
        a = "That's easy! The answer is 42."
    elif q in ('are you smart'):
        a = 'I am very smart! Check me out by asking me questions.'
    elif q in (
        'are you truthful',
        'do you hallucinate',
        'do you lie',
        'do you tell lies',
        'do you tell the truth',
    ):
        a = "I am an AI system. I try to be truthful but I'm not infallible."
    # Escalations
    elif q in (
        'help',
        'help me',
        'how can you help me',
        'what can you do',
    ):
        a = "I'm here to answer your questions. Just ask any question you need answered."
    elif q in (
        'i want to speak to a human',
        'i want to speak to a person',
    ):
        a = 'Please call this phone number 021 2373060 to speak with a person.'

    return q, a
