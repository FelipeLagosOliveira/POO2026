import arcade 

ALTURA = 800
LARGURA = 600
NOME = "MEU JÓGOS"
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("direita.png", scale = 0.3)
        self.textura_direita = arcade.load_texture("direita.png")
        self.textura_esquerda = arcade.load_texture("esquerda.png")
    def update(self):
        pass


class JanelaJogo(arcade.Window):
    def __init__ (self):
        super().__init__(ALTURA,LARGURA,NOME)
        arcade.set_background_color(arcade.color.PURPLE_MOUNTAIN_MAJESTY)

        #criar meu personagem
        self.personagem = Player()
        #posicionar na tela
        self.personagem.center_x = 200
        self.personagem.center_y = 200

    
    def on_draw(self):
        self.clear()
        #desenhar meu personagem
        arcade.draw_sprite(self.personagem)

    def on_update(self, delta_time):
        pass

def main():
    tela = JanelaJogo()
    arcade.run()

if __name__ == "__main__":
    main()

