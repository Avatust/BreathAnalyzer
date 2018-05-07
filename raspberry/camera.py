import pygame
import pygame.camera


class Obscura:

    def __init__(self, device, resolution):
        pygame.camera.init()
        self.cam = pygame.camera.Camera(device, resolution)

    def take_and_save_img(self, filename):
        self.cam.start()
        img = self.cam.get_image()
        self.cam.stop()
        pygame.image.save(img, filename)
