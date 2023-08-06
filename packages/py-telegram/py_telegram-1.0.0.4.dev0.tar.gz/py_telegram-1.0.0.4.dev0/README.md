# Telegram Bot API Library
## Requirements
- Module requests (You can get it on: https://www.pypi.com/project/requests/)

## Errors and Exceptions
- `BotNotExistsError`: When the bot not exists, this error will raise.
- `NoInternetConnectionError`: When the computer has no Internet, this error will raise.

## Help
If you need help, just type `python -m py_telegram --help` to the shell. 

## Installation
For installing this library as python module, you just need to run `install.py`. 

If you want to uninstall, just type `python -m py_telegram --uninstall` to the shell. Then, the module will uninstall itself.

## Usage and initalisation
```python
import py_telegram
bot = telgrambot.bot(apikey: str)
```
Parameters
- apikey: 
Required, string. The API-Key of your bot (like `1234:abcdefg`).

## Methods
### Send a Text Message
You can send a Text message using the `bot.sendTextMessage()`
Returns a dictionary with the response and the status code of the request as an integer.
#### Syntax:
```python
bot.sendTextMessage(chat_id, text[, disable_web_page_preview = False, disable_notification = False, reply_to_message_id = None, allow_sending_without_reply = True, parse_mode = `MarkdownV2`])
```

#### Parameters:
- `chat_id`: Required, integer or string. Unique identifier of the chat.
- `text`: Required, string. The text to send as message.
- `disable_web_page_preview`: Optional, bool. Disabels the link preview for this message. Default is False.
- `disable_notification`: Optional, bool. Sends the message silently, when set to True. Default is False.
- `reply_to_message_id`: Optional, integer. If the message is a reply, the ID of the original message. Set this parameter to None, if you don`t want to send the message as a reply. Default is None.
- `allow_sending_without_reply`: Optional, integer. Sends the message even is the reply_to_message_id is invalid or not set. Default is True.
- ` parse_mode`: Optional, string. Mode for parsing entities in the message text. Must be set to:
    - `MarkdownV2`
    - `HTML`
    - `Markdown`
    
    Default is `MarkdownV2`
### Get Updates
You can use this method to receive incoming updates. 
Returns a dictionary with the response and the status code of the request as an integer.
#### Syntax:
```python
getUpdates([offset=None, limit=100, timeout=0, allowed_updates=[]])
```
#### Parameters:
- `offset`:
    Required, integer. Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. Default is None.
- `limit`:
    Required, integer. Limits the number of updates to be retrieved. Values between 1-100 are accepted. Default to 100.
- `timeout`:
    Required, integer. Timeout in seconds for long polling. Default is 0.
- `allowed_updates`:
    Required, array/list of strings. For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. Default is a empty array (will not be sended as parameter, if the array is empty).