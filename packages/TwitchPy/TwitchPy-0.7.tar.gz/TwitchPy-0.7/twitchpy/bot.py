from twitchpy.client import Client
import ssl
import socket
from twitchpy.message import Message
from twitchpy.channel import Channel

class Bot:
    """
    Represents a bot
    """

    def __init__(self,oauth_token,client_id,client_secret,username,channels,command_prefix,ready_message=""):
        """
        Args:
            oauth_token (str): OAuth token to identify the application
            client_id (str): Client ID to identify the application
            client_secret (str): Client secret to identify the application
            username (str): Name of the bot
            channels (list[str]): Names of channels the bot will access
            command_prefix (str): Prefix of the commands the bot will recognize
            ready_message (str): Message that the bot will send through the chats of the channels it access
        """

        self.__irc_server="irc.chat.twitch.tv"
        self.__irc_port=6697
        self.__client=Client(oauth_token,client_id,client_secret)
        self.__oauth_token=oauth_token
        self.username=username

        self.channels=[]

        for channel in channels:
            self.channels.append(channel.replace("@","").lower())

        self.command_prefix=command_prefix
        self.ready_message=ready_message
        self.custom_checks={}
        self.custom_listeners={}
        self.listeners_to_remove=[]
        self.custom_commands={}
        self.commands_to_remove=[]
        self.custom_methods_after_commands={}
        self.methods_after_commands_to_remove=[]
        self.custom_methods_before_commands={}
        self.methods_before_commands_to_remove=[]

    def __send_privmsg(self,channel,text):
        self.__send_command(f"PRIVMSG #{channel} :{text}")

    def __send_command(self,command):
        if "PASS" not in command:
            print(f"< {command}")

        self.irc.send((command+"\r\n").encode())

    def run(self):
        """
        Runs the bot
        """

        self.irc=ssl.wrap_socket(socket.socket())
        self.irc.connect((self.__irc_server,self.__irc_port))
        
        self.__send_command(f"PASS {self.__oauth_token}")
        self.__send_command(f"NICK {self.username}")

        for channel in self.channels:
            self.__send_command(f"JOIN #{channel}")
            self.__send_privmsg(channel,self.ready_message)

        for check in self.custom_checks.values():
            if check()!=True:
                return

        self.__loop()

    def __get_user_from_prefix(self,prefix):
        domain=prefix.split("!")[0]

        if domain.endswith(".tmi.twitch.tv"):
            return domain.replace(".tmi.twitch.tv","")

        if "tmi.twitch.tv" not in domain:
            return domain

        return None

    def __remove_prefix(self,string,prefix):
        if not string.startswith(prefix):
            return string

        return string[len(prefix):]

    def __parse_message(self,received_msg):
        parts=received_msg.split(" ")

        prefix=None
        user=None
        channel=None
        irc_command=None
        irc_args=None
        text=None
        text_command=None
        text_args=None

        if parts[0].startswith(":"):
            prefix=self.__remove_prefix(parts[0],":")
            user=self.__get_user_from_prefix(prefix)
            parts=parts[1:]

        text_start=next(
            (idx for idx,part in enumerate(parts) if part.startswith(":")),
            None
        )

        if text_start is not None:
            text_parts=parts[text_start:]
            text_parts[0]=text_parts[0][1:]
            text=" ".join(text_parts)

            if text_parts[0].startswith(self.command_prefix):
                text_command=self.__remove_prefix(text_parts[0],self.command_prefix)
                text_args=text_parts[1:]

            parts=parts[:text_start]

        irc_command=parts[0]
        irc_args=parts[1:]

        hash_start=next(
            (idx for idx,part in enumerate(irc_args) if part.startswith("#")),
            None
        )

        if hash_start is not None:
            channel=irc_args[hash_start][1:]

        message=Message(prefix=prefix,user=user,channel=channel,irc_command=irc_command,irc_args=irc_args,text=text,text_command=text_command,text_args=text_args)

        return message

    def __handle_message(self,received_msg):
        if len(received_msg)==0:
            return

        message=self.__parse_message(received_msg)
        print(f"[{message.channel}] {message.user}: {message.text}")

        if message.irc_command=="PING":
            self.__send_command("PONG :tmi.twitch.tv")

        for listener in self.custom_listeners.values():
            listener(message)

        for listener in self.listeners_to_remove:
            if listener in self.custom_listeners.keys():
                self.custom_listeners.pop(listener)

        self.listeners_to_remove=[]

        if message.irc_command=="PRIVMSG":
            if message.text_command in self.custom_commands:
                for before in self.custom_methods_before_commands.values():
                    before(message)

                for method in self.methods_before_commands_to_remove:
                    if method in self.custom_methods_before_commands.keys():
                        self.custom_methods_before_commands.pop(method)

                self.custom_commands[message.text_command](message)

                for after in self.custom_methods_after_commands.values():
                    after(message)

                for method in self.methods_after_commands_to_remove:
                    if method in self.custom_methods_after_commands.keys():
                        self.custom_methods_after_commands.pop(method)

    def __loop(self):
        while True:
            received_msgs=self.irc.recv(2048).decode()

            for received_msg in received_msgs.split("\r\n"):
                self.__handle_message(received_msg)

            for command in self.commands_to_remove:
                if command in self.custom_commands.keys():
                    self.custom_commands.pop(command)

    def add_check(self,name,check):
        """
        Adds a check to the bot

        Args:
            name (str): Check's name
            check (func): Method that will act as a check
        """

        self.custom_checks[name]=check

    def add_listener(self,name,listener):
        """
        Adds a command to the bot

        Args:
            name (str): Command's name
            listener (str): Method that will be executed when the command is invoked
        """

        self.custom_listeners[name]=listener

    def add_command(self,name,command):
        """
        Adds a command to the bot

        Args:
            name (str): Command's name
            command (func): Method that will be executed when the command is invoked
        """

        self.custom_commands[name]=command

    def start_commercial(self,broadcaster_id,length):
        """
        Starts a commercial on a specified channel

        Args:
            broadcaster_id (int): ID of the channel requesting a commercial
            length (int): Desired length of the commercial in seconds
                          Valid options are 30, 60, 90, 120, 150 and 180

        Returns:
            list
        """

        return self.__client.start_commercial(broadcaster_id,length)

    def get_extension_analytics(self,extension_id="",first=20,type=""):
        """
        Gets a URL that extension developers can use to download analytics reports for their extensions
        The URL is valid for 5 minutes

        Args:
            extension_id (str, optional): Client ID value assigned to the extension when it is created
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
            type (str, optional): Type of analytics report that is returned
                                  Valid values: "overview_v1" and "overview_v2"

        Returns:
            list
        """

        return self.__client.get_extension_analytics(extension_id,first,type)

    def get_game_analytics(self,first=20,game_id="",type=""):
        """
        Gets a URL that game developers can use to download analytics reports for their games
        The URL is valid for 5 minutes

        Args:
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
            game_id (str, optional): Game ID
            type (str, optional): Type of analytics report that is returned
                                  Valid values: "overview_v1" and "overview_v2"

        Returns:
            list
        """

        return self.__client.get_game_analytics(first,game_id,type)

    def get_bits_leaderboard(self,count=10,user_id=""):
        """
        Gets a ranked list of Bits leaderboard information for a broadcaster

        Args:
            count (int, optional): Number of results to be returned
                                   Maximum: 100
                                   Default: 10
            user_id (str, optional): ID of the user whose results are returned

        Returns:
            list
        """

        return self.__client.get_bits_leaderboard(count,user_id)

    def get_cheermotes(self,broadcaster_id=""):
        """
        Retrieves the list of available Cheermotes
        Cheermotes returned are available throughout Twitch, in all Bits-enabled channels

        Args:
            broadcaster_id (str, optional): ID for the broadcaster who might own specialized Cheermotes

        Returns:
            list
        """

        return self.__client.get_cheermotes(broadcaster_id)

    def get_extension_transactions(self,extension_id,id="",first=20):
        """
        Allows extension back end servers to fetch a list of transactions that have occurred for their extension across all of Twitch

        Args:
            extension_id (str): ID of the extension to list transactions for
            id (str, optional): Transaction IDs to look up
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_extension_transactions(extension_id,id,first)

    def create_custom_reward(self,broadcaster_id,title,cost,prompt="",is_enabled=True,background_color="",is_user_input_required=False,is_max_per_stream_enabled=False,max_per_stream=None,is_max_per_user_per_stream_enabled=False,max_per_user_per_stream=None,is_global_cooldown_enabled=False,global_cooldown_seconds=None,should_redemptions_skip_request_queue=False):
        """
        Creates a Custom Reward on a channel

        Args:
            broadcaster_id (str): ID of the channel creating a reward
            title (str): The title of the reward
            cost (int): The cost of the reward
            prompt (str, optional): The prompt for the viewer when they are redeeming the reward
            is_enabled (bool, optional): Is the reward currently enabled, if false the reward won’t show up to viewers
                                         Defaults true
            background_color (str, optional): Custom background color for the reward
                                              Format: Hex with # prefix
            is_user_input_required (bool, optional): Does the user need to enter information when redeeming the reward
                                                     Defaults false
            is_max_per_stream_enabled (bool, optional): Whether a maximum per stream is enabled
                                                        Defaults to false
            max_per_stream (int, optional): The maximum number per stream if enabled
            is_max_per_user_per_stream_enabled (bool, optional): Whether a maximum per user per stream is enabled
                                                                 Defaults to false
            max_per_user_per_stream (int, optional): The maximum number per user per stream if enabled
            is_global_cooldown_enabled (bool, optional): Whether a cooldown is enabled
                                                         Defaults to false
            global_cooldown_seconds (int, optional): The cooldown in seconds if enabled
            should_redemptions_skip_request_queue (bool, optional): Should redemptions be set to FULFILLED status immediately when redeemed and skip the request queue instead of the normal UNFULFILLED status
                                                                    Defaults false

        Returns:
            list
        """

        return self.__client.create_custom_reward(broadcaster_id,title,cost,prompt,is_enabled,background_color,is_user_input_required,is_max_per_stream_enabled,max_per_stream,is_max_per_user_per_stream_enabled,max_per_user_per_stream,is_global_cooldown_enabled,global_cooldown_seconds,should_redemptions_skip_request_queue)

    def delete_custom_reward(self,broadcaster_id,id):
        """
        Deletes a Custom Reward on a channel
        Any UNFULFILLED Custom Reward Redemptions of the deleted Custom Reward will be updated to the FULFILLED status

        Args:
            broadcaster_id (str): ID of the channel deleting a reward
            id (str): ID of the Custom Reward to delete
        """

        self.__client.delete_custom_reward(broadcaster_id,id)

    def get_custom_reward(self,broadcaster_id,id="",only_manageable_rewards=False):
        """
        Returns a list of Custom Reward objects for the Custom Rewards on a channel

        Args:
            broadcaster_id (str): ID of the channel deleting a reward
            id (str, optional): This parameter filters the results and only returns reward objects for the Custom Rewards with matching ID
            only_manageable_rewards (bool, optional): When set to true, only returns custom rewards that the calling broadcaster can manage
                                                      Defaults false.

        Returns:
            list
        """

        return self.__client.get_custom_reward(broadcaster_id,id,only_manageable_rewards)

    def get_custom_reward_redemption(self,broadcaster_id,reward_id,id="",status="",sort="OLDEST",first=20):
        """
        Returns Custom Reward Redemption objects for a Custom Reward on a channel
        You may specify only one of the args

        Args:
            broadcaster_id (str): ID of the channel owner of a reward
            reward_id (str): This parameter returns paginated Custom Reward Redemption objects for redemptions of the Custom Reward
            id (str, optional): This param filters the results and only returns Custom Reward Redemption objects for the redemptions with matching ID
            status (str, optional): This param filters the paginated Custom Reward Redemption objects for redemptions with the matching status
                                    Can be one of UNFULFILLED, FULFILLED or CANCELED
            sort (str, optional): Sort order of redemptions returned when getting the paginated Custom Reward Redemption objects for a reward
                                  One of: OLDEST, NEWEST
                                  Default: OLDEST
            first (int, optional): Number of results to be returned when getting the paginated Custom Reward Redemption objects for a reward
                                   Limit: 50
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_custom_reward_redemption(broadcaster_id,reward_id,id,status,sort,first)

    def update_custom_reward(self,broadcaster_id,id,title="",prompt="",cost=None,background_color="",is_enabled=None,is_user_input_required=None,is_max_per_stream_enabled=None,max_per_stream=None,is_max_per_user_per_stream_enabled=False,max_per_user_per_stream=None,is_global_cooldown_enabled=False,global_cooldown_seconds=None,is_paused=None,should_redemptions_skip_request_queue=None):
        """
        Updates a Custom Reward created on a channel

        Args:
            broadcaster_id (str): ID of the channel updating a reward
            id (str): ID of the Custom Reward to update
            title (str, optional): The title of the reward
            prompt (str, optional): The prompt for the viewer when they are redeeming the reward
            cost (int, optional): The cost of the reward
            background_color (str, optional): Custom background color for the reward
                                              Format: Hex with # prefix
            is_enabled (bool, optional): Is the reward currently enabled
            is_user_input_required (bool, optional): Does the user need to enter information when redeeming the reward
            is_max_per_stream_enabled (bool, optional): Whether a maximum per stream is enabled
            max_per_stream (int, optional): The maximum number per stream if enabled
            is_max_per_user_per_stream_enabled (bool, optional): Whether a maximum per user per stream is enabled
                                                                 Defaults to false
            max_per_user_per_stream (int, optional): The maximum number per user per stream if enabled
            is_global_cooldown_enabled (bool, optional): Whether a cooldown is enabled
                                                         Defaults to false
            global_cooldown_seconds (int, optional): The cooldown in seconds if enabled
            is_paused (bool, optional): Is the reward currently paused
            should_redemptions_skip_request_queue (bool, optional): Should redemptions be set to FULFILLED status immediately when redeemed and skip the request queue instead of the normal UNFULFILLED status

        Returns:
            list
        """

        return self.__client.update_custom_reward(broadcaster_id,id,title,prompt,cost,background_color,is_enabled,is_user_input_required,is_max_per_stream_enabled,max_per_stream,is_max_per_user_per_stream_enabled,max_per_user_per_stream,is_global_cooldown_enabled,global_cooldown_seconds,is_paused,should_redemptions_skip_request_queue)

    def update_redemption_status(self,id,broadcaster_id,reward_id,status=""):
        """
        Updates the status of Custom Reward Redemption objects on a channel that are in the UNFULFILLED status

        Args:
            id (str): ID of the Custom Reward Redemption to update
            broadcaster_id (str): ID of the channel updating a reward redemption
            reward_id (str): ID of the Custom Reward the redemptions to be updated are for
            status (str, optional): The new status to set redemptions to
                                    Can be either FULFILLED or CANCELED

        Returns:
            list
        """

        return self.__client.update_redemption_status(id,broadcaster_id,reward_id,status)

    def create_clip(self,broadcaster_id,has_delay=False):
        """
        This returns both an ID and an edit URL for a new clip.

        Args:
            broadcaster_id (str): ID of the stream from which the clip will be made
            has_delay (bool, optional): If false, the clip is captured from the live stream when the API is called; otherwise, a delay is added before the clip is captured (to account for the brief delay between the broadcaster’s stream and the viewer’s experience of that stream)
                                        Default: false.

        Returns:
            dict
        """

        return self.__client.create_clip(broadcaster_id,has_delay)

    def get_clips(self,broadcaster_id="",game_id="",id="",first=20):
        """
        Gets clip information by clip ID, broadcaster ID or game ID

        Args:
            broadcaster_id (str, optional): ID of the broadcaster for whom clips are returned
            game_id (str, optional): ID of the game for which clips are returned
            id (str, optional): ID of the clip being queried
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_clips(broadcaster_id,game_id,id,first)

    def create_entitlement_grants_upload_url(self,manifest_id,type):
        """
        Creates a URL where you can upload a manifest file and notify users that they have an entitlement

        Args:
            manifest_id (string): Unique identifier of the manifest file to be uploaded
                                  Must be 1-64 characters
            type (string): Type of entitlement being granted
                           Only bulk_drops_grant is supported

        Returns:
            str
        """

        return self.__client.create_entitlement_grants_upload_url(manifest_id,type)

    def get_code_status(self,code,user_id):
        """
        Gets the status of one or more provided codes

        Args:
            code (str): The code to get the status of
            user_id (int): ID of the user which is going to receive the entitlement associated with the code

        Returns:
            list
        """

        return self.__client.get_code_status(code,user_id)

    def get_drops_entitlements(self,id="",user_id="",game_id="",first=20):
        """
        Gets a list of entitlements for a given organization that have been granted to a game, user, or both

        Args:
            id (str, optional): ID of the entitlement
            user_id (str, optional): A Twitch User ID
            game_id (str, optional): A Twitch Game ID
            first (int, optional): Maximum number of entitlements to return
                                   Default: 20
                                   Max: 100

        Returns:
            list
        """

        return self.__client.get_drops_entitlements(id,user_id,game_id,first)

    def redeem_code(self,code,user_id):
        """
        Redeems one or more provided codes

        Args:
            code (str): The code to redeem
            user_id (int): ID of the user which is going to receive the entitlement

        Returns:
            list
        """

        return self.__client.redeem_code(code,user_id)

    def get_top_games(self,first=20):
        """
        Gets the most popular games

        Args:
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_top_games(first)

    def get_game(self,id="",name=""):
        """
        Gets games by game ID or name
        For a query to be valid, name and/or id must be specified

        Args:
            id (str, optional): Game ID
            name (str, optional): Game name
                                  The name must be an exact match

        Returns:
            Game
        """

        return self.__client.get_game(id,name)

    def get_hype_train_events(self,broadcaster_id,first=1,id=""):
        """
        Gets the information of the most recent Hype Train of the given channel ID

        Args:
            broadcaster_id (str): User ID of the broadcaster
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 1
            id (str, optional): The id of the wanted event

        Returns:
            list
        """

        return self.__client.get_hype_train_events(broadcaster_id,first,id)

    def check_automod_status(self,broadcaster_id,msg_id="",msg_user="",user_id=""):
        """
        Determines whether a string message meets the channel’s AutoMod requirements

        Args:
            broadcaster_id (str): User ID of the broadcaster
            msg_id (str, optional): Developer-generated identifier for mapping messages to results
            msg_user (str, optional): Message text
            user_id (str, optional): User ID of the sender

        Returns:
            list
        """

        return self.__client.check_automod_status(broadcaster_id,msg_id,msg_user,user_id)

    def get_banned_events(self,broadcaster_id,user_id="",first=20):
        """
        Returns all user bans and un-bans in a channel

        Args:
            broadcaster_id (str): User ID of the broadcaster
            user_id (str, optional): Filters the results and only returns a status object for ban events that include users being banned or un-banned in the channel
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_banned_events(broadcaster_id,user_id,first)

    def get_banned_users(self,broadcaster_id,user_id="",first=20):
        """
        Returns all banned and timed-out users in a channel

        Args:
            broadcaster_id (str): User ID of the broadcaster
            user_id (str, optional): Filters the results and only returns a status object for users who are banned in the channel
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_banned_users(broadcaster_id,user_id,first)

    def get_moderators(self,broadcaster_id,user_id="",first=20):
        """
        Returns all moderators in a channel

        Args:
            broadcaster_id (str): User ID of the broadcaster
            user_id (str, optional): Filters the results and only returns a status object for users who are moderators in this channel
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_moderators(broadcaster_id,user_id,first)

    def get_moderator_events(self,broadcaster_id,user_id="",first=20):
        """
        Returns a list of moderators or users added and removed as moderators from a channel

        Args:
            broadcaster_id (str): User ID of the broadcaster
            user_id (str, optional): Filters the results and only returns a status object for users who have been added or removed as moderators in the channel
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_moderator_events(broadcaster_id,user_id,first)

    def search_categories(self,query,first=20):
        """
        Returns a list of games or categories that match the query via name either entirely or partially

        Args:
            query (str): url encoded search query
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.search_categories(query,first)

    def search_channels(self,query,first=20,live_only=False):
        """
        Returns a list of channels that match the query via channel name or description either entirely or partially

        Args:
            query (str): url encoded search query
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20
            live_only (bool, optional): Filter results for live streams only
                                        Default: false

        Returns:
            list
        """

        return self.__client.search_channels(query,first,live_only)

    def get_stream_key(self,broadcaster_id):
        """
        Gets the channel stream key for a user

        Args:
            broadcaster_id (str): User ID of the broadcaster

        Returns:
            str
        """

        return self.__client.get_stream_key(broadcaster_id)

    def get_streams(self,first=20,game_id="",language="",user_id="",user_login=""):
        """
        Gets active streams

        Args:
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20
            game_id (str, optional): Returns streams broadcasting a specified game ID
            language (str, optional): Stream language
            user_id (str, optional): Returns streams broadcast by one or more specified user IDs
            user_login (str, optional): Returns streams broadcast by one or more specified user login names

        Returns:
            list
        """

        return self.__client.get_streams(first,game_id,language,user_id,user_login)

    def create_stream_marker(self,user_id,description=""):
        """
        Creates a marker in the stream of a user specified by user ID

        Args:
            user_id (str): ID of the broadcaster in whose live stream the marker is created
            description (str, optional): Description of or comments on the marker
                                         Max length is 140 characters

        Returns:
            list
        """

        return self.__client.create_stream_marker(user_id,description)

    def get_stream_markers(self,user_id,video_id,first=20):
        """
        Gets a list of markers for either a specified user’s most recent stream or a specified VOD/video (stream), ordered by recency
        Only one of user_id and video_id must be specified

        Args:
            user_id (str): ID of the broadcaster from whose stream markers are returned
            video_id (str): ID of the VOD/video whose stream markers are returned
            first (int, optional): Number of values to be returned when getting videos by user or game ID
                                   Limit: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_stream_markers(user_id,video_id,first)

    def get_channel(self,broadcaster_id):
        """
        Gets a channel

        Args:
            broadcaster_id (str): ID of the channel to be updated

        Returns:
            Channel
        """

        return self.__client.get_channel(broadcaster_id)

    def modify_channel_information(self,broadcaster_id,game_id,broadcaster_language,title):
        """
        Modifies channel information
        game_id, broadcaster_language and title parameters are optional, but at least one parameter must be provided

        Args:
            broadcaster_id (str): ID of the channel to be updated
            game_id (str): The current game ID being played on the channel
            broadcaster_language (str): The language of the channel
            title (str): The title of the stream
        """

        self.__client.modify_channel_information(broadcaster_id,game_id,broadcaster_language,title)

    def get_broadcaster_subscriptions(self,broadcaster_id,user_id="",first=20):
        """
        Get all of a broadcaster’s subscriptions

        Args:
            broadcaster_id (str): User ID of the broadcaster
            user_id (str, optional): ID of account to get subscription status of
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_broadcaster_subscriptions(broadcaster_id,user_id,first)

    def get_all_stream_tags(self,first=20,tag_id=""):
        """
        Gets the list of all stream tags defined by Twitch

        Args:
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20
            tag_id (str, optional): ID of a tag

        Returns:
            list
        """

        return self.__client.get_all_stream_tags(first,tag_id)

    def get_stream_tags(self,broadcaster_id):
        """
        Gets the list of tags for a specified stream (channel)

        Args:
            broadcaster_id (str): ID of the stream thats tags are going to be fetched

        Returns:
            list
        """

        return self.__client.get_stream_tags(broadcaster_id)

    def replace_stream_tags(self,broadcaster_id,tag_ids=[]):
        """
        Applies specified tags to a specified stream (channel), overwriting any existing tags applied to that stream
        If no tag ids are provided, all tags are removed from the stream

        Args:
            broadcaster_id (str): ID of the stream for which tags are to be replaced
            tag_ids (list, optional): IDs of tags to be applied to the stream
                                      Maximum of 100 supported
        """

        self.__client.replace_stream_tags(broadcaster_id,tag_ids)

    def create_user_follows(self,from_id,to_id,allow_notifications=False):
        """
        Adds a specified user to the followers of a specified channel

        Args:
            from_id (str): User ID of the follower
            to_id (str): ID of the channel to be followed by the user
            allow_notifications (bool, optional): If true, the user gets email or push notifications (depending on the user’s notification settings) when the channel goes live
                                                  Default value is false
        """

        self.__client.create_user_follows(from_id,to_id,allow_notifications)

    def delete_user_follows(self,from_id,to_id):
        """
        Deletes a specified user from the followers of a specified channel

        Args:
            from_id (str): User ID of the follower
            to_id (str): Channel to be unfollowed by the user
        """

        self.__client.delete_user_follows(from_id,to_id)

    def get_user(self,id="",login=""):
        """
        Gets an user

        Args:
            id (str, optional): User ID
            login (str, optional): User login name

        Returns:
            User
        """

        return self.__client.get_user(id,login)

    def get_user_follows(self,first=20,from_id="",to_id=""):
        """
        Gets information on follow relationships between Twitch users
        At minimum, from_id or to_id must be provided for a query to be valid

        Args:
            first (int, optional): Maximum number of objects to return
                                   Maximum: 100
                                   Default: 20
            from_id (str, optional): User ID
            to_id (str, optional): User ID

        Returns:
            list
        """

        return self.__client.get_user_follows(first,from_id,to_id)

    def update_user(self,description=""):
        """
        Updates the description of a user

        Args:
            description (str, optional): User’s account description

        Returns:
            User
        """

        return self.__client.update_user(description)

    def get_user_extensions(self):
        """
        Gets a list of all extensions (both active and inactive) for a specified user

        Returns:
            list
        """

        return self.__client.get_user_extensions()

    def get_user_active_extensions(self,user_id=""):
        """
        Gets information about active extensions installed by a specified user

        Args:
            user_id (str, optional): ID of the user whose installed extensions will be returned

        Returns:
            list
        """

        return self.__client.get_user_active_extensions(user_id)

    def update_user_extensions(self):
        """
        Updates the activation state, extension ID, and/or version number of installed extensions for a specified user

        Returns:
            list
        """

        return self.__client.update_user_extensions()

    def get_videos(self,id,user_id,game_id,first=20,language="",period="all",sort="time",type="all"):
        """
        Gets video information by video ID, user ID, or game ID
        Each request must specify one video id, one user_id, or one game_id

        Args:
            id (str): ID of the video
            user_id (str): ID of the user who owns the video
            game_id (str): ID of the game the video is of
            first (int, optional): Number of values to be returned
                                   Limit: 100
                                   Default: 20
            language (str, optional): Language of the video
            period (str, optional): Period during which the video was created
                                    Valid values: "all", "day", "week", "month"
            sort (str, optional): Sort order of the videos
                                  Valid values: "time", "trending", "views"
                                  Default: "time"
            type (str, optional): Type of video
                                  Valid values: "all", "upload", "archive", "highlight"
                                  Default: "all"

        Returns:
            list
        """

        return self.__client.get_videos(id,user_id,game_id,first,language,period,sort,type)

    def get_webhook_subscriptions(self,first=20):
        """
        Gets the Webhook subscriptions of a user

        Args:
            first (int, optional): Number of values to be returned per page
                                   Limit: 100
                                   Default: 20

        Returns:
            list
        """

        return self.__client.get_webhook_subscriptions(first)

    def get_chatters(self,username):
        """
        Gets the users into a channel chat

        Args:
            username (str): Channel's name

        Returns:
            dict
        """
        
        return self.__client.get_chatters(username)

    def ban(self,channel,user,reason=""):
        """
        Bans a user

        Args:
            channel (str): Channel who bans
            username (str): User to ban
            reason (str, optional): Reason of the ban
        """

        self.__send_privmsg(channel,f"/ban @{user} {reason}")

    def block(self,channel,user):
        """
        Blocks a user

        Args:
            channel (str): Channel who blocks
            username (str): User to block
        """

        self.__send_privmsg(channel,f"/block @{user}")

    def clear(self,channel):
        """
        Clears the chat

        Args:
            channel (str): Channel to clean the chat
        """

        self.__send_privmsg(channel,"/clear")

    def color(self,channel,color):
        """
        Changes the color of the channel's name in the chat

        Args:
            channel (str): Channel to change color
            color (str): New color's name
        """

        self.__send_privmsg(channel,f"/color {color}")

    def commercial(self,channel,duration=30):
        """
        Places advertising in the channel

        Args:
            channel (str): Channel on which start the commercial
            duration (int): Duration of advertising
        """

        self.__send_privmsg(channel,f"/commercial {duration}")

    def emoteonly(self,channel):
        """
        Activates the "emotes only" mode

        Args:
            channel (str): Channel on which activate the mode
        """

        self.__send_privmsg(channel,"/emoteonly")

    def emoteonly_off(self,channel):
        """
        Disables "emotes only" mode

        Args:
            channel (str): Channel on which disable the mode
        """

        self.__send_privmsg(self.name,"/emoteonlyoff")

    def followers(self,channel):
        """
        Activates the "followers only" mode

        Args:
            channel (str): Channel on which activate the mode
        """

        self.__send_privmsg(channel,"/followers")

    def followers_off(self,channel):
        """
        Disables the "followers only" mode

        Args:
            channel (str): Channel on which disable the mode
        """

        self.__send_privmsg(channel,"/followersoff")

    def host(self,channel,username):
        """
        Hosts a channel

        Args:
            channel (str): Name of the channel who hosts
            username (str): Name of the channel to host
        """

        self.__send_privmsg(channel,f"/host {username}")

    def marker(self,channel,description=""):
        """
        Leaves a mark on the channel's stream

        Args:
            channel (str): Channel in which leave the mark
            description (str): Mark's description
        """

        self.__send_privmsg(channel,f"/marker {description}")

    def mod(self,channel,username):
        """
        Makes a user mod

        Args:
            channel (str): Channel who promotes the user
            username (str): Name of the user to be promoted
        """

        self.__send_privmsg(channel,f"/mod {username}")

    def raid(self,channel,username):
        """
        Raids another channel

        Args:
            channel (str): Name of the channel who raids
            username (str): Name of the channel to raid
        """

        self.__send_privmsg(channel,f"/raid {username}")

    def send(self,channel,text):
        """
        Sends a message by chat

        Args:
            channel (str): Owner of the chat
            text (str): Message's text
        """

        self.__send_privmsg(channel,text)

    def send_me(self,channel,text):
        """
        Sends a message by chat with the color of the channel's name

        Args:
            channel (str): Owner of the chat
            text (str): Message's text
        """

        self.__send_privmsg(channel,f"/me {text}")

    def slow(self,channel,duration):
        """
        Activates the "slow" mode

        Args:
            channel (str): Channel on which activate the mode
            duration (int): Time between messages
        """

        self.__send_privmsg(channel,f"/slow {duration}")

    def slow_off(self,channel):
        """
        Disables the "slow" mode

        Args:
            channel (str): Channel on which disable the mode
        """

        self.__send_privmsg(channel,f"/slow_off")

    def subscribers(self,channel):
        """
        Activates the "subscribers only" mode

        Args:
            channel (str): Channel on which activate the mode
        """

        self.__send_privmsg(channel,"/subscribers")

    def subscribers_off(self,channel):
        """
        Disables "subscriber only" mode

        Args:
            channel (str): Channel on which disable the mode
        """

        self.__send_privmsg(channel,"/subscribersoff")

    def timeout(self,channel,user,duration=600,reason=""):
        """
        Expels a user temporarily

        Args:
            channel (str): Channel who ejects
            user (str): Name of the user to expel
            duration (int): Ejecting time
            reason (str): Reason for expulsion
        """

        self.__send_privmsg(channel,f"/timeout @{user} {duration} {reason}")

    def unban(self,channel,user):
        """
        Undoes the ban of a user

        Args:
            channel (str): Name of the channel who readmits
            user (str): Name of the user to readmit
        """

        self.__send_privmsg(channel,f"/unban @{user}")

    def unblock(self,channel,user):
        """
        Unblocks a user

        Args:
            channel (str): Name of the channel who unblocks
            user (str): Name of the user to unblock
        """

        self.__send_privmsg(channel,f"/unblock @{user}")

    def uniquechat(self,channel):
        """
        Activates the "unique" mode

        Args:
            channel (str): Channel on which activate the mode
        """

        self.__send_privmsg(channel,"/uniquechat")

    def uniquechat_off(self,channel):
        """
        Disables the "unique" mode

        Args:
            channel (str): Channel on which disable the mode
        """

        self.__send_privmsg(channel,"/uniquechatoff")

    def unhost(self,channel):
        """
        Unhosts the hosted channel

        Args:
            channel (str): Channel who unhosts
        """

        self.__send_privmsg(channel,f"/unhost")

    def unmod(self,channel,username):
        """
        Removes the moderator's rank from a user

        Args:
            channel (str): Channel who removes the moderator's rank
            username (str): User's name
        """

        self.__send_privmsg(channel,f"/unmod {username}")

    def unraid(self,channel):
        """
        Cancels an raid

        Args:
            channel (str): Channel who unraids
        """

        self.__send_privmsg(channel,f"/unraid")

    def unvip(self,channel,username):
        """
        Removes the vip range from a user

        Args:
            channel (str): Channel who remove's the vip range
            username (str): User's name
        """

        self.__send_privmsg(channel,f"/unvip {username}")

    def vip(self,channel,username):
        """
        Makes a user vip

        Args:
            channel (str): Channel who makes a user vip
            username (str): User's name
        """

        self.__send_privmsg(channel,f"/vip {username}")

    def whisper(self,channel,user,text):
        """
        Whispers to a user

        Args:
            channel (str): Channel on which send the whisp
            user (str): User's name
            text (str): Whisper's text
        """

        self.__send_privmsg(channel,f"/w {user} {text}")

    def add_method_after_commands(self,name,method):
        """
        Adds to the bot a method that will be executed after each command

        Args:
            name (str): Method's name
            method (func): Method to be executed after each command
        """

        self.custom_methods_after_commands[name]=method

    def add_method_before_commands(self,name,method):
        """
        Adds to the bot a method that will be executed before each command

        Args:
            name (str): Method's name
            method (func): Method to be executed before each command
        """

        self.custom_methods_before_commands[name]=method

    def remove_check(self,name):
        """
        Removes a check from the bot

        Args:
            name (str): Check's name
        """

        self.custom_checks.pop(name)

    def remove_listener(self,name):
        """
        Removes a listener from the bot

        Args:
            name (str): Listener's name
        """

        self.listeners_to_remove.append(name)

    def remove_command(self,name):
        """
        Removes a command from the bot

        Args:
            name (str): Command's name
        """

    def remove_method_after_commands(self,name):
        """
        Removes a method that is executed after each command

        Args:
            name (str): Method's name
        """

        self.custom_methods_after_commands.pop(name,None)

    def remove_method_before_commands(self,name):
        """
        Removes a method that is executed before each command

        Args:
            name (str): Method's name
        """

        self.custom_methods_before_commands.pop(name,None)