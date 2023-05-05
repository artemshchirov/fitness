import re
import inspect
import types

import pytest
from conftest import Capturing

try:
    import main
except ModuleNotFoundError:
    assert False, 'File `main.py` not found'
except NameError as exc:
    name = re.findall("name '(\w+)' is not defined", str(exc))[0]
    assert False, f'Class {name} not found in the main.py file.'
except ImportError:
    assert False, 'File `main.py` not found'


def test_read_package():
    assert hasattr(main, 'read_package'), (
        'Create a function to handle incoming package - `read_package`'
    )
    assert callable(main.read_package), (
        'Make sure `read_package` is a function.'
    )
    assert isinstance(main.read_package, types.FunctionType), (
        'Make sure `read_package` is a function.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (('SWM', [720, 1, 80, 25, 40]), 'Swimming'),
    (('RUN', [15000, 1, 75]), 'Running'),
    (('WLK', [9000, 1, 75, 180]), 'SportsWalking'),
])
def test_read_package_return(input_data, expected):
    result = main.read_package(*input_data)
    assert result.__class__.__name__ == expected, (
        'Function `read_package` should return a sports type class '
        'depending on the training code.'
    )


def test_InfoMessage():
    assert inspect.isclass(main.InfoMessage), (
        'Make sure `InfoMessage` is a class.'
    )
    info_message = main.InfoMessage
    info_message_signature = inspect.signature(info_message)
    info_message_signature_list = list(info_message_signature.parameters)
    for p in ['training_type', 'duration', 'distance', 'speed', 'calories']:
        assert p in info_message_signature_list, (
            'The `__init__` method of the `InfoMessage` class should have '
            f'the parameter {p}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    (['Swimming', 1, 75, 1, 80],
        'Training type: Swimming; '
        'Duration: 1.000 hr.; '
        'Distance: 75.000 km; '
        'Avg. speed: 1.000 km/hr; '
        'Calories burned: 80.000.'
     ),
    (['Running', 4, 20, 4, 20],
        'Training type: Running; '
        'Duration: 4.000 hr.; '
        'Distance: 20.000 km; '
        'Avg. speed: 4.000 km/hr; '
        'Calories burned: 20.000.'
     ),
    (['SportsWalking', 12, 6, 12, 6],
        'Training type: SportsWalking; '
        'Duration: 12.000 hr.; '
        'Distance: 6.000 km; '
        'Avg. speed: 12.000 km/hr; '
        'Calories burned: 6.000.'
     ),
])
def test_InfoMessage_get_message(input_data, expected):
    info_message = main.InfoMessage(*input_data)
    assert hasattr(info_message, 'get_message'), (
        'Create the `get_message` method in the `InfoMessage` class.'
    )
    assert callable(info_message.get_message), (
        'Ensure that `get_message` in the `InfoMessage` class is a method.'
    )
    result = info_message.get_message()
    assert isinstance(result, str), (
        'The `get_message` method in the `InfoMessage` class '
        'should return a value of type `str`'
    )
    assert result == expected, (
        'The `get_message` method of the `InfoMessage` class should '
        'return a string.\n'
        'For example: \n'
        'Training type: Swimming; '
        'Duration: 1.000 hr.; '
        'Distance: 75.000 km; '
        'Avg. speed: 1.000 km/hrr; '
        'Calories burned: 80.000.'
    )


