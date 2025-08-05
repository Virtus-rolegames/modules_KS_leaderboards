import asyncio
from typing import List

from immitators import send_message as send_message
from immitators import User as User


class Leaderboard:
    """
    Класс с помощью которого, реализован основной функционал. При создании ест список Users. Каждый user должен быть
    экземпляром класса User и иметь следующие параметры:
    user_id - тг id для отправки сообщения
    win_points - победные очки игрока
    username - отображаемое имя игрока

    Используется функция leaders.send().
    """
    def __init__(self, users):
        self.scores = []
        self.users: List[User] = users

    def _calc(self):
        buf = {}
        for user in self.users:
            buf[user] = user.win_points
        self.scores = sorted(buf.items(), key=lambda item: item[1], reverse=True)

    async def send(self, final: bool = False):
        """
        Функция отправки сообщений с рейтингом. Вроде бы сразу адаптировал под aiogram по синтаксису
            Обычное сообщение:
                Вы занимаете 3 место.
            Сообщение с final = True:
                Игрок Bob занимает 1 место. Итоговый счет: 11
                Игрок Eva занимает 2 место. Итоговый счет: 9
                Игрок Alice занимает 3 место. Итоговый счет: 5
        :param final: По дефолту False. Если получит True, отправит всем users полную таблицу
        :return: Ничего не возвращает
        """
        self._calc()
        for user in self.users:
            if final:
                text = ""
                for i, (player, win_points) in enumerate(self.scores, start=1):
                    text += f"Игрок {player.username} занимает {i} место. Итоговый счет: {win_points}\n"
            else:
                place = "Ошибка игрок не найден"
                score = "Ошибка игрок не найден"
                for i, (player, win_points) in enumerate(self.scores, start=1):
                    if player == user:
                        place = i
                        #score = self.scores[place-1]
                text = f"Вы занимаете {place} место."
                #\nВаш текущий счёт: {score[1]}
            await send_message(user.user_id, text=text)


async def test():
    user_a = User(user_id="a", win_points=5, username="Alice")
    user_b = User(user_id="b", win_points=11, username="Bob")
    user_c = User(user_id="c", win_points=9, username="Eva")
    users = [user_a, user_b, user_c]
    leaders = Leaderboard(users)
    await leaders.send()
    await leaders.send(True)


if __name__ == "__main__":
    asyncio.run(test())
