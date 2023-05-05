# Module for calculating and displaying full information about workouts based on data from sensor block

## Task

Implement a software module using OOP methodology to calculate and display information
about the past workout based on data from the sensor block.

## Base class

```python
class Training
```

### Class properties

- `action` - the main action during the workout (step - running, walking; stroke - swimming);
- `duration` - workout duration;
- `weight` - athlete's weight;
- `M_IN_KM` = 1000 - constant for converting values from meters to kilometers. Its value is 1000.
- `LEN_STEP` - the distance the athlete covers in one step or stroke. One step is 0.65 meters, one stroke
  when swimming is 1.38 meters.

### Class methods

- `get_distance()` - method returns the distance covered during the workout

```python
# basic calculation formula
step * LEN_STEP / M_IN_KM
```

- `get_mean_speed()` - method returns the average movement speed during the workout

```python
# basic calculation formula
distance / duration
```

- `get_burned_calories()` - method returns the number of calories burned
- `show_training_info()` - method returns an object of the message class

## Subclasses

Running workout class

```python
class Running
```

### Class properties

Inherited properties

### Class methods

Override method:

- `get_burned_calories()` - method returns the number of calories burned

```python
# calculation formula
(18 * average_speed - 20) * athlete_weight / M_IN_KM * workout_time_in_minutes
```

---

### Sports walking class

```python
class SportsWalking
```

### Class properties

Added properties:

- height

### Class methods

Override method:

- `get_burned_calories()` - method returns the number of calories burned

```python
# calculation formula
(18 * average_speed - 20) * athlete_weight / M_IN_KM * workout_time_in_minutes
```

---

Swimming workout class

```python
class Swimming
```

### Class properties

Added properties:

- length_pool - pool length
- count_pool - number of pools swam

### Class methods

Override method:

- `get_mean_speed()` - method returns the average movement speed during the workout

```python
# calculation formula
pool_length * count_pool / M_IN_KM / workout_time
```

- `get_burned_calories()` - method returns the number of calories burned.

```python
# формула расчета
(скорость + 1.1) * 2 * вес
```

## Information Message Class

```python
class InfoMessage
```

### Class Properties

- `training_type` - type of training
- `duration` - training duration
- `distance` - distance covered during training
- `speed` - average movement speed during training
- `calories` - kilocalories burned during training

### Class Methods

- `get_message()` - method returns a message string:

```python
# output message
# all float values are rounded to 3 decimal places
'Training type: {training_type}; Duration: {duration} h.; Distance: {distance} km; Avg. speed: {speed} km/h; Calories burned: {calories}'.
```

## Module Functions

```python
def read_package
```

- The `read_package` function takes the training code and a list of its parameters as input.
- The function should determine the type of training and create an object of the corresponding class,
  passing it the parameters obtained in the second argument. This object should be returned by the function.

---

```python
def main(training)
```

The `main()` function should take an instance of the Training class as input.

- When executing the `main()` function, the `show_training_info()` method should be called for this instance;
  the result of the method execution should be an object of the `InfoMessage` class, which should be saved in the info variable.
- For the `InfoMessage` object saved in the `info` variable, a method should be called,
  which returns a message string with data about the training; this string should be passed to the print() function.

## Installation Instructions

**_- Clone the repository:_**

```bash
git clone https://github.com/artemshchirov/hw_python_oop.git
```

**_- Install and activate a virtual environment:_**

- For Linux and MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

- For Windows

```bash
python -m venv venv
source venv/Scripts/activate

```

**_- Install dependencies from requirements.txt file:_**

```bash
pip install -r requirements.txt
```
