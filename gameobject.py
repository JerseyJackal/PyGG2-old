import pygame
from pygame.locals import *
from load_image import load_image
from collision import characterHitObstacle, objectCheckCollision

class GameObject(pygame.sprite.Sprite):

	def __init__(self, root, xpos, ypos):

		pygame.sprite.Sprite.__init__(self)

		self.root = root

		self.x = xpos
		self.y = ypos

		self.oldX = xpos
		self.oldY = ypos

		self.hspeed = 0
		self.vspeed = 0

		self.sprite = -1
		self.rect = -1

		self.xImageOffset = 0
		self.yImageOffset = 0

		self.xRectOffset = 0
		self.yRectOffset = 0

		self.root.GameObjectList.append(self)


	def beginStep(self):

		pass


	def step(self):

		pass


	def endStep(self):

		if self.x < 0.0:
			self.x = 0.0

		if self.y < 0.0:
			self.y = 0.0

		self.x += self.hspeed
		self.y += self.vspeed
		if self.rect != -1:
			self.rect.topleft = (self.x-self.xRectOffset, self.y-self.yRectOffset)


	def collide(self):
		self.oldX = self.x
		self.oldY = self.y

	def draw(self):

		if self.sprite != -1:
			self.root.Surface.blit(self.sprite, ((self.x+self.xImageOffset)-self.root.Xview, (self.rect.top+self.yImageOffset)-self.root.Yview))
			
class MapObject(GameObject):

	def __init__(self, root):

		GameObject.__init__(self, root, 0, 0)

		self.sprite = pygame.image.load("Maps/MapTesting.png")
		self.sprite.convert_alpha()
		self.sprite.convert()
		self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width()*6, self.sprite.get_height()*6))


		self.rect = pygame.Rect(0, 0, self.sprite.get_width(), self.sprite.get_height())

		self.root.Surface.blit(self.sprite, (0, 0))

		self.mask = pygame.mask.from_surface(self.sprite)

		print self.mask.count()


		self.root.map = self

	def draw(self):

		self.root.Surface.blit(self.sprite, (0-self.root.Xview, 0-self.root.Yview))


class PlayerControl(GameObject):

	def __init__(self, root):

		GameObject.__init__(self, root, 0, 0)


	def beginStep(self):

		up = 0
		left = 0
		right = 0
		LMB = 0
		RMB = 0

		for event in pygame.event.get():
			pass

		key = pygame.key.get_pressed()
		if key[K_w]:
			up = 1

		if key[K_a]:
			left = 1

		elif key[K_d]:
			right = 1

		LMB, middleMouseButton, RMB = pygame.mouse.get_pressed()

		# Send keybyte

		self.root.Myself.up = up
		self.root.Myself.left = left
		self.root.Myself.right = right
		self.root.Myself.LMB = LMB
		self.root.Myself.RMB = RMB
