from abc import ABC, abstractmethod
from google.adk.agents import Agent


# ======================
# Абстракція
# ======================

class Exercise(ABC):

    def __init__(self, name: str, duration_min: int):
        self.name = name
        self.duration_min = duration_min

    @abstractmethod
    def calories_burned(self) -> float:
        pass


# ======================
# Наслідування
# ======================

class CardioExercise(Exercise):

    def __init__(self, name: str, duration_min: int, intensity: float):
        super().__init__(name, duration_min)
        self.intensity = intensity

    def calories_burned(self) -> float:
        return self.duration_min * 8 * self.intensity


class StrengthExercise(Exercise):

    def __init__(self, name: str, duration_min: int, weight_kg: float):
        super().__init__(name, duration_min)
        self.weight_kg = weight_kg

    def calories_burned(self) -> float:
        return self.duration_min * 5 + self.weight_kg * 0.5


# ======================
# Інкапсуляція
# ======================

class Workout:

    def __init__(self):
        self.__exercises = []

    def add(self, exercise: Exercise):
        self.__exercises.append(exercise)

    def total_calories(self) -> float:
        return sum(ex.calories_burned() for ex in self.__exercises)

    def summary(self) -> dict:

        exercises = []

        for ex in self.__exercises:
            exercises.append(
                {
                    "name": ex.name,
                    "duration_min": ex.duration_min,
                    "calories": round(ex.calories_burned(), 2)
                }
            )

        return {
            "exercises": exercises,
            "total_calories": round(self.total_calories(), 2)
        }


# ======================
# Tool
# ======================

def calculate_workout(exercises: list) -> dict:

    workout = Workout()

    for item in exercises:

        exercise_type = item.get("type")

        if exercise_type == "cardio":

            exercise = CardioExercise(
                item["name"],
                item["duration_min"],
                item["intensity"]
            )

        elif exercise_type == "strength":

            exercise = StrengthExercise(
                item["name"],
                item["duration_min"],
                item["weight_kg"]
            )

        else:
            continue

        workout.add(exercise)

    return workout.summary()


# ======================
# AI Agent
# ======================

root_agent = Agent(
    name="fitness_trainer",
    model="gemini-2.0-flash",
    description="Персональний фітнес-тренер",
    instruction="""
Ти персональний фітнес-тренер.

Твої завдання:

- розраховувати кількість спалених калорій;
- аналізувати тренування;
- рекомендувати навантаження;
- пояснювати результати.

Завжди відповідай українською мовою.
""",
    tools=[calculate_workout]
)
