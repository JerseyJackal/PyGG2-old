from functions import place_free, lengthdir, sign
import pygame

def objectCheckCollision(character, wallmask):

# Check if a the Character has hit the wall:

	hasCollided = False

	for index in range(len(wallmask)):

		if abs(wallmask[index].centerx-character.rect.centerx) < 50:
			if abs(wallmask[index].centery-character.rect.centery) < 50:
				if character.rect.colliderect(wallmask[index]):
					# Hit detected Flag as hit and break out.

					hasCollided = True
					break
	
	if hasCollided:
		return True
	else:
		return False



def characterHitObstacle(character, wallmask):



	newX = character.x
	newY = character.y

	oldX = character.x-character.hspeed
	oldY = character.y-character.vspeed

	hspeed = character.hspeed
	vspeed = character.vspeed


	length = lengthdir(hspeed, vspeed)

	if length == 0:# You haven't moved; if this happens something went wrong

		character.x = oldX
		character.y = oldY
		return False


	# hs and vs is the normalized vector of hspeed and vspeed.
	hs = character.hspeed/length
	vs = character.vspeed/length

	i = 0
	while objectCheckCollision(character, wallmask) and i < length:

		character.x = newX-(hs*i)
		character.y = newY-(vs*i)
		i += 1


	# The character got pushed out, but now we need to let him move in the directions he's allowed to move.

	character.x += sign(character.hspeed)

	if not objectCheckCollision(character, wallmask):

		# There's empty space on the left/right

		# Kill all vertical movement
		character.vspeed = 0

		i = 0
		while i <= hspeed:

			character.x = newX+(sign(character.hspeed)*i)

			# If the new position has met a wall too:
			if objectCheckCollision(character, wallmask):
				character.x = newX+(sign(character.hspeed)*(i-1))
				break

	else:
		character.x -= sign(character.hspeed)
		character.y += sign(character.vspeed)

		if not objectCheckCollision(character, wallmask):

			# There's empty space on the left/right

			# Kill all vertical movement
			character.hspeed = 0

			i = 0
			while i <= vspeed:

				character.y = newY+(sign(character.vspeed)*i)

				# If the new position has met a wall too:
				if objectCheckCollision(character, wallmask):
					character.y = newY+(sign(character.vspeed)*(i-1))
					break

		character.y -= sign(character.vspeed)
	

#	character.hspeed = 0
#	character.vspeed = 0

#	character.hspeed = oldX-character.x
#	character.vspeed = oldY-character.y

	return True


















	# The Character has collided; Push him back out:

	# This code was written for a situation before the character actually moved, but I want to keep this compatible with our structure.
	# Hence; move everything back, and move forward as far as we can.

	character.x -= character.hspeed
	character.y -= character.vspeed

	hleft = character.hspeed
	vleft = character.vspeed

	loopCounter = 0
	stuck = 0
	collisionRectified = True
	while((abs(hleft) >= 1 or abs(vleft) >= 1) and stuck == 0): # while we still have distance to travel
		loopCounter += 1
		if(loopCounter > 10):
		    # After 10 loops, it's assumed we're stuck. Stop all vertical movement.
			stuck = 1

		collisionRectified = False # set this to true when we fix a collision problem
		# (eg. detect hitting the ceiling and setting vspeed = 0)
		# if, after checking for all our possible collisions, we realize that we haven't
		# been able to fix a collision problem, then we probably hit a corner or something,
		# and we should try to fix that

		prevX = character.x
		prevY = character.y


		# move as far as we can without hitting something
		# In GMK, this was "move_contact_solid(point_direction(x, y, x + hleft, y + vleft), point_distance(x, y, x + hleft, y + vleft))"

		length = functions.lengthdir(hleft, vleft)
		distance = 0

		while distance < length:

			character.x = character.x+hleft*distance
			character.y = character.y+vleft*distance

			if objectCheckCollision(character, wallmask):
				character.x = character.x-hleft*distance
				character.y = character.y-vleft*distance
				break

			distance += length/20


		# deduct that movement from our remaining movement
		hleft -= (character.x - prevX)
		vleft -= (character.y - prevY)

		# determine what we hit, and act accordingly

		if(vleft != 0 and not functions.place_free(character.x, character.y + functions.sign(vleft), wallmask)):  # we hit a ceiling or floor
			if(vleft>0):
				moveStatus = 0 # floors, not ceilings, reset moveStatus
		
			vleft = 0 # don't go up or down anymore
			character.vspeed = 0 # don't try it next frame, either
			collisionRectified = True
	

		if(hleft != 0 and not functions.place_free(character.x + functions.sign(hleft), character.y, wallmask)):  # we hit a wall on the left or right
			moveStatus = 0
			if(functions.place_free(character.x + functions.sign(hleft), character.y - 6, wallmask)):  # if we could just walk up the step
				character.y -= 6 # hop up the step.
			collisionRectified = True
	
#		elif(functions.place_free(character.x + functions.sign(hleft), character.y + 6, wallmask) and abs(character.hspeed) >= abs(character.vspeed)): # ceiling sloping
#	
#			character.y += 6
#			collisionRectified = True
	
		else: # it's not just a step, we've actually gotta stop
	
			hleft = 0 # don't go left or right anymore
			characterhspeed = 0 # don't try it next frame, either
			collisionRectified = True
	

	if(not collisionRectified and (abs(hleft) >= 1 or abs(vleft) >= 1)):
		# uh-oh, no collisions fixed, try stopping all vertical movement and see what happens
		charactervspeed = 0
		vleft = 0
