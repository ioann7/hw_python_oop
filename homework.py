"""
Модуль фитнес-трекера, который обрабатывает
данные для трех видов тренировок:
для бега, спортивной ходьбы и плавания.
"""


from typing import Union, Type, Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить информационное сообщение."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    SECONDS_IN_MIN: int = 60
    COEFF_CALLORIE_1: Union[int, float]
    COEFF_CALLORIE_2: Union[int, float]

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = int(action)
        self.duration = float(duration)
        self.weight = float(weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())

    def get_duration_in_minutes(self) -> float:
        """Получить время тренировки в минутах."""
        return self.duration * self.SECONDS_IN_MIN


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALLORIE_1 = 18
    COEFF_CALLORIE_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = self.COEFF_CALLORIE_1
        coeff_2 = self.COEFF_CALLORIE_2
        return ((coeff_1 * self.get_mean_speed() - coeff_2)
                * self.weight
                / self.M_IN_KM
                * self.get_duration_in_minutes())

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            'Running', self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALLORIE_1 = 0.035
    COEFF_CALLORIE_2 = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = float(height)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = self.COEFF_CALLORIE_1
        coeff_2 = self.COEFF_CALLORIE_2
        left_multiplier = (coeff_1
                           * self.weight
                           + (self.get_mean_speed()**2 // self.height)
                           * coeff_2)
        return left_multiplier * self.get_duration_in_minutes()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            'SportsWalking', self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEFF_CALLORIE_1 = 1.1
    COEFF_CALLORIE_2 = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = float(length_pool)
        self.count_pool = float(count_pool)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = self.COEFF_CALLORIE_1
        coeff_2 = self.COEFF_CALLORIE_2
        return ((self.get_mean_speed() + coeff_1)
                * coeff_2
                * self.weight)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            'Swimming', self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return workout_types[workout_type](*data)
    except KeyError as e:
        print(f'This type of workout "{workout_type}" is not supported.')
        raise KeyError(e)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
