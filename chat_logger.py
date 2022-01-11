import socket
import logging
from emoji import demojize
import re
def get_chat_dataframe(userMessage):
    data = []
    try:
        pattern = re.compile(":(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)")
        if pattern.match(userMessage) :
            print(userMessage)
            username, channel, message = re.search(
            ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', userMessage
            ).groups()

            d = {
            'channel': channel,
            'username': username,
            'message': str(message).replace("\r", "")
            }

            data.append(d)
            print(data)

    except Exception:
        pass

"""
Get token here: https://twitchapps.com/tmi/
"""

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'THE_NAME_OF_YOUR_CHANNEL_HERE'
token = 'oauth:YOUR_TOKEN_HERE'
channel = '#THE_NAME_OF_THE_LIVE_CHANNEL' # Keep the #


def main():
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                get_chat_dataframe(demojize(resp))
                logging.info(demojize(resp))
    except KeyboardInterrupt:
        sock.close()
        exit()

if __name__ == '__main__':
    main()