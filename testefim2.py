import arcade
import random


ALTURA = 600
LARGURA = 800
NOME = "A Fada das Moedas"
VELOCIDADE = 3
VELOCIDADE_VILAO_ESPECIAL = 6
ARQUIVO_FUNDO = "fundo.jpg"


class TelaComFundo(arcade.View):
    """View base que desenha o mesmo fundo em todas as telas."""

    def __init__(self):
        super().__init__()
        self.background_list = arcade.SpriteList()
        fundo = arcade.Sprite(ARQUIVO_FUNDO)
        fundo.center_x = LARGURA / 2
        fundo.center_y = ALTURA / 2
        fundo.width = LARGURA
        fundo.height = ALTURA
        self.background_list.append(fundo)

    def desenhar_fundo(self):
        self.background_list.draw()


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


class VilaoEspecial(Vilao):
    def __init__(self):
        arcade.Sprite.__init__(self, "bruxadir.png", scale=0.1)
        self.textura_direita = self.texture
        self.textura_esquerda = arcade.load_texture("bruxaesq.png")


class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.4)
        self.valor = 1


class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.6)
        self.valor = 10

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1
        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1


class TelaInicial(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        arcade.draw_text("Jogo - A Fada das Moedas", LARGURA / 2, 470,
                         arcade.color.YELLOW, 25, anchor_x="center")
        arcade.draw_text("OBJETIVO", LARGURA / 2, 400,
                         arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Colete todas as moedas sem encostar nos vilões.",
                         LARGURA / 2, 365, arcade.color.DARK_BLUE, 16,
                         anchor_x="center")
        arcade.draw_text("Moeda comum: +1 ponto     Moeda especial: +10 pontos",
                         LARGURA / 2, 335, arcade.color.WHITE, 16,
                         anchor_x="center")
        arcade.draw_text("[I] Instruções     [S] Sobre     [J] Jogar     [ESC] Sair",
                         LARGURA / 2, 100, arcade.color.YELLOW, 18,
                         anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.I:
            self.window.show_view(TelaInstrucoes())
        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class TelaInstrucoes(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        arcade.draw_text("INSTRUÇÕES", LARGURA / 2, 470,
                         arcade.color.YELLOW, 26, anchor_x="center")
        textos = [
            "W ou S: mover para cima ou para baixo",
            "A ou D: mover para a esquerda ou para a direita",
            "Colete as moedas comuns para ganhar 1 ponto.",
            "Colete as moedas especiais para ganhar 10 pontos.",
            "Evite o vilão comum (-1 ponto) e a bruxa (-3 pontos).",
            "Pressione ESC para voltar ao menu principal.",
        ]
        for indice, texto in enumerate(textos):
            arcade.draw_text(texto, LARGURA / 2, 380 - indice * 42,
                             arcade.color.DARK_BLUE, 16, anchor_x="center")
        arcade.draw_text("Pressione ESC para voltar", LARGURA / 2, 90,
                         arcade.color.DARK_RED, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


class TelaSobre(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        arcade.draw_text("SOBRE O JOGO", LARGURA / 2, 470,
                         arcade.color.YELLOW, 26, anchor_x="center")
        arcade.draw_text("A Fada das Moedas", LARGURA / 2, 380,
                         arcade.color.DARK_BLUE, 22, anchor_x="center")
        arcade.draw_text("Um jogo de coleta e desvio criado com Python e Arcade.",
                         LARGURA / 2, 335, arcade.color.BLACK, 16,
                         anchor_x="center")
        arcade.draw_text("Desvie dos inimigos, colete tudo e faça a maior pontuação!",
                         LARGURA / 2, 295, arcade.color.BLACK, 16,
                         anchor_x="center")
        arcade.draw_text("Pressione ESC para voltar", LARGURA / 2, 90,
                         arcade.color.DARK_RED, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


class TelaJogo(TelaComFundo):
    def __init__(self):
        super().__init__()
        self.velocidade = VELOCIDADE
        self.pontuacao = 0
        self.tempo_decorrido = 0.0
        self.tirar_ponto = True

        self.sprite_moedas = arcade.SpriteList()
        for _ in range(25):
            moeda = Moeda()
            moeda.center_x = random.randint(50, LARGURA - 50)
            moeda.center_y = random.randint(50, ALTURA - 50)
            self.sprite_moedas.append(moeda)

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
        self.sprite_jogador = arcade.SpriteList(self.jogador)

        self.vilao = Vilao()
        self.vilao.center_x, self.vilao.center_y = 650, 500
        self.vilao.change_x, self.vilao.change_y = self.velocidade, self.velocidade - 1
        self.sprite_vilao = arcade.SpriteList(self.vilao)

        self.vilao_especial = VilaoEspecial()
        self.vilao_especial.center_x, self.vilao_especial.center_y = 350, 300
        self.vilao_especial.change_x = -VELOCIDADE_VILAO_ESPECIAL
        self.vilao_especial.change_y = VELOCIDADE_VILAO_ESPECIAL - 1
        self.sprite_vilao_especial = arcade.SpriteList(self.vilao_especial)

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        self.sprite_moedas.draw()
        self.sprite_vilao.draw()
        self.sprite_vilao_especial.draw()
        self.sprite_jogador.draw()
        arcade.draw_text(f"Moedas Coletadas: {self.pontuacao}", 10, 570,
                         arcade.color.YELLOW, 14)
        arcade.draw_text(f"Tempo: {int(self.tempo_decorrido)}s", LARGURA - 120, 570,
                         arcade.color.YELLOW, 14)

    def on_update(self, delta_time):
        self.tempo_decorrido += delta_time
        self.sprite_moedas.update()
        self.sprite_jogador.update()
        self.sprite_vilao.update()
        self.sprite_vilao_especial.update()

        for moeda in arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas):
            self.pontuacao += moeda.valor
            moeda.remove_from_sprite_lists()

        colisoes = arcade.check_for_collision_with_list(self.jogador, self.sprite_vilao)
        colisoes_especiais = arcade.check_for_collision_with_list(
            self.jogador, self.sprite_vilao_especial)
        if (colisoes or colisoes_especiais) and self.tirar_ponto:
            self.pontuacao -= 3 if colisoes_especiais else 1
            self.tirar_ponto = False
        if not colisoes and not colisoes_especiais:
            self.tirar_ponto = True

        if len(self.sprite_moedas) == 0:
            self.window.show_view(TelaVitoria(self.pontuacao, int(self.tempo_decorrido)))

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


class TelaVitoria(TelaComFundo):
    def __init__(self, pontuacao_final, tempo_final):
        super().__init__()
        self.pontuacao = pontuacao_final
        self.cronometro = tempo_final

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()
        arcade.draw_text("Fim do Jogo", LARGURA / 2, 400,
                         arcade.color.ROYAL_PURPLE, 24, anchor_x="center")
        arcade.draw_text(f"Sua pontuação foi: {self.pontuacao}", LARGURA / 2, 350,
                         arcade.color.ROYAL_PURPLE, 18, anchor_x="center")
        arcade.draw_text(f"Tempo: {self.cronometro}s", LARGURA / 2, 315,
                         arcade.color.ROYAL_PURPLE, 18, anchor_x="center")
        arcade.draw_text("[J] Jogar novamente     [ESC] Voltar ao menu",
                         LARGURA / 2, 220, arcade.color.DARK_RED, 18,
                         anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


def executar():
    janela = arcade.Window(LARGURA, ALTURA, NOME)
    janela.show_view(TelaInicial())
    arcade.run()


if __name__ == "__main__":
    executar()
