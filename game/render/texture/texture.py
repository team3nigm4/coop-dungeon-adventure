# Create the texture from image

import OpenGL.GL as gl
from PIL import Image as img

from game.render.texture import textureid as textureId
from game.screen import gamemanager as gameManager


class Texture:
	PATH = "game/resources/textures/"

	def __init__(self, path):
		# Default values
		self.texId = textureId.TextureId(Texture.PATH + path)
		self.width = 1
		self.height = 1
		self.correctLoaded = False

	def defaultInit(self):
		self.correctLoaded = False
		self.texId.setId(gameManager.GameManager.texManager.error.texId.getId())
		self.texId.setPath(gameManager.GameManager.texManager.error.texId.getPath())

	def load(self):
		try:
			image = img.open(self.texId.getPath())
			self.loadImage(image)
		except Exception:
			self.error()

	def loadImage(self, image):
		try:
			# Open the image
			flippedImage = image.transpose(img.FLIP_TOP_BOTTOM)
			imgData = flippedImage.convert("RGBA").tobytes()

			self.width = image.width
			self.height = image.height

			# Upload to openGL
			try:
				self.texId.setId(gl.glGenTextures(1))
				self.bind()
				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
				gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
				gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0,
								gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imgData)
				print("Texture num : " + str(self.texId.getId()) + " , loaded with path : " + self.texId.getPath())
				gameManager.GameManager.texManager.add(self.texId)
				self.correctLoaded = True
			except Exception:
				gl.glDeleteTextures(self.texId.getId())
				gameManager.GameManager.texManager.remove(self.texId)
				self.error()
		except Exception:
			self.error()

	def error(self):
		# When error, replace the current texture by the error texture
		print("Error on loading the texture " + str(self.texId.getId()) + " :\n" + self.texId.getPath())
		self.defaultInit()

	def bind(self):
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.texId.getId())

	def status(self):
		return self.correctLoaded

	def unload(self, status=True):
		# Security when error with unloaded textures
		if self.correctLoaded:
			gl.glDeleteTextures(self.texId.getId())
			gameManager.GameManager.texManager.remove(self.texId)
			self.correctLoaded = False
			if status:
				print("Texture num : " + str(self.texId.getId()) + ", unloaded.")
