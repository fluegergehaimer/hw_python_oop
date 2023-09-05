from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESSAGE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    action: int
    duration: float
    weight: float

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

        return InfoMessage(
            self.__class__.__name__,
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SPENT_CALORIES_MULTIPIER_1 = 0.035
    SPENT_CALORIES_MULTIPIER_2 = 0.029
    KM_HOURS_TO_M_SECONDS = 0.278
    CM_IN_M = 100

    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.SPENT_CALORIES_MULTIPIER_1 * self.weight
             + ((self.get_mean_speed() * self.KM_HOURS_TO_M_SECONDS)**2
                / (self.height / self.CM_IN_M))
                * self.SPENT_CALORIES_MULTIPIER_2 * self.weight)
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWM_SPENT_CALORIES_MULTIPIER_1 = 1.1
    SWM_SPENT_CALORIES_MULTIPIER_2 = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWM_SPENT_CALORIES_MULTIPIER_1)
            * self.SWM_SPENT_CALORIES_MULTIPIER_2
            * self.weight * self.duration
        )


TRAINING_TYPES = {'RUN': Running,
                  'WLK': SportsWalking,
                  'SWM': Swimming
                  }


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAINING_TYPES:
        raise TypeError('Unsupported training type.')
    elif workout_type == 'SWM' and len(data) != 5:
        raise ValueError('Invalid number of arguments')
    elif workout_type == 'RUN' and len(data) != 3:
        raise ValueError('Invalid number of arguments')
    elif workout_type == 'WLK' and len(data) != 4:
        raise ValueError('Invalid number of arguments')
    return TRAINING_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
