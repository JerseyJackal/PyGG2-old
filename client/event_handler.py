from __future__ import division, print_function

# add our main folder as include dir
import sys
sys.path.append("../")

import struct
import engine.map
import engine.player
import function, constants
from networking import event_serialize


def Server_Event_Hello(networker, game, event):
    # Stop saying hello
    networker.has_connected = True
    # TODO: Some version check using event.version and constants.GAME_VERSION_NUMBER
    # Set all the important values to the game
    game.servername = event.servername
    game.maxplayers = event.maxplayers
    game.map = engine.map.Map(game, event.mapname)

def Server_Event_Player_Join(networker, game, event):
    newplayer = engine.player.Player(game, game.current_state, event.id)
    newplayer.name = event.name

def Server_Event_Changeclass(networker, game, event):
    player = game.current_state.players[event.playerid]
    player.nextclass = event.newclass

def Server_Event_Die(networker, game, event):
    player = game.current_state.players[event.playerid]
    character = game.current_state.enities[player.character_id]
    character.die(game, game.current_state)

def Server_Event_Spawn(networker, game, event):
    player = game.current_state.players[event.playerid]

def Server_Snapshot_Update(networker, game, event):
    state = game.current_state
    for playerid, player in state.players:
        player.deserialize_input(event.bytestr)

        character = state.entities[player.character_id]
        character.deserialize(state)

def Server_Full_Update(networker, game, event):
    numof_players = struct.unpack_from(">B", event.bytestr)[0]
    event.bytestr = event.bytestr[1:]

    for index in range(numof_players):
        player = engine.player.Player(game, game.current_state, index)

        player.name, player_class = struct.unpack_from(">32pB", event.bytestr)
        player.nextclass = function.convert_class(player_class)
        event.bytestr = event.bytestr[33:]

        # TODO: Make spawning not instant
        #if character_exists:
        #    player.spawn(game, game.current_state)

    Server_Snapshot_Update(networker, game, event)


# Gather the functions together to easily be called by the event ID
eventhandlers = {}
eventhandlers[constants.EVENT_HELLO] = Server_Event_Hello
eventhandlers[constants.EVENT_PLAYER_JOIN] = Server_Event_Player_Join
eventhandlers[constants.EVENT_PLAYER_CHANGECLASS] = Server_Event_Changeclass
eventhandlers[constants.EVENT_PLAYER_DIE] = Server_Event_Die
eventhandlers[constants.EVENT_PLAYER_SPAWN] = Server_Event_Spawn
eventhandlers[constants.SNAPSHOT_UPDATE] = Server_Snapshot_Update
eventhandlers[constants.FULL_UPDATE] = Server_Full_Update
