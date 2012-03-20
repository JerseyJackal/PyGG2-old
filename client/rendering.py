from __future__ import division, print_function

import pygrafix

import engine.gamestate
import constants

import function

import map_renderer
import character_renderer
import weapon_renderer
import projectile_renderer
import spectator
import engine.character
import engine.weapon
import engine.projectile
import hud_renderer

class GameRenderer(object):
    def __init__(self, client):
        self.window = client.window

        self.interpolated_state = engine.gamestate.Gamestate()
        self.renderers = {}
        self.focus_object_id = None

        self.view_width = constants.GAME_WIDTH
        self.view_height = constants.GAME_HEIGHT

        self.maprenderer = map_renderer.MapRenderer(self, "twodforttwo_remix")
        self.healthhud = None
        self.overlayblits = []

        self.renderers = {
            engine.character.Scout: character_renderer.ScoutRenderer(),
            engine.character.Pyro: character_renderer.PyroRenderer(),
            engine.character.Soldier: character_renderer.SoldierRenderer(),
            engine.character.Heavy: character_renderer.HeavyRenderer(),
            engine.character.Engineer: character_renderer.EngineerRenderer(),
            engine.character.Spy: character_renderer.SpyRenderer(),
            engine.weapon.Scattergun: weapon_renderer.ScattergunRenderer(),
            engine.weapon.Flamethrower: weapon_renderer.FlamethrowerRenderer(),
            engine.weapon.Rocketlauncher: weapon_renderer.RocketlauncherRenderer(),
            engine.weapon.Minigun: weapon_renderer.MinigunRenderer(),
            engine.weapon.Shotgun: weapon_renderer.ShotgunRenderer(),
            engine.weapon.Revolver: weapon_renderer.RevolverRenderer(),
            engine.projectile.Shot: projectile_renderer.ShotRenderer(),
            engine.projectile.Flame: projectile_renderer.FlameRenderer(),
            engine.projectile.Rocket: projectile_renderer.RocketRenderer()
        }

        self.world_sprites = []
        self.hud_sprites = []

    def render(self, client, game, frametime):
        # reset spritegroups
        self.world_sprites = []
        self.hud_sprites = []

        self.window = client.window
        alpha = game.accumulator / constants.PHYSICS_TIMESTEP

        self.interpolated_state.interpolate(game.previous_state, game.current_state, alpha)
        focus_object_id = game.current_state.players[client.our_player_id].character_id

        if focus_object_id != None:
            client.spectator.x = self.interpolated_state.entities[focus_object_id].x
            client.spectator.y = self.interpolated_state.entities[focus_object_id].y
            if game.current_state.entities[focus_object_id].just_spawned:
                self.healthhud = hud_renderer.HealthRenderer(self)
                game.current_state.entities[focus_object_id].just_spawned = False
            self.healthhud.render(self)
        else:
            if self.healthhud != None:
                self.healthhud = None
            player = game.current_state.players[client.our_player_id]
            if player.left:
                client.spectator.x -= 800*frametime
            elif player.right:
                client.spectator.x += 800*frametime
            if player.up:
                client.spectator.y -= 800*frametime
            elif player.down:
                client.spectator.y += 800*frametime
        # update view
        self.xview = int(int(client.spectator.x) - self.view_width / 2)
        self.yview = int(int(client.spectator.y) - self.view_height / 2)

        # clear screen if needed
        if client.spectator.x <= self.view_width / 2 or client.spectator.x + self.view_width >= game.map.width or client.spectator.y <= self.view_height / 2 or self.yview + self.view_height >= game.map.height:
            self.window.clear()

        # draw background
        self.maprenderer.render(self, self.interpolated_state)
        # draw entities
        for entity in self.interpolated_state.entities.values():
            self.renderers[type(entity)].render(self, game, self.interpolated_state, entity)

        pygrafix.sprite.draw_batch(self.world_sprites, scale_smoothing = False)
        pygrafix.sprite.draw_batch(self.hud_sprites, scale_smoothing = False)
        temp = (25,25)
        temp2 = (10,10)
        temp3 = (3,3,3)
        pygrafix.draw.rectangle(temp,temp2,temp3,0,None)
    def get_screen_coords(self, x, y):
        # calculate drawing position
        draw_x = int(x - self.xview)
        draw_y = int(y - self.yview)

        return draw_x, draw_y
