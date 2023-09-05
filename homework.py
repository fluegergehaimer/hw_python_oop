from dataclasses import dataclass, asdict


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
        return self.MESSAGE.format(**asdict(self))


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
            type(self).__name__,
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
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * (
                self.duration * self.MIN_IN_HOUR
            )
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SPENT_CALORIES_MULTIPIER_1 = 0.035
    SPENT_CALORIES_MULTIPIER_2 = 0.029
    KM_IN_M = 0.278
    CM_IN_M = 100

    height: float

    def get_spent_calories(self) -> float:
        return (
            (
                self.SPENT_CALORIES_MULTIPIER_1 * self.weight
                + (
                    (
                        self.get_mean_speed() * self.KM_IN_M
                    )**2 / (
                        self.height / self.CM_IN_M
                    )
                )
                * self.SPENT_CALORIES_MULTIPIER_2 * self.weight
            ) * (
                self.duration * self.MIN_IN_HOUR
            )
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIMMING_COEFF = 1.1
    SWIMMING_COEFF_2 = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (
                self.get_mean_speed() + self.SWIMMING_COEFF
            )
            * self.SWIMMING_COEFF_2
            * self.weight * self.duration
        )


TRAINING_TYPES = {'RUN': Running,
                  'WLK': SportsWalking,
                  'SWM': Swimming
                  }

CHECK_VALUES = {'RUN': (Running, 3),
                'WLK': (SportsWalking, 4),
                'SWM': (Swimming, 5)
                }

type_error = 'Required data type "string", not {type}.'
value_error = '{workout} - Unsupported type of training.'
attribute_error = 'Invalid number of arguments. Required {quantity}'


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if not isinstance(workout_type, str):
        raise TypeError(type_error.format(type=type(workout_type)))
    elif workout_type not in TRAINING_TYPES:
        raise ValueError(value_error.format(workout=workout_type))
    elif CHECK_VALUES[workout_type] != (
        TRAINING_TYPES[workout_type], len(data)
    ):
        raise ValueError(
            attribute_error.format(quantity=CHECK_VALUES[workout_type][1])
        )

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
