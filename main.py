from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random

class GameBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    ball_type = StringProperty('yellow')

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class GamePaddle(Widget):
    def on_touch_move(self, touch):
        if touch.y < self.parent.height / 3:
            self.center_x = touch.x

class CatchGame(Widget):
    ball = ObjectProperty(None)
    paddle = ObjectProperty(None)
    score = NumericProperty(0)
    highscore = NumericProperty(0)
    lives = NumericProperty(3)
    game_over_text = StringProperty("")

    def start_game(self):
        self.score = 0
        self.lives = 3
        self.game_over_text = ""
        self.ball.opacity = 1
        self.reset_ball()

    def reset_ball(self):
        if self.lives <= 0:
            return
        self.ball.center_y = self.height - 50
        self.ball.center_x = random.randint(50, self.width - 250)

        rand = random.random()
        if rand < 0.6:
            self.ball.ball_type = 'yellow'
        elif rand < 0.8:
            self.ball.ball_type = 'red'
        else:
            self.ball.ball_type = 'green'

        speed = -4 - (max(0, self.score) * 0.3)
        self.ball.velocity = (0, speed)

    def update(self, dt):
        if self.lives <= 0:
            self.game_over_text = "ИГРА ОКОНЧЕНА!\nКликните для рестарта"
            self.ball.opacity = 0 # Прячем шарик, когда игра закончена
            return

        self.ball.move()

        # Поймали ракеткой
        if self.ball.collide_widget(self.paddle) and self.ball.velocity_y < 0:
            if self.ball.ball_type == 'yellow':
                self.score += 1
            elif self.ball.ball_type == 'red':
                self.score -= 3
            elif self.ball.ball_type == 'green':
                self.score += 3

            if self.score > self.highscore:
                self.highscore = self.score

            # Если упали ниже -5 очков, забираем жизнь и обнуляем счет
            if self.score <= -5:
                self.lives -= 1
                self.score = 0

            self.reset_ball()

        # Шарик упал на пол
        if self.ball.y < 0:
            if self.ball.ball_type != 'red': # За красные жизнь на полу не теряем
                self.lives -= 1
            self.reset_ball()

    def on_touch_down(self, touch):
        if self.lives <= 0:
            self.start_game()

class CatchApp(App):
    def build(self):
        game = CatchGame()
        Clock.schedule_once(lambda dt: game.start_game(), 0.1)
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    CatchApp().run()