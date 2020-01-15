from numpy.random import uniform, exponential, random_sample


class UniformGenerator:
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def generate(self):
        return uniform(self._a, self._b)


class ExponentialGenerator:
    def __init__(self, lambd):
        self._betta = 1 / lambd

    def generate(self):
        return exponential(self._betta)


class Modeller:
    def __init__(self, uniform_a, uniform_b, expo_lambda, reenter_prop, req_count, dt):
        self._generator = UniformGenerator(uniform_a, uniform_b)
        self._processor = ExponentialGenerator(expo_lambda)
        self._reenter_prob = reenter_prop
        self._req_count = req_count
        self.dt = dt

        self._queue_size = 0
        self._max_queue_size = 0
        self._processed_requests = 0
        self._reentered_requests = 0

    def add_to_queue(self):
        self._queue_size += 1
        if self._queue_size > self._max_queue_size:
            self._max_queue_size += 1

    def process(self):
        if self._queue_size == 0:
            return 0

        self._queue_size -= 1
        self._processed_requests += 1

        if random_sample() < self._reenter_prob:
            self._reentered_requests += 1
            self.add_to_queue()
        return 1

    def time_based_modelling(self):
        generator = self._generator
        processor = self._processor

        time_to_appear = generator.generate()
        time_to_process = time_to_appear + processor.generate()
        curr_time = 0
        while self._processed_requests < self._req_count:
            if curr_time >= time_to_appear:
                self.add_to_queue()
                time_to_appear += generator.generate()
            if curr_time >= time_to_process:
                self.process()
                if self._queue_size > 0:
                    time_to_process += processor.generate()
                else:
                    time_to_process = time_to_appear + processor.generate()
            curr_time += self.dt

        return (self._processed_requests, self._reentered_requests, self._max_queue_size, curr_time)

    def event_based_modelling(self):
        generator = self._generator
        processor = self._processor

        time_to_appear = generator.generate()
        time_to_process = time_to_appear + processor.generate()
        while self._processed_requests < self._req_count:
            if time_to_appear <= time_to_process:
                self.add_to_queue()
                time_to_appear += generator.generate()
            if time_to_appear >= time_to_process:
                self.process()
                if self._queue_size > 0:
                    time_to_process += processor.generate()
                else:
                    time_to_process = time_to_appear + processor.generate()

        return (self._processed_requests, self._reentered_requests, self._max_queue_size, time_to_process)



print(uniform(0.1, 5.6))