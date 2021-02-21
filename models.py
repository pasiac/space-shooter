class ObserverSpritesGroup:
    """ It's observer pattern mixed with decorator pattern and iterator"""

    def __init__(self, sprites):
        self.sprites = sprites

    def add(self, sprite):
        self.sprites.add(sprite)

    def remove(self, sprite):
        self.sprites.remove(sprite)

    def update(self, *args, **kwargs):
        self.sprites.update(*args, **kwargs)

    def draw(self, *args, **kwargs):
        self.sprites.draw(*args, **kwargs)

    def __len__(self):
        return len(self.sprites)

    def __iter__(self):
        return iter(self.sprites)
