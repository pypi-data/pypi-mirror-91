

def kotok(a):
    print("SDf")
    return a,


class A:
    
    def predict(self):
        print("predict")
        self.init_net()


class B(A):
    
    def init_net(self):
        print("init_net")


if __name__ == '__main__':
    b = B()
    b.predict()