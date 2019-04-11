# Create the texture from image

import OpenGL.GL as gl
from PIL import Image as img

from game.util.logger import Logger


class Texture:
	PATH = "game/resources/textures/"

	def __init__(self, path):
		# Default values
		self.path = Texture.PATH + path
		self.width = 0
		self.height = 0
		self.correctLoaded = False
		self.id = 0

	def load(self):
		try:
			image = img.open(self.path)
			self.loadImage(image)
		except Exception as error:
			self.error(error)
			return False

	def loadImage(self, image):
		try:
			# Open the image
			flippedImage = image.transpose(img.FLIP_TOP_BOTTOM)
			imgData = flippedImage.convert("RGBA").tobytes()

			self.width = image.width
			self.height = image.height

			# Upload to openGL
			try:
				self.id = gl.glGenTextures(1)
				self.bind()
				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
				gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imgData)
				Logger.info("TEXTURE +", "Texture n°" + str(self.id) + " loaded (" + self.path.replace(self.PATH, '') + ")")
				self.correctLoaded = True
			except Exception as error:
				gl.glDeleteTextures(self.id)
				self.error(error)
				return False
		except Exception as error:
			self.error(error)
			return False

	def error(self, error):
		# When error, replace the current texture by the error texture
		Logger.error("TEXTURE", "Error while loading texture n°" + str(self.id) + " (" + self.path.replace(self.PATH, '') + ')')
		Logger.bold("Error returned :")
		print("  " + str(error) + "\n")

	def bind(self):
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.id)

	def status(self):
		return self.correctLoaded

	def unload(self, status=True):
		# Security when error with unloaded textures
		if self.correctLoaded:
			gl.glDeleteTextures(self.id)
			self.correctLoaded = False
			if status:
				Logger.info("TEXTURE -", "Texture n°" + str(self.id) + " unloaded")
