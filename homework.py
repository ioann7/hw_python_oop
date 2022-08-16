"""
Модуль фитнес-трекера, который обрабатывает
данные для трех видов тренировок:
для бега, спортивной ходьбы и плавания.
"""


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить информационное сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage('Training', self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())

    def get_duration_in_minutes(self) -> float:
        """Получить время тренировки в минутах."""
        return self.duration * 60


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 18
        coeff_2 = 20
        dur_in_min = self.get_duration_in_minutes()
        left_mul = (coeff_1 * self.get_mean_speed() - coeff_2)
        return left_mul * self.weight / self.M_IN_KM * dur_in_min

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            'Running', self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = float(height)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 0.035
        coeff_2 = 0.029
        dur_in_min = self.get_duration_in_minutes()
        internal_mul = (self.get_mean_speed()**2 // self.height)
        external_mul = (coeff_1 * self.weight + internal_mul * coeff_2)
        return external_mul * dur_in_min

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            'SportsWalking', self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = float(length_pool)
        self.count_pool = float(count_pool)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 1.1
        coeff_2 = 2
        first_mul = (self.get_mean_speed() + coeff_1)
        return first_mul * coeff_2 * self.weight

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            'Swimming', self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_types[workout_type](*data)


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
