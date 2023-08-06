import requests
import socket
import json


class Error(OSError):
    pass


class BotNotExistsError(Error):
    """
    When the bot not exists, this error will raise.
    """


class NoInternetConnectionError(Error):
    """
    When the computer has no Internet, this error will raise.
    """


class RequestError(Error):
    """
    When the request has an other return code as 200, this error will raise.
    """


class ValueNotInRangeError(Error):
    """
    When a parameter of a function is not in range, this error will raise.
    """


class bot:
    def _checkInternetConnection(self):
        """
        This function is checking the internet connection with making a head-request for google.com.
        """
        try:
            requests.head(url="http://www.google.com")
            return True
        except requests.exceptions.ConnectionError:
            return False
        else:
            return False

    def __init__(self,
                 apikey: str):
        """
        Initalize the bot API. 

        Syntax:
            bot = py_telegram.bot(apikey)

        Parameters:
            - apikey:
                Required. The API-Key of your bot (like '1234:abcdefg').
        """
        if(self._checkInternetConnection() == False):
            raise NoInternetConnectionError(
                "Your Computer is not connected to the Internet.")

        self.apikey = apikey

    def _send_request(self, method: str, request_data: list):
        request_data_str = "?"
        x = 0
        for i in request_data:
            request_data_str = request_data_str + str(request_data[x]) + "&"
            x = x + 1
        request = requests.get(
            "https://api.telegram.org/bot" + self.apikey + "/" + method + request_data_str)
        if not request.status_code == 200:
            raise RequestError("The status code of the GET request was " + str(
                request.status_code) + "\n and the data from the server was: \n" + request.text)
        else:
            return request.text, request.status_code

    def sendTextMessage(self, chat_id: int or str, text: str, disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None, allow_sending_without_reply=True, parse_mode='MarkdownV2'):
        """
        Send a Text Message. 

        Syntax:
            bot.sendTextMessage(chat_id, text[, disable_web_page_preview = False, disable_notification = False, reply_to_message_id = None, allow_sending_without_reply = True, parse_mode = 'MarkdownV2'])

        Parameters:
            - chat_id:
                Required, integer or string. Unique identifier of the chat.
            - text:
                Required, string. The text to send as message.
            - disable_web_page_preview:
                Optional, bool. Disabels the link preview for this message. Default is False.
            - disable_notification:
                Optional, bool. Sends the message silently, when set to True. Default is False.
            - reply_to_message_id:
                Optional, integer. If the message is a reply, the ID of the original message. Set this parameter to None, if you don't want to send the message as a reply. Default is None.
            - allow_sending_without_reply:
                Optional, integer. Sends the message even is the reply_to_message_id is invalid or not set. Default is True.
            - parse_mode:
                Optional, string. Mode for parsing entities in the message text. Must be set to:
                    - 'MarkdownV2'
                    - 'HTML'
                    - 'Markdown'
                Default is 'MarkdownV2'
        Returns a dictionary with the response and the status code of the request as an integer.
        """
        chat_id = str(chat_id)
        text = str(text)
        disable_web_page_preview = str(disable_web_page_preview)
        disable_notification = str(disable_notification)
        allow_sending_without_reply = str(allow_sending_without_reply)
        parse_mode = str(parse_mode)

        request_data = []
        request_data.append("chat_id=" + str(chat_id))
        request_data.append("text=" + text)
        request_data.append("disable_web_page_preview=" +
                            disable_web_page_preview)
        request_data.append("disable_notification=" + disable_notification)
        request_data.append("allow_sending_without_reply=" +
                            allow_sending_without_reply)
        request_data.append("parse_mode=" + parse_mode)

        if not reply_to_message_id == None:
            reply_to_message_id = str(reply_to_message_id)
            request_data.append("reply_to_message_id=" + reply_to_message_id)

        r_text, r_status_code = self._send_request("sendMessage", request_data)
        return json.loads(r_text), int(r_status_code)

    def getUpdates(self, offset=None, limit=100, timeout=0, allowed_updates=[]):
        """
        Use this method to receive incoming updates. 

        Syntax:
            bot.getUpdates([offset=None, limit=100, timeout=0, allowed_updates=[]])

        Parameters:
            - offset:
                Required, integer. Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. Default is None.
            - limit:
                Required, integer. Limits the number of updates to be retrieved. Values between 1-100 are accepted. Default to 100.
            - timeout:
                Required, integer. Timeout in seconds for long polling. Default is 0.
            - allowed_updates:
                Required, array/list of strings. For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. Default is a empty array (will not be sended as parameter, if the array is empty.)

        Returns a dictionary with the response and the status code of the request as an integer.
        """
        request_data = []
        if not int(limit) > 0 and int(limit) < 101:
            raise ValueNotInRangeError(
                "The value of the limit parameter is not in range. Please type a value between 1 and 100.")
        if not offset == None:
            request_data.append("offset=" + str(offset))
        if not allowed_updates == []:
            request_data.append("allowed_updates=" + str(allowed_updates))
        if not limit == 100:
            request_data.append("limit=" + str(limit))
        if not timeout == 0:
            request_data.append("timeout=" + str(timeout))

        r_text, r_status_code = self._send_request("getUpdates", request_data)
        return json.loads(r_text), int(r_status_code)

    def getCommands(self):
        """
        Get the Bot Commands.

        Syntax:
            bot.getCommands()

        Parameters:
            There are no parameters.

        Returns a dictionary with the response and the status code of the request as an integer.
        """
        r_text, r_status_code = self._send_request("getMyCommands", [])
        return json.loads(r_text)["result"], int(r_status_code)

    def setCommands(self, commands: dict):
        """
        Set the Bot Commands.

        Syntax:
            bot.setCommands(commands)

        Parameters:
            - commands:
                Required, dictionary. The commands to set (like [{"command":"test","description":"this is only a test"},{"command":"testest","description":"second test"}]). The Key of
                this dictionary should be th actual command, the value should be the description.

        Returns a dictionary with the response and the status code of the request as an integer.
        """
        commands = json.dumps(commands)
        r_text, r_status_code = self._send_request(
            "setMyCommands", ["commands=" + commands])
        return json.loads(r_text), int(r_status_code)