def test_Training():
    assert inspect.isclass(main.Training), (
        'Ensure that `Training` is a class.'
    )
    training = main.Training
    training_signature = inspect.signature(training)
    training_signature_list = list(training_signature.parameters)
    for param in ['action', 'duration', 'weight']:
        assert param in training_signature_list, (
            'The `__init__` method of the `Training` class '
            f'should have the parameter {param}.'
        )
    assert 'LEN_STEP' in list(training.__dict__), (
        'Set the `LEN_STEP` attribute in the `Training` class'
    )
    assert training.LEN_STEP == 0.65, (
        'The length of a step in the `Training` class should be 0.65'
    )
    assert 'M_IN_KM' in list(training.__dict__), (
        'Set the `M_IN_KM` attribute in the `Training` class'
    )
    assert training.M_IN_KM == 1000, (
        'In the `Training` class, specify the correct '
        'number of meters in a kilometer: 1000'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.273),
    ([1206, 12, 6], 0.7838999999999999),
])
def test_Training_get_distance(input_data, expected):
    training = main.Training(*input_data)
    assert hasattr(training, 'get_distance'), (
        'Create the `get_distance` method in the `Training` class.'
    )
    result = training.get_distance()
    assert type(result) == float, (
        'The `get_distance` method in the `Training` class '
        'should return a value of type `float`'
    )
    assert result == expected, (
        'Check the distance calculation formula in the `Training` class'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.06825),
    ([1206, 12, 6], 0.065325),
])
def test_Training_get_mean_speed(input_data, expected):
    training = main.Training(*input_data)
    assert hasattr(training, 'get_mean_speed'), (
        'Create the `get_mean_speed` method in the `Training` class.'
    )
    result = training.get_mean_speed()
    assert type(result) == float, (
        'The `get_mean_speed` method in the `Training` class'
        'should return a `float` value'
    )
    assert result == expected, (
        'Check the formula for calculating the average movement speed'
        'in the `Training` class'
    )


@pytest.mark.parametrize('input_data', [
    ([9000, 1, 75]),
    ([420, 4, 20]),
    ([1206, 12, 6]),
])
def test_Training_get_burned_calories(input_data):
    training = main.Training(*input_data)
    assert hasattr(training, 'get_burned_calories'), (
        'Create the `get_burned_calories` method in the `Training` class.'
    )
    assert callable(training.get_burned_calories), (
        'Make sure `get_burned_calories` is a function.'
    )


def test_Training_show_training_info(monkeypatch):
    training = main.Training(*[720, 1, 80])
    assert hasattr(training, 'show_training_info'), (
        'Create the `show_training_info` method in the `Training` class.'
    )

    def mock_get_burned_calories():
        return 100
    monkeypatch.setattr(
        training,
        'get_burned_calories',
        mock_get_burned_calories
    )
    result = training.show_training_info()
    assert result.__class__.__name__ == 'InfoMessage', (
        'The `show_training_info` method of the `Training` class'
        'should return an object of the `InfoMessage` class.'
    )


def test_Swimming():
    assert hasattr(main, 'Swimming'), 'Create the `Swimming` class'
    assert inspect.isclass(main.Swimming), (
        'Make sure `Swimming` is a class.'
    )
    assert issubclass(main.Swimming, main.Training), (
        'The `Swimming` class should inherit from the `Training` class.'
    )
    swimming = main.Swimming
    swimming_signature = inspect.signature(swimming)
    swimming_signature_list = list(swimming_signature.parameters)
    for param in ['action', 'duration', 'weight', 'length_pool', 'count_pool']:
        assert param in swimming_signature_list, (
            'The `__init__` method of the `Swimming` class'
            f' must have the {param} parameter.'
        )
    assert 'LEN_STEP' in list(swimming.__dict__), (
        'Set the `LEN_STEP` attribute in the `Swimming` class'
    )
    assert swimming.LEN_STEP == 1.38, (
        'The length of a stroke in the `Swimming` class should be 1.38'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 1.0),
    ([420, 4, 20, 42, 4], 0.042),
    ([1206, 12, 6, 12, 6], 0.005999999999999999),
])
def test_Swimming_get_mean(input_data, expected):
    swimming = main.Swimming(*input_data)
    result = swimming.get_mean_speed()
    assert result == expected, (
        'Override the `get_mean_speed` method in the `Swimming` class. '
        'Check the formula '
        'for calculating the average speed in the `Swimming` class.'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 336.0),
    ([420, 4, 20, 42, 4], +45.68000000000001),
    ([1206, 12, 6, 12, 6], 13.272000000000002),
])
def test_Swimming_get_burned_calories(input_data, expected):
    swimming = main.Swimming(*input_data)
    result = swimming.get_burned_calories()
    assert type(result) == float, (
        'Override the `get_burned_calories` method in the `Swimming` class.'
    )
    assert result == expected, (
        'Check the formula for calculating the burned calories in '
        'the `Swimming` class.'
    )


