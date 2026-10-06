import datetime
import os
import random

import arcade
from peewee import (Model, SqliteDatabase, CharField, IntegerField,
                    FloatField, DateTimeField)

# ---------------------------------------------------------------------------
# Constantes globais
# ---------------------------------------------------------------------------
ALTURA = 600
LARGURA = 800
NOME = "A Fada das Moedas"
VELOCIDADE = 3
VELOCIDADE_VILAO_ESPECIAL = 5
ARQUIVO_FUNDO = "fundo.jpg"
GRAVIDADE = 0.5
FORCA_PULO = 16
TAMANHO_MAX_NOME = 12

# Efeitos de colisão (durações em segundos)
TEMPO_INVENCIVEL = 1.5      # imunidade depois de um golpe
TEMPO_FLASH = 0.3           # clarão vermelho
TEMPO_TREMOR = 0.35         # tremor de tela
INTENSIDADE_TREMOR = 8      # deslocamento máximo da câmera, em pixels

# ** SPRITES DE DANO DA FADA (DIREITA E ESQUERDA) **
ARQUIVO_TREMIDO_D = "tremido_p_dir.png"   # Fada com olhar de espanto/dano (virada p/ direita)
ARQUIVO_TREMIDO_E = "tremido_p_esq.png"   # Fada com olhar de espanto/dano (virada p/ esquerda)
TEMPO_TREMIDA = 0.35                      # Quanto tempo a fada fica no estado de dano
REDUCAO_VELOCIDADE = 0.1                  # Quanto a velocidade cai a cada colisão com vilão
VELOCIDADE_MINIMA = 0.5                   # A velocidade nunca fica abaixo disso

# ---------------------------------------------------------------------------
# Banco de dados (Peewee ORM)
# ---------------------------------------------------------------------------
db = SqliteDatabase("ranking.db")


class BaseModel(Model):
    """Classe mãe de todas as tabelas: define em qual banco elas moram."""

    class Meta:
        database = db


class Pontuacao(BaseModel):
    """Cada objeto Pontuacao é uma partida salva no ranking."""

    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.nome_jogador} - {self.pontos} pts ({self.tempo_partida:.1f}s)"


def inicializar_banco():
    """Abre a conexão e cria as tabelas que ainda não existem."""
    db.connect(reuse_if_open=True)
    db.create_tables([Pontuacao])


def buscar_top10():
    """Devolve as 10 melhores pontuações; em caso de empate, vence o mais rápido."""
    consulta = (Pontuacao
                .select()
                .order_by(Pontuacao.pontos.desc(), Pontuacao.tempo_partida.asc())
                .limit(10))
    return list(consulta)


# ---------------------------------------------------------------------------
# Sprites
# ---------------------------------------------------------------------------
class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("bloco.png", scale=1)
        self.center_x = x
        self.center_y = y


class TelaComFundo(arcade.View):
    """View base que desenha o fundo padronizado em todas as telas."""

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
        self.olhando_direita = True

        # ** TEXTURAS DE DANO/IMPACTO (A FADA ESPANTADA/VERMELHA) **
        self.textura_tremida_d = arcade.load_texture(ARQUIVO_TREMIDO_D)
        self.textura_tremida_e = arcade.load_texture(ARQUIVO_TREMIDO_E)
        self.tempo_tremida = 0.0   # zero = não está tremendo
        self.tempo_troca = 0.0
        self.lado_tremida = True

    def tremer(self):
        """Liga o estado de dano/impacto por TEMPO_TREMIDA segundos."""
        self.tempo_tremida = TEMPO_TREMIDA

    def update(self, delta_time):
        self.center_x += self.change_x

        # Atualiza a orientação da textura normal
        if self.change_x > 0:
            self.texture = self.textura_direita
            self.olhando_direita = True
        elif self.change_x < 0:
            self.texture = self.textura_esquerda
            self.olhando_direita = False

        # Limites da tela
        if self.right > LARGURA:
            self.right = LARGURA
            self.change_x = 0

        if self.left < 0:
            self.left = 0
            self.change_x = 0

        # ** TEXTURA DE COLISÃO / TREMIDO DA PERSONAGEM **
        if self.tempo_tremida > 0:
            self.tempo_tremida = max(0.0, self.tempo_tremida - delta_time)
            self.tempo_troca += delta_time
            if self.tempo_troca >= 0.05:      # alterna rapidamente o lado para dar o efeito de tremer
                self.tempo_troca = 0.0
                self.lado_tremida = not self.lado_tremida
            
            # ** APLICA A TEXTURA DE DANO NA DIREÇÃO CORRETA OU ALTERNADA **
            if self.lado_tremida:
                self.texture = self.textura_tremida_d
            else:
                self.texture = self.textura_tremida_e


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


