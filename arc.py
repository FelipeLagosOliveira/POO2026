import arcade, random

ALTURA = 800
LARGURA = 600
NOME = "MEU JOGO"
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("direita_p.png", scale= 1)
        
        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("esquerda_p.png")
        
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.right > 800:
            self.right = 800
            self.change_x = 0
        if self.top > 600:
            self.top = 600
            self.change_y = 0
        if self.left < 0:
            self.left = 0
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0

class Vilao(arcade.Sprite):
    def __init__(self):
        super().__init__("vilaodireita.png", scale=0.1)
        
        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("vilaoesquerda.png")


    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote no Eixo X
        if self.left <= 0 or self.right >= 800:
            self.change_x *= -1  
        # Rebote no Eixo Y
        if self.bottom <= 0 or self.top >= 600:
            self.change_y *= -1


class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.4)
        
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > 800:
            self.right = 800
            self.change_x = 0
        if self.top > 600:
            self.top = 600
            self.change_y = 0
        if self.left < 0:
            self.left = 0
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0

class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.6)
        
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote no Eixo X
        if self.left <= 0 or self.right >= 800:
            self.change_x *= -1  
        # Rebote no Eixo Y
        if self.bottom <= 0 or self.top >= 600:
            self.change_y *= -1

# Criação de Tela Inicial
class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("Jogo - A fada das moedas", LARGURA/2, 400, arcade.color.ROYAL_PURPLE, 18, anchor_x="center")
        arcade.draw_text("Pressione [J] para Jogar", LARGURA/2, 300, arcade.color.DARK_RED, 18,)
        arcade.draw_text("Pressione [Esc] para Sair", LARGURA/2, 250, arcade.color.DARK_RED, 18,)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)
        
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
        
        

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.PURPLE)

        self.velocidade = 3
        self.pontuacao = 0

        # Lista de moedas
        self.sprite_moedas = arcade.SpriteList()
        for i in range(25):
            moeda = Moeda()
            moeda.center_x = random.randint(50, 750)
            moeda.center_y = random.randint(50, 550)
            self.sprite_moedas.append(moeda)

        # Criar uma moeda especial
        self.moeda_especial = MoedaEspecial()
        self.moeda_especial.center_x = 650  
        self.moeda_especial.center_y = 500
        self.moeda_especial.change_x = self.velocidade
        self.moeda_especial.change_y = self.velocidade-1
        self.sprite_moedas.append(self.moeda_especial)

        # Criar o jogador
        self.jogador = Player()
        self.jogador.left = 0
        self.jogador.bottom = 0
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        # Criar o Vilao
        self.sprite_vilao = arcade.SpriteList()
        self.vilao = Vilao()
        self.vilao.center_x = 650  
        self.vilao.center_y = 500
        self.vilao.change_x = self.velocidade
        self.vilao.change_y = self.velocidade - 1
        self.sprite_vilao.append(self.vilao) # Adiciona na lista correta

        
    def on_draw(self):
        self.clear() 
        # Desenhe os personagens aqui!
        self.sprite_moedas.draw()
        self.sprite_vilao.draw() 
        self.sprite_jogador.draw()

        arcade.draw_text(f"Moedas Coletadas: {self.pontuacao}", 10, 570, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.sprite_moedas.update()
        self.sprite_jogador.update()
        self.sprite_vilao.update()

        moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas)
        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            # SE for moeda especial, soma 5 pontos, senão soma 1 ponto
            if moeda == self.moeda_especial:
                self.pontuacao += 5
            else:
                self.pontuacao += 1

        colisao_vilao = arcade.check_for_collision_with_list(self.jogador,self.sprite_vilao)
        for vilao in colisao_vilao:
            if vilao == self.vilao:
                self.pontuacao -= 3


        # Gerenciamento do Teclado (Explicado abaixo)
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A: # Seta da esquerda ou A
            self.jogador.change_x = -self.velocidade
        elif key == arcade.key.D: # Seta da direita ou D
            self.jogador.change_x = self.velocidade
        elif key == arcade.key.W: # Seta de cima ou W
            self.jogador.change_y = self.velocidade
        elif key == arcade.key.S: # Seta de baixo ou s
            self.jogador.change_y = -self.velocidade

        if (key == arcade.key.ESCAPE): 
            tela_incial = TelaInicial()
            self.window.show_view(tela_incial)


    def on_key_release(self, key, modifiers):
        # Ao soltar uma tecla, verifica se é do eixo X ou Y para zerar a velocidade
        if key in [arcade.key.A, arcade.key.D]:
            self.jogador.change_x = 0
        if key in [arcade.key.W, arcade.key.S]:
            self.jogador.change_y = 0

'''class TelaVitoria(arcade.View):
    def __init__(self):

    def on_draw(self):'''
        


def executar():
    #Cria a janela principal do jogo
    
    janela = arcade.Window(LARGURA, ALTURA,"Jogo")
    # Cria uma tela inicial 
    tela_inicial = TelaInicial()
    # Alimenta a janela com o menu e roda o loop do jogo
    janela.show_view(tela_inicial)
    arcade.run()

if __name__ == "__main__":
    executar()