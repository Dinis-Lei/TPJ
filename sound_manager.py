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
            "hit": self.mixer.Sound("./usedAssets/sounds/sfx_twoTone.ogg"),
            "lose": self.mixer.Sound("./usedAssets/sounds/sfx_lose.ogg"),
            "lifeUp": self.mixer.Sound("./usedAssets/sounds/sfx_shieldUp.ogg"),
            "lifeDown": self.mixer.Sound("./usedAssets/sounds/sfx_shieldDown.ogg"),
        }

    def play(self, sound:str, loops:int=0, volume:float=0.1) -> None:
        """
        Plays a sound

        Args:
            sound (str): sound to be played
            loop (bool, optional): if the sound should loop. Defaults to False.
            volume (float, optional): volume of the sound. Defaults to 0.1.

        Returns:
            None
        """
        channel = self.mixer.find_channel()
        if channel:
            self.sounds[sound].set_volume(volume)
            channel.play(self.sounds[sound], loops=loops) 

        