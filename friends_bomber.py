import sys
from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.hmessage import HMessage
from g_python.hpacket import HPacket

extension_info = {
    "title": "Friends Bomber",
    "description": "Add all peoples in a Room",
    "version": "1.0",
    "author": "!\"nota#0445"
}

friends = []

ext = Extension(extension_info, sys.argv)   # sys.argv are the commandline arguments, for example ['-p', '9092'] (G-Earth's extensions port)
ext.start()

def friends_in_account(message: HMessage):
    packet = message.packet
    packet.read('ii')
    friends_number = packet.read_int()
    for x in range(friends_number):
        packet.read_int()
        username = packet.read_string()
        print(username)
        friends.append(username)
        packet.read('iBBsisssBBBu') 

def update_friend(message: HMessage):
    packet = message.packet
    packet.read('iiii')
    username = packet.read_string()
    friends.append(username)


def users_in_room(message: HMessage):
    packet = message.packet
    packet.read('ii')
    username = packet.read_string()
    if not username in friends:
        ext.send_to_server(HPacket('RequestFriend', username))

ext.intercept(Direction.TO_CLIENT, friends_in_account, 'FriendListFragment')
ext.intercept(Direction.TO_CLIENT, users_in_room, 'Users')
ext.intercept(Direction.TO_CLIENT, update_friend, 'FriendListUpdate')