def test_SportsWalking():
    assert hasattr(
        main, 'SportsWalking'), 'Create the `SportsWalking` class.'
    assert inspect.isclass(main.SportsWalking), (
        'Check that `SportsWalking` is a class.'
    )
    assert issubclass(main.SportsWalking, main.Training), (
        'The `SportsWalking` class should inherit from the `Training` class.'
    )
    sports_walking = main.SportsWalking
    sports_walking_signature = inspect.signature(sports_walking)
    sports_walking_signature_list = list(sports_walking_signature.parameters)
    for param in ['action', 'duration', 'weight', 'height']:
        assert param in sports_walking_signature_list, (
            'The `SportsWalking` class `__init__` method '
            f'should have the parameter {param}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75, 180], 157.50000000000003),
    ([420, 4, 20, 42], 168.00000000000003),
    ([1206, 12, 6, 12], 151.20000000000002),
])
def test_SportsWalking_get_burned_calories(input_data, expected):
    sports_walking = main.SportsWalking(*input_data)
    result = sports_walking.get_burned_calories()
    assert type(result) == float, (
        'Override the `get_burned_calories` method in '
        'the `SportsWalking` class.'
    )
    assert result == expected, (
        'Check the formula for calculating the burned calories in '
        'the `SportsWalking` class.'
    )


def test_Running():
    assert hasattr(main, 'Running'), 'Create the `Running` class.'
    assert inspect.isclass(main.Running), (
        'Check that `Running` is a class.'
    )
    assert issubclass(main.Running, main.Training), (
        'The `Running` class should inherit from the `Training` class.'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 383.84999999999997),
    ([420, 4, 20], -90.1032),
    ([1206, 12, 6], -81.320328),
])
def test_Running_get_burned_calories(input_data, expected):
    running = main.Running(*input_data)
    assert hasattr(running, 'get_burned_calories'), (
        'Create the `get_burned_calories` method in the `Running` class.'
    )
    result = running.get_burned_calories()
    assert type(result) == float, (
        'Override the `get_burned_calories` method in the `Running` class.'
    )
    assert result == expected, (
        'Check the formula for calculating burned calories in '
        'the `Running` class.'
    )


def test_main():
    assert hasattr(main, 'main'), (
        'Create the main program function named `main`.'
    )
    assert callable(main.main), 'Check that `main` is a function.'
    assert isinstance(main.main, types.FunctionType), (
        'Check that `main` is a function.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (['SWM', [720, 1, 80, 25, 40]], [
        'Training type: Swimming; '
        'Duration: 1.000 hr.; '
        'Distance: 0.994 km; '
        'Avg. speed: 1.000 km/hr; '
        'Calories burned: 336.000.'
    ]),
    (['RUN', [1206, 12, 6]], [
        'Training type: Running; '
        'Duration: 12.000 hr.; '
        'Distance: 0.784 km; '
        'Avg. speed: 0.065 km/hr; '
        'Calories burned: -81.320.'
    ]),
    (['WLK', [9000, 1, 75, 180]], [
        'Training type: SportsWalking; '
        'Duration: 1.000 hr.; '
        'Distance: 5.850 km; '
        'Avg. speed: 5.850 km/hr; '
        'Calories burned: 157.500.'
    ])
])
def test_main_output(input_data, expected):
    with Capturing() as get_message_output:
        training = main.read_package(*input_data)
        main.main(training)
    assert get_message_output == expected, (
        'The `main` method should print the result to the console.\n'
    )
