import sys
class ActionError(Exception):
    def __init__(self, message):
        super(Exception)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

class linkedlist:
    def __init__(self):
        self.data = []
        self.head = None
    
    def initializeList(self, data):
        try:
            self.data = []
            for x in data[::-1]:
                n = Node(x)
                if data.index(x) == 0:
                    n.next = None
                    self.data.insert(0, n)
                else:
                    n.next = data[data.index(x) + 1]
                    self.data.insert(0, n)

        except:
            import traceback

            def myexcepthook(type, value, tb):
                l = ''.join(traceback.format_exception(type, value, tb))
                print(l)


            sys.excepthook = myexcepthook
            raise ActionError("Cannot Re-Initialize Existing Linked List. Can erase and append though.")

    def __str__(self):
        m = ""
        for x in self.data:
            if x != self.data[-1]:
                m += str(x) + " --> "

            else:
                m += str(x)

        return m

# Create empty linked list
ll1 = linkedlist()

# Initialize all links and add data
ll1.initializeList([1, 2, 3, 4, 5, 1])
ll1.initializeList([1, 2, 3, 4, 5, 1, 6])
print(ll1)
