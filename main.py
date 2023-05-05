from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Information message about training."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO: str = ('Training type: {training_type}; '
                 'Duration: {duration:.3f} hr.; '
                 'Distance: {distance:.3f} km; '
                 'Avg. speed: {speed:.3f} km/hr; '
                 'Calories burned: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFO.format(**asdict(self))


class Training:
    """Base class for training."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    M_TO_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in kilometers."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average movement speed."""
        distance = self.get_distance()
        return distance / self.duration

    def get_burned_calories(self) -> float:
        """Get the amount of calories spent."""
        raise NotImplementedError('unexpectedly not implemented')

    def show_training_info(self) -> InfoMessage:
        """Return an information message about the completed training."""
        distance = self.get_distance()
        spent_calories = self.get_burned_calories()
        speed_km_h = self.get_mean_speed()
        training_type = self.__class__.__name__

        return InfoMessage(training_type,
                           self.duration,
                           distance,
                           speed_km_h,
                           spent_calories)


class Running(Training):
    """Training: Running."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_burned_calories(self) -> float:
        mean_speed_kmh = self.get_mean_speed()
        calories_from_speed = (self.CALORIES_MEAN_SPEED_MULTIPLIER
                               * mean_speed_kmh
                               - self.CALORIES_MEAN_SPEED_SHIFT)
        calories_from_distance = (self.weight / Training.M_IN_KM
                                  * self.duration * Training.M_TO_HOUR)
        burned_calories = calories_from_speed * calories_from_distance

        return burned_calories


class SportsWalking(Training):
    """Training: Sports walking."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_burned_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        burned_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                            + (mean_speed ** 2 // self.height)
                            * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                           * self.duration * self.M_TO_HOUR)

        return burned_calories


class Swimming(Training):
    """Training: Swimming."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        distance = self.length_pool * self.count_pool / Training.M_IN_KM
        return distance / self.duration

    def get_burned_calories(self):
        speed_kmh = self.get_mean_speed()
        burned_calories = ((speed_kmh + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                           * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)

        return burned_calories


def read_package(workout_type: str, data: list) -> Training:
    """Read data received from sensors."""
    training_types = {'SWM': Swimming,
                      'WLK': SportsWalking,
                      'RUN': Running}

    try:
        training_type = training_types[workout_type]
    except KeyError:
        print('Invalid workout type:', workout_type)
        return None

    try:
        return training_type(*data)
    except TypeError:
        print('Incorrect number of data items')
        return None


def main(training: Training) -> None:
    """Main function."""
    try:
        info = training.show_training_info()
    except AttributeError:
        print('Attribute Error')
    else:
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
