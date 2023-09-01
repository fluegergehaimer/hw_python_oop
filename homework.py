class InfoMessage:
    """Информационное сообщение о тренировке."""

    def _init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {training.__class__.__name__}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    DURATION_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return Training.get_distance(self) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        
        return InfoMessage.get_message(self)

class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration:
                 float, weight: float) -> None:
        super().__init__(action, duration, weight)


    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.DURATION_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035
    K_2 = 0.029

    def __init__(self, action: int, duration:
                 float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = super().get_distance()
        self.speed = super().get_mean_speed

    def get_spent_calories(self) -> float:
        return (((self.K_1 * self.weight
                  + (self.get_mean_speed()**2 / self.height) * self.K_2
                  * self.weight) * (self.duration * self.DURATION_MIN)))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    K_1 = 1.1
    K_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(self, action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / (self.duration * self.DURATION_MIN))

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.K_1) * self.K_2 * self.weight
                * self.duration * self.DURATION_MIN)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    TRAINING_TYPES = {'RUN': Running,
                      'WLK': SportsWalking,
                      'SWM': Swimming
                      }
    
    return TRAINING_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        #('SWM', [720, 1, 80, 25, 40]),
       # ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
