import pygame

class SoundManager:

    def __init__(self) -> None:
        """
        Creates a sound manager object

        Args:
            None

        Returns:
            None

        """
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.set_num_channels(15)
         

        self.sounds = {
            "laser1": self.mixer.Sound("./usedAssets/sounds/sfx_laser1.ogg"),
            "laser2": self.mixer.Sound("./usedAssets/sounds/sfx_laser2.ogg"),
            "zap": self.mixer.Sound("./usedAssets/sounds/sfx_zap.ogg"),
        }

    def play(self, sound:str, loop:bool=False, volume:float=0.1) -> None:
        """
        Plays a sound

        Args:
            sound (str): sound to be played
            loop (bool, optional): if the sound should loop. Defaults to False.
            volume (float, optional): volume of the sound. Defaults to 0.1.

        Returns:
            None
        """
        self.mixer.Sound("./usedAssets/sounds/sfx_twoTone.ogg").play()
        print("Play")
        #find an unused channel
        channel = self.mixer.find_channel()
        if channel:
            self.sounds[sound].set_volume(volume)
            if loop:
                channel.play(self.sounds[sound], -1)

            else:
                channel.play(self.sounds[sound]) 

        