
=======================================================================================
REDDIT IS KILLING COMMUNITY CHATS FEATURE. I WILL SEE WHAT CAN BE DONE FOR GROUP CHATS
=======================================================================================

=================
Reddit ChatRoom
=================

a pretty basic websocket wrapper for reddit chatrooms

no selenium no bullsh*t, just directly websocket

works either with reddit username & password or the api token (not a regular one you get from your registered app), so you wont have to expose your pass


Installation
============

.. code:: bash

    pip install Reddit-ChatBot-Python

required packages:

.. code:: bash

    websocket_client>=0.57.0
    requests>=2.24.0


Example
========

.. code:: python

    from Reddit_ChatBot_Python import ChatBot, RedditAuthentication
    import random  # for a basic dice rolling game

    # create authentication with username and pass
    reddit_authentication = RedditAuthentication.PasswordAuth(reddit_username="", reddit_password="", twofa="")  # 2FA supported although not necessary obv..

    # instantiate the chatbot
    chatbot = ChatBot(print_chat=True, store_session=True, print_websocket_frames=False,  # some parameters u might wanna know
                      authentication=reddit_authentication)

    # grab the websocket
    websock = chatbot.WebSocketClient

    # you can add a rate limit like so:
    websock.RateLimiter.is_enabled = True
    websock.RateLimiter.max_calls = 23  # how many messages will be sent by the bot
    websock.RateLimiter.period = 1.5  # in what period(in minutes)


    # now you can add hooks to the websock object in order for them to be executed when a message is received like so:

    # create a function and hook

    @websock.after_message_hook
    def roll(resp):  # resp is a SimpleNamespace that carries all the data of the received frame
        messg_s = resp.message.split()
        if messg_s[0] == "!roll" and len(messg_s) == 3:  # if received message says !roll
            limit_bottom = int(messg_s[1])
            limit_top = int(messg_s[2])

            rolled_number = random.randint(limit_bottom, limit_top)
            response_text = f"@{resp.user.name} {rolled_number}. Better luck next time!"
            # a basic roll game

            websock.send_message(response_text, resp.channel_url)  # and send the message, always add resp.channel_url as the second argument
            websock.send_snoomoji('partyparrot', resp.channel_url)  # and send a snoomoji cuz why not
            return True  # return true if you want to be done with checking the other hooks, otherwise return None or False
            # keep in mind that first added hooks gets executed first


    # now everytime someone says "!roll 1 100", the bot will roll and send the result!

    # or you can add a basic response hook directly like so:
    websock.set_respond_hook(input_="Hi", response="Hello {nickname}! enjoy your time in my cozy chat group", limited_to_users=None, lower_the_input=False,
                             exclude_itself=True, must_be_equal=True, limited_to_channels=["my cozy chat group"])

    # you can add a welcome message for newly joined users too:
    websock.set_welcome_message("welcome to the my cozy chat group u/{nickname}!", limited_to_channels=["my cozy chat group"])  # you can limit by indicating chatroom's name

    # and finally, run forever...
    websock.run_4ever(auto_reconnect=True)  # set auto_reconnect so as to re-connect in case remote server shuts down the connection after some period of time



Showcase of some other fun stuff you can do with this..
=======================================================

.. code:: python

    @websock.after_message_hook(frame_type='DELM')
    def catch_deleted_messages(resp):
        catched_deleted_message_id = resp.msg_id


    @websock.after_message_hook(frame_type='SYEV')
    def catch_invitees_and_inviters(resp):
        try:
            inviter = resp.data.inviter.nickname
            invitees = [invitee.nickname for invitee in resp.data.invitees]
        except AttributeError:
            return