# ---------------------------------------------------------------------------
# Telas
# ---------------------------------------------------------------------------
class TelaInicial(TelaComFundo):
    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text("Jogo - A Fada das Moedas", LARGURA / 2, 470,
                         arcade.color.YELLOW, 25, anchor_x="center")
        arcade.draw_text("OBJETIVO", LARGURA / 2, 400,
                         arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Colete todas as moedas sem encostar nos vilões.",
                         LARGURA / 2, 365, arcade.color.YELLOW_GREEN, 16,
                         anchor_x="center")
        arcade.draw_text("Moeda comum: +1 ponto     Moeda especial: +10 pontos",
                         LARGURA / 2, 335, arcade.color.WHITE, 16,
                         anchor_x="center")
        arcade.draw_text("[I] Instruções   [S] Sobre   [R] Ranking   [J] Jogar   [ESC] Sair",
                         LARGURA / 2, 100, arcade.color.YELLOW, 16,
                         anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.I:
            self.window.show_view(TelaInstrucoes())
        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())
        elif key == arcade.key.R:
            self.window.show_view(TelaRanking())
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
            "Depois de um golpe você pisca e fica imune por 1,5 s.",
        ]
        for indice, texto in enumerate(textos):
            arcade.draw_text(texto, LARGURA / 2, 395 - indice * 38,
                             arcade.color.WHITE, 16, anchor_x="center")
        arcade.draw_text("Pressione ESC para voltar", LARGURA / 2, 90,
                         arcade.color.LIGHT_RED_OCHRE, 18, anchor_x="center")

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
                         arcade.color.WHITE, 22, anchor_x="center")
        arcade.draw_text("Um jogo de coleta e desvio criado com Python e Arcade.",
                         LARGURA / 2, 335, arcade.color.WHITE, 16,
                         anchor_x="center")
        arcade.draw_text("Desvie dos inimigos, colete tudo e faça a maior pontuação!",
                         LARGURA / 2, 295, arcade.color.WHITE, 16,
                         anchor_x="center")
        arcade.draw_text("Pressione ESC para voltar", LARGURA / 2, 90,
                         arcade.color.LIGHT_RED_OCHRE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


class TelaJogo(TelaComFundo):
    def __init__(self):
        super().__init__()
        self.velocidade = VELOCIDADE
        self.pontuacao = 0
        self.tempo_decorrido = 0.0
        self.mensagem = ""

        fundo = self.background_list[0]
        fundo.width = LARGURA + 2 * INTENSIDADE_TREMOR
        fundo.height = ALTURA + 2 * INTENSIDADE_TREMOR

        # Criar jogador
        self.jogador = Player()
        self.jogador.center_x = 50
        self.jogador.center_y = 50
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.jogador)

        # Criar vilões
        self.vilao = Vilao()
        self.vilao.center_x, self.vilao.center_y = 650, 500
        self.vilao.change_x, self.vilao.change_y = self.velocidade, self.velocidade - 1
        self.sprite_vilao = arcade.SpriteList()
        self.sprite_vilao.append(self.vilao)

        self.vilao_especial = VilaoEspecial()
        self.vilao_especial.center_x, self.vilao_especial.center_y = 350, 300
        self.vilao_especial.change_x = -VELOCIDADE_VILAO_ESPECIAL
        self.vilao_especial.change_y = VELOCIDADE_VILAO_ESPECIAL - 1
        self.sprite_vilao_especial = arcade.SpriteList()
        self.sprite_vilao_especial.append(self.vilao_especial)

        # Criando os blocos
        self.sprite_blocos = arcade.SpriteList()
        for x in range(32, LARGURA + 32, 64):
            chao = Bloco(x=x, y=30)
            self.sprite_blocos.append(chao)

        posicoes_plataforma = [(300, 250), (550, 250)]
        for x, y in posicoes_plataforma:
            plataforma = Bloco(x, y)
            self.sprite_blocos.append(plataforma)

        # Física
        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jogador,
            walls=self.sprite_blocos,
            gravity_constant=GRAVIDADE
        )
        self.engine_fisica_vilao_especial = arcade.PhysicsEnginePlatformer(
            player_sprite=self.vilao_especial,
            walls=self.sprite_blocos,
            gravity_constant=GRAVIDADE
        )

        # Criar moedas
        self.sprite_moedas = arcade.SpriteList()
        for _ in range(25):
            moeda = Moeda()
            while True:
                moeda.center_x = random.randint(50, LARGURA - 50)
                moeda.center_y = random.randint(50, ALTURA - 50)
                if not arcade.check_for_collision_with_list(moeda, self.sprite_blocos):
                    break
            self.sprite_moedas.append(moeda)

        self.moedas_especiais = arcade.SpriteList()
        for _ in range(5):
            moeda = MoedaEspecial()
            while True:
                moeda.center_x = random.randint(80, LARGURA - 80)
                moeda.center_y = random.randint(80, ALTURA - 80)
                if not arcade.check_for_collision_with_list(moeda, self.sprite_blocos):
                    break
            moeda.change_x = random.choice([-1, 1]) * self.velocidade
            moeda.change_y = random.choice([-1, 1]) * (self.velocidade - 1)
            self.moedas_especiais.append(moeda)
            self.sprite_moedas.append(moeda)

        # Temporizadores
        self.tempo_invencivel = 0.0
        self.tempo_flash = 0.0
        self.tempo_tremor = 0.0

        # Câmera do mundo
        self.camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()

        # Câmera principal
        self.camera.use()
        self.desenhar_fundo()
        self.sprite_moedas.draw()
        self.sprite_vilao.draw()
        self.sprite_vilao_especial.draw()
        self.sprite_jogador.draw()
        self.sprite_blocos.draw()

        # Câmera padrão da UI/HUD
        self.window.default_camera.use()

        # ** EFEITO VISUAL DE CLARÃO VERMELHO NA TELA **
        if self.tempo_flash > 0:
            alpha = int(120 * self.tempo_flash / TEMPO_FLASH)
            arcade.draw_rect_filled(
                arcade.XYWH(LARGURA / 2, ALTURA / 2, LARGURA, ALTURA),
                (255, 0, 0, alpha)
            )

        # HUD
        arcade.draw_text(f"Moedas Coletadas: {self.pontuacao}", 10, 570,
                         arcade.color.YELLOW, 14)
        arcade.draw_text(f"Tempo: {int(self.tempo_decorrido)}s", LARGURA - 120, 570,
                         arcade.color.YELLOW, 14)
        
        if self.tempo_invencivel > 0:
            arcade.draw_text(self.mensagem, LARGURA / 2, 540, arcade.color.RED, 16,
                             anchor_x="center", bold=True)

    def on_update(self, delta_time):
        self.tempo_decorrido += delta_time
        self.sprite_moedas.update()
        self.sprite_jogador.update(delta_time)
        self.sprite_vilao.update(delta_time)
        self.sprite_vilao_especial.update(delta_time)

        self.engine_fisica.update()
        self.engine_fisica_vilao_especial.update()

        # Colisão com moedas
        for moeda in arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas):
            self.pontuacao += moeda.valor
            if moeda.valor == 10:
                self.velocidade += 0.5
            moeda.remove_from_sprite_lists()

        self.tempo_invencivel = max(0.0, self.tempo_invencivel - delta_time)
        self.tempo_flash = max(0.0, self.tempo_flash - delta_time)
        self.tempo_tremor = max(0.0, self.tempo_tremor - delta_time)

        # ** LÓGICA DE COLISÃO COM VILÕES (SEM EXPLOSÕES ADICIONAIS) **
        if self.tempo_invencivel == 0:
            colisoes = arcade.check_for_collision_with_list(
                self.jogador, self.sprite_vilao)
            colisoes_especiais = arcade.check_for_collision_with_list(
                self.jogador, self.sprite_vilao_especial)

            if colisoes or colisoes_especiais:
                if colisoes_especiais:
                    self.pontuacao -= 3
                    self.mensagem = "A bruxa te atingiu! -3 pontos"
                else:
                    self.pontuacao -= 1
                    self.mensagem = "O vilão te atingiu! -1 ponto"

                # ** TROCA A FADA PARA A TEXTURA DE IMPACTO / TREMIDA **
                self.jogador.tremer()

                self.velocidade = max(VELOCIDADE_MINIMA,
                                      self.velocidade - REDUCAO_VELOCIDADE)
                if self.jogador.change_x > 0:
                    self.jogador.change_x = self.velocidade
                elif self.jogador.change_x < 0:
                    self.jogador.change_x = -self.velocidade

                self.tempo_invencivel = TEMPO_INVENCIVEL
                self.tempo_flash = TEMPO_FLASH
                self.tempo_tremor = TEMPO_TREMOR

        # ** PISCAR DA PERSONAGEM DURANTE A IMUNIDADE **
        if self.tempo_invencivel > 0:
            if int(self.tempo_invencivel * 10) % 2 == 0:
                self.jogador.alpha = 80
            else:
                self.jogador.alpha = 255
        else:
            self.jogador.alpha = 255

        # Tremor de câmera
        if self.tempo_tremor > 0:
            forca = INTENSIDADE_TREMOR * self.tempo_tremor / TEMPO_TREMOR
            self.camera.position = (
                LARGURA / 2 + random.uniform(-forca, forca),
                ALTURA / 2 + random.uniform(-forca, forca),
            )
        else:
            self.camera.position = (LARGURA / 2, ALTURA / 2)

        # Vitória
        if len(self.sprite_moedas) == 0:
            self.window.show_view(TelaVitoria(self.pontuacao, self.tempo_decorrido))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.jogador.change_x = -self.velocidade
        elif key == arcade.key.D:
            self.jogador.change_x = self.velocidade
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())

        if key == arcade.key.RIGHT:
            self.jogador.change_x += self.velocidade
        elif key == arcade.key.LEFT:
            self.jogador.change_x -= self.velocidade

        if key == arcade.key.W or key == arcade.key.SPACE:
            if self.engine_fisica.can_jump():
                self.jogador.change_y = FORCA_PULO

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.jogador.change_x = 0
        if key in (arcade.key.W, arcade.key.S):
            self.jogador.change_y = 0


