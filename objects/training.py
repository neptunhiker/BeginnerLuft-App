class Training:

    def __init__(self, name, cost_per_training_lesson, data_base_id=None):
        self.name = name
        self.cost_per_training_lesson = cost_per_training_lesson
        self.data_base_id = data_base_id

    @classmethod
    def test_training(cls):
        name = "Name der Maßnahme"
        cost_per_training_lesson = 12.34

        return cls(name, cost_per_training_lesson)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.cost_per_training_lesson}, {self.data_base_id})"


if __name__ == '__main__':
    training = Training.test_training()
    print(training)