import numpy as np


class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        """
        Инициализация нейронной сети.

        :param input_size: Количество входных нейронов.
        :param hidden_size: Количество нейронов в скрытом слое.
        :param output_size: Количество выходных нейронов.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Инициализация весов и смещений
        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size)
        self.bias_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size)
        self.bias_output = np.zeros((1, self.output_size))

    def sigmoid(self, x):
        """
        Сигмоидная функция активации.

        :param x: Входные данные.
        :return: Значение сигмоиды.
        """
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        """
        Производная сигмоидной функции.

        :param x: Входные данные.
        :return: Производная сигмоиды.
        """
        return x * (1 - x)

    def forward(self, X):
        """
        Прямой проход (forward pass).

        :param X: Входные данные.
        :return: Выходные данные сети.
        """
        # Скрытый слой
        self.hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.hidden_output = self.sigmoid(self.hidden_input)

        # Выходной слой
        self.output_input = (
            np.dot(self.hidden_output, self.weights_hidden_output) + self.bias_output
        )
        self.output = self.sigmoid(self.output_input)

        return self.output

    def backward(self, X, y, learning_rate):
        """
        Обратное распространение ошибки (backpropagation).

        :param X: Входные данные.
        :param y: Целевые значения.
        :param learning_rate: Скорость обучения.
        """
        # Ошибка на выходном слое
        output_error = y - self.output
        output_delta = output_error * self.sigmoid_derivative(self.output)

        # Ошибка на скрытом слое
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden_output)

        # Обновление весов и смещений
        self.weights_hidden_output += (
            self.hidden_output.T.dot(output_delta) * learning_rate
        )
        self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
        self.weights_input_hidden += X.T.dot(hidden_delta) * learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        """
        Обучение нейронной сети.

        :param X: Входные данные.
        :param y: Целевые значения.
        :param epochs: Количество эпох.
        :param learning_rate: Скорость обучения.
        """
        for epoch in range(epochs + 1):
            output = self.forward(X)
            self.backward(X, y, learning_rate)

            if epoch % 1000 == 0:
                loss = np.mean(np.square(y - output))
                print(f"Epoch {epoch}, Loss: {loss}")

    def predict(self, X):
        """
        Предсказание на новых данных.

        :param X: Входные данные.
        :return: Предсказанные значения.
        """
        return self.forward(X)


# Пример использования
if __name__ == "__main__":
    # Данные для обучения (XOR)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[1], [0], [1], [0]])

    # Создание и обучение сети
    nn = SimpleNeuralNetwork(input_size=2, hidden_size=4, output_size=1)
    nn.train(X, y, epochs=10000, learning_rate=1)

    # Предсказание
    predictions = nn.predict(X)
    print("Predictions:")
    # print(list(map(lambda el: int(el.round()), predictions)))
    print(predictions)
