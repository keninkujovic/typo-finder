class TSTNode:
    def __init__(self, char):
        self.character = char
        self.left = None
        self.middle = None
        self.right = None
        self.isWordEnd = False

class TST:
    def __init__(self):
        self.root = None

    def insert(self, word):
        self.root = self._insert(self.root, word, 0)

    def _insert(self, node, word, index):
        if node is None:
            node = TSTNode(word[index])

        char = word[index]

        if char < node.character:
            node.left = self._insert(node.left, word, index)
        elif char > node.character:
            node.right = self._insert(node.right, word, index)
        elif index < len(word) - 1:
            node.middle = self._insert(node.middle, word, index + 1)
        else:
            node.isWordEnd = True

        return node

    def search(self, word):
        node = self._search(self.root, word, 0)
        return node is not None and node.isWordEnd

    def _search(self, node, word, index):
        if node is None:
            return None

        char = word[index]

        if char < node.character:
            return self._search(node.left, word, index)
        elif char > node.character:
            return self._search(node.right, word, index)
        elif index < len(word) - 1:
            return self._search(node.middle, word, index + 1)
        else:
            return node

def loadDictionary(tst, filename):
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip()
            tst.insert(word)

def findTypos(tst, text):
    words = set(text.split())
    typos = [word for word in words if not tst.search(word)]
    return typos

def main():
    tst = TST()
    loadDictionary(tst, "dictionary.txt")

    with open('input.txt') as f: input_text = f.read()
    typos = findTypos(tst, input_text)
    print(typos)

if __name__ == "__main__":
    main()

