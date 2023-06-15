class a():
    def __init__(self):
        super().__init__()
        self.list_1 = [0, 1, 2]
        self.list_2 = [3, 4, 5]
        for i in range(1, 3):
            # print(eval(f'self.list_{i}'))
            # print(getattr(self, f'list_{i}'))
            setattr(self, f'list_{i}', [i, i, i])
            print(getattr(self, f'list_{i}'))


a()
# for i in range(1, 3):
#     setattr(a, f'list_{i}', [i, i, i])
#     print(getattr(a, f'list_{i}'))
    # print(getattr(a(), f'list_{i}'))