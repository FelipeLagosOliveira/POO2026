import arcade
import random


ALTURA = 600
LARGURA = 800
NOME = "A Fada das Moedas"
VELOCIDADE = 3


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("direita_p.png", scale=1)
        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("esquerda_p.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.right > LARGURA:
            self.right = LARGURA
            self.change_x = 0
        if self.top > ALTURA:
            self.top = ALTURA
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

        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1
        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1


class VilaoEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("bruxadir.png", scale=0.1)
        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("bruxaesq.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1
        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1


class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.4)


class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.6)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1
        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1


class TelaInicial(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Jogo - A Fada das Moedas", LARGURA / 2, 470,
            arcade.color.ROYAL_PURPLE, 25, anchor_x="center"
        )
        arcade.draw_text(
            "OBJETIVO", LARGURA / 2, 400,
            arcade.color.BLACK, 18, anchor_x="center"
        )
        arcade.draw_text(
            "Colete todas as moedas sem encostar nos vilões.",
            LARGURA / 2, 365, arcade.color.DARK_BLUE, 16, anchor_x="center"
        )
        arcade.draw_text(
            "Moeda comum: +1 ponto     Moeda especial: +10 pontos",
            LARGURA / 2, 335, arcade.color.DARK_BLUE, 16, anchor_x="center"
        )
        arcade.draw_text(
            "CONTROLES", LARGURA / 2, 275,
            arcade.color.BLACK, 18, anchor_x="center"
        )
        arcade.draw_text(
            "W A S D: movimentar a fada", LARGURA / 2, 240,
            arcade.color.DARK_GREEN, 16, anchor_x="center"
        )
        
        arcade.draw_text(
            "Pressione [J] para jogar", LARGURA / 2, 120,
            arcade.color.DARK_RED, 18, anchor_x="center"
        )
        arcade.draw_text(
            "Pressione [ESC] para sair", LARGURA / 2, 80,
            arcade.color.DARK_RED, 18, anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.PURPLE)

        self.background_list = arcade.SpriteList()
        background = arcade.Sprite("fundo.jpg")
        background.center_x = LARGURA / 2
        background.center_y = ALTURA / 2
        background.width = LARGURA
        background.height = ALTURA
        self.background_list.append(background)

        self.velocidade = VELOCIDADE
        self.pontuacao = 0
        self.tempo_decorrido = 0.0
        self.tirar_ponto = True

        self.sprite_moedas = arcade.SpriteList()

        # 25 moedas comuns
        for _ in range(25):
            moeda = Moeda()
            moeda.center_x = random.randint(50, LARGURA - 50)
            moeda.center_y = random.randint(50, ALTURA - 50)
            self.sprite_moedas.append(moeda)

        # 5 moedas especiais que se movimentam e valem 10 pontos
        self.moedas_especiais = arcade.SpriteList()
        for _ in range(5):
            moeda = MoedaEspecial()
            moeda.center_x = random.randint(80, LARGURA - 80)
            moeda.center_y = random.randint(80, ALTURA - 80)
            moeda.change_x = random.choice([-1, 1]) * self.velocidade
            moeda.change_y = random.choice([-1, 1]) * (self.velocidade - 1)
            self.moedas_especiais.append(moeda)
            self.sprite_moedas.append(moeda)

        self.jogador = Player()
        self.jogador.left = 0
        self.jogador.bottom = 0
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        self.vilao = Vilao()
        self.vilao.center_x = 650
        self.vilao.center_y = 500
        self.vilao.change_x = self.velocidade
        self.vilao.change_y = self.velocidade - 1
        self.sprite_vilao = arcade.SpriteList()
        self.sprite_vilao.append(self.vilao)

        self.vilao_especial = VilaoEspecial()
        self.vilao_especial.center_x = 350
        self.vilao_especial.center_y = 300
        self.vilao_especial.change_x = -self.velocidade
        self.vilao_especial.change_y = self.velocidade - 1
        self.sprite_vilao_especial = arcade.SpriteList()
        self.sprite_vilao_especial.append(self.vilao_especial)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.sprite_moedas.draw()
        self.sprite_vilao.draw()
        self.sprite_vilao_especial.draw()
        self.sprite_jogador.draw()

        arcade.draw_text(
            f"Moedas Coletadas: {self.pontuacao}", 10, 570,
            arcade.color.WHITE, 14
        )
        arcade.draw_text(
            f"Tempo: {int(self.tempo_decorrido)}s", LARGURA - 120, 570,
            arcade.color.WHITE, 14
        )

    def on_update(self, delta_time):
        self.tempo_decorrido += delta_time

        self.sprite_moedas.update()
        self.sprite_jogador.update()
        self.sprite_vilao.update()
        self.sprite_vilao_especial.update()  # Atualiza o vilão especial

        moedas_colididas = arcade.check_for_collision_with_list(
            self.jogador, self.sprite_moedas
        )
        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            if moeda in self.moedas_especiais:
                self.pontuacao += 10
            else:
                self.pontuacao += 1

        colisoes = arcade.check_for_collision_with_list(
            self.jogador, self.sprite_vilao
        )
        if colisoes and self.tirar_ponto:
            self.pontuacao -= 1
            self.tirar_ponto = False

        colisoes_especiais = arcade.check_for_collision_with_list(
            self.jogador, self.sprite_vilao_especial
        )
        if colisoes_especiais and self.tirar_ponto:
            self.pontuacao -= 3
            self.tirar_ponto = False

        if not colisoes and not colisoes_especiais:
            self.tirar_ponto = True

        if len(self.sprite_moedas) == 0:
            self.window.show_view(
                TelaVitoria(self.pontuacao, int(self.tempo_decorrido))
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.jogador.change_x = -self.velocidade
        elif key == arcade.key.D:
            self.jogador.change_x = self.velocidade
        elif key == arcade.key.W:
            self.jogador.change_y = self.velocidade
        elif key == arcade.key.S:
            self.jogador.change_y = -self.velocidade
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.jogador.change_x = 0
        if key in (arcade.key.W, arcade.key.S):
            self.jogador.change_y = 0


class TelaVitoria(arcade.View):
    def __init__(self, pontuacao_final, tempo_final):
        super().__init__()
        self.pontuacao = pontuacao_final
        self.cronometro = tempo_final

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Fim do Jogo", LARGURA / 2, 400,
            arcade.color.ROYAL_PURPLE, 24, anchor_x="center"
        )
        arcade.draw_text(
            f"Sua pontuação foi: {self.pontuacao}", LARGURA / 2, 350,
            arcade.color.ROYAL_PURPLE, 18, anchor_x="center"
        )
        arcade.draw_text(
            f"Tempo: {self.cronometro}s", LARGURA / 2, 315,
            arcade.color.ROYAL_PURPLE, 18, anchor_x="center"
        )
        arcade.draw_text(
            "Pressione [J] para jogar novamente", LARGURA / 2, 250,
            arcade.color.DARK_RED, 18, anchor_x="center"
        )
        arcade.draw_text(
            "Pressione [ESC] para sair", LARGURA / 2, 200,
            arcade.color.DARK_RED, 18, anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


def executar():
    janela = arcade.Window(LARGURA, ALTURA, NOME)
    janela.show_view(TelaInicial())
    arcade.run()


if __name__ == "__main__":
    executar()
