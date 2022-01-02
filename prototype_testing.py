

class Foo:

    def does_it_exidst(self):
        print("yo")



if __name__ == '__main__':
    method = getattr(Foo, "does_it_exist", None)
    if callable(method):
        print("yes")
    else:
        print("no")