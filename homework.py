from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Выводит данные информационного сообщения.

        Returns:
            Строку параметров информационного сообщения.
        """
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Рассчитывает дистанцию.

        Returns:
            Дистанцию в километрах, рассчитанную по
            произведению количества действий и длины шага за это действие.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю скорость движения.

        Returns:
            Значение средней скорости движения, рассчитанное в результате
            деления пройденной дистанции на время тренировки.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Рассчитывает количество затраченных калорий.

        Raises:
            NotImplementedError: Если наследник не переопределил
                метод получения калорий.
        """
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Формирует информационное сообщение о выполненной тренировке.

        Returns:
            Информационное сообщение о тренировке -
            объект класса InfoMessage.
        """
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_RUNNING_MULTIPLIER = 18
    CALORIES_RUNNING_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_RUNNING_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_RUNNING_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278  # 1000 метров / 60 минут в секундах
    CM_IN_M = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + (
                (
                    (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
        ) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


class InvalidInputDataError(Exception):
    pass


WORKOUT_TYPES = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming,
}


def read_package(workout_type: str, data: List[float]) -> Training:
    """Считывает данные полученные от датчиков.

    Args:
        workout_type: код тренировки, представляющий собой строку из
            из трех букв в верхнем регистре.
        data: [количество действий, время тренировки в часах,
            вес пользователя, рост пользователя(опционально) или
            длина бассейна, сколько раз пользователь переплыл бассейн
            (опционально)].

    Returns:
        Объект одного из трех классов тренировки, наследуемых от Training.
    """
    try:
        return WORKOUT_TYPES[workout_type](*data)
    except (KeyError, TypeError) as err:
        raise InvalidInputDataError(err)


def main(training: Training) -> None:
    """Главная функция.

    Args:
        training: Объект одного из трех классов тренировки.
    """
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
