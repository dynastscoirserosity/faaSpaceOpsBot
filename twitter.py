import pytz
import tweepy
#import config
from datetime import datetime
from itertools import islice

def run():
    client = tweepy.Client(
        consumer_key= 'your key goes here',
        consumer_secret = 'your key goes here',
        access_token = 'your key goes here',
        access_token_secret = 'your key goes here'
    )
    
    # read details of the file containing today's extract
    with open('scratchiest.txt', 'r') as file:
        file.seek(0)
        total_characters = len(file.read())  # count total characters
        file.seek(0)
        total_lines = len(file.readlines())  # count total lines

    tweet_text = ''
    header = str('\U0001F4C5 Updated ' + datetime.now(pytz.timezone('US/Eastern')).strftime('%d %b %Y (%Y/%m/%d) %H:%M %Z') + '\n')

    # if there are less than x characters
    likely_empty_limit = 10
    character_limit = 220
    if total_characters < likely_empty_limit:
        tweet_text = header + 'The operations plan does not currently include any advisories for space operations.'
        client.create_tweet(text = tweet_text)

    elif likely_empty_limit <= total_characters <= character_limit:
        with open('scratchiest.txt', 'r') as file:
            with open('scratchiest.txt', 'r') as file:
                tweet_text = header + '\n' + file.read()
                client.create_tweet(text = tweet_text)

    elif total_characters > character_limit:
        with open('scratchiest.txt', 'r') as file:
            read_total_lines = file.readlines()
            max_lines = len(read_total_lines) # find how many lines the section of interest takes up
            blank_lines_array = [0] # create an array with the first line
            # append blank lines to array
            l_no = 0
            for x in read_total_lines:
                if x.strip() == '':
                    blank_lines_array.append(int(l_no+1))
                l_no += 1
            # append the last line to array
            blank_lines_array.append(int(max_lines))

            # find number of sections
            current_section = 1
            number_of_sections = 1 # len(blank_lines_array) - 1
            s = 0
            e = 1

            # for each section, repeat until max sections
            while current_section <= number_of_sections:
                file.seek(0)
                section = islice(file, blank_lines_array[s], blank_lines_array[e]) # extract this section
                # write section to buffer
                buffer = ''
                for x in section:
                    buffer = buffer + str(x)
                tweet_text = header + '\n' + buffer

                if len(tweet_text) < 220:
                    client.create_tweet(text = tweet_text)

                elif len(tweet_text) >= 220:
                    character = 240
                    while tweet_text[character] != 'Z':
                        character -= 1

                    character_printer = 0
                    tweet_text_sub1 = str('')
                    while 0 <= character_printer <= character:
                        tweet_text_sub1 = tweet_text_sub1 + tweet_text[character_printer]
                        character_printer += 1
                    response = client.create_tweet(text = tweet_text_sub1)
                    response_1 = response[0]
                    tweet_id = response_1['id']

                    character_printer = character + 1
                    tweet_text_sub2 = str('')
                    while character <= character_printer <= len(tweet_text) - 1:
                        tweet_text_sub2 = tweet_text_sub2 + tweet_text[character_printer]
                        character_printer += 1
                    tweet_text_sub2 = '== BACKUP(S) ==' + tweet_text_sub2
                    client.create_tweet(text = tweet_text_sub2, in_reply_to_tweet_id = tweet_id)

                # increase array start value, array end value, and session number by 1
                s += 1
                e += 1
                
                current_section += 1