class TelaVitoria(TelaComFundo):
    def __init__(self, pontuacao_final, tempo_final):
        super().__init__()
        self.pontuacao = pontuacao_final
        self.tempo = float(tempo_final)
        self.nome = ""
        self.salvo = False
        self.id_salvo = None

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text("Fim do Jogo", LARGURA / 2, 440,
                         arcade.color.YELLOW, 24, anchor_x="center")
        arcade.draw_text(f"Sua pontuação foi: {self.pontuacao}", LARGURA / 2, 390,
                         arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text(f"Tempo: {int(self.tempo)}s", LARGURA / 2, 355,
                         arcade.color.WHITE, 18, anchor_x="center")

        if not self.salvo:
            arcade.draw_text("Digite seu nome para o ranking:", LARGURA / 2, 290,
                             arcade.color.WHITE, 16, anchor_x="center")
            arcade.draw_rect_outline(arcade.XYWH(LARGURA / 2, 250, 360, 50),
                                     arcade.color.WHITE, border_width=2)
            arcade.draw_text(self.nome + "_", LARGURA / 2, 250,
                             arcade.color.YELLOW, 22, anchor_x="center",
                             anchor_y="center")
            arcade.draw_text("[ENTER] Salvar     [ESC] Voltar ao menu sem salvar",
                             LARGURA / 2, 170, arcade.color.LIGHT_RED_OCHRE, 14,
                             anchor_x="center")
        else:
            arcade.draw_text("Pontuação salva no ranking!", LARGURA / 2, 290,
                             arcade.color.YELLOW_GREEN, 18, anchor_x="center")
            arcade.draw_text("[J] Jogar novamente   [R] Ranking   [ESC] Menu",
                             LARGURA / 2, 220, arcade.color.LIGHT_RED_OCHRE, 18,
                             anchor_x="center")

    def on_text(self, text):
        if self.salvo:
            return
        if text.isprintable() and len(self.nome) < TAMANHO_MAX_NOME:
            self.nome += text

    def salvar_pontuacao(self) -> Pontuacao:
        nova = Pontuacao.create(
            nome_jogador=self.nome.strip(),
            pontos=self.pontuacao,
            tempo_partida=self.tempo,
        )
        self.salvo = True
        self.id_salvo = nova.id
        return nova

    def on_key_press(self, key, modifiers):
        if not self.salvo:
            if key == arcade.key.BACKSPACE:
                self.nome = self.nome[:-1]
            elif key in (arcade.key.ENTER, arcade.key.NUM_ENTER):
                if self.nome.strip():
                    self.salvar_pontuacao()
            elif key == arcade.key.ESCAPE:
                self.window.show_view(TelaInicial())
            return

        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.R:
            self.window.show_view(TelaRanking(destaque_id=self.id_salvo))
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


class TelaRanking(TelaComFundo):
    def __init__(self, destaque_id: int = None):
        super().__init__()
        self.melhores = buscar_top10()
        self.destaque_id = destaque_id

    def on_draw(self):
        self.clear()
        self.desenhar_fundo()

        arcade.draw_text("TOP 10 - RANKING", LARGURA / 2, 540,
                         arcade.color.YELLOW, 26, anchor_x="center")

        if not self.melhores:
            arcade.draw_text("Nenhuma pontuação ainda! Seja o primeiro.",
                             LARGURA / 2, 300, arcade.color.WHITE, 18,
                             anchor_x="center")
        else:
            y_cab = 490
            arcade.draw_text("POS", 100, y_cab, arcade.color.YELLOW_GREEN, 14)
            arcade.draw_text("NOME", 160, y_cab, arcade.color.YELLOW_GREEN, 14)
            arcade.draw_text("PONTOS", 450, y_cab, arcade.color.YELLOW_GREEN, 14,
                             anchor_x="right")
            arcade.draw_text("TEMPO", 560, y_cab, arcade.color.YELLOW_GREEN, 14,
                             anchor_x="right")
            arcade.draw_text("DATA", 700, y_cab, arcade.color.YELLOW_GREEN, 14,
                             anchor_x="right")

            for i, registro in enumerate(self.melhores):
                y = 450 - i * 34
                if registro.id == self.destaque_id:
                    cor = arcade.color.YELLOW
                else:
                    cor = arcade.color.WHITE

                arcade.draw_text(f"{i + 1}º", 100, y, cor, 16)
                arcade.draw_text(registro.nome_jogador, 160, y, cor, 16)
                arcade.draw_text(str(registro.pontos), 450, y, cor, 16,
                                 anchor_x="right")
                arcade.draw_text(f"{registro.tempo_partida:.1f}s", 560, y, cor, 16,
                                 anchor_x="right")
                arcade.draw_text(registro.data_hora.strftime("%d/%m/%Y"), 700, y,
                                 cor, 16, anchor_x="right")

        arcade.draw_text("[J] Jogar     [ESC] Voltar ao menu", LARGURA / 2, 40,
                         arcade.color.LIGHT_RED_OCHRE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


def executar():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    inicializar_banco()

    janela = arcade.Window(LARGURA, ALTURA, NOME)
    janela.show_view(TelaInicial())
    arcade.run()

    if not db.is_closed():
        db.close()


if __name__ == "__main__":
    executar()