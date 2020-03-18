import sys
from collections import Counter
import heapq
import unittest

class MinHeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding: 
    def __init__(self):
        self.MinHeap = []
        self.tree = {}
        self.invertedTree = {}

    def buildHeap(self, data):
        counterData = self.getCounterdata(data)
        if (len(counterData) == 1):
            #Skip Heap as 2 elements needed
            #Jump directly to huffman's coding
            char = counterData[0][0]
            freq = counterData[0][1]
            self.tree[char] = '0'
            self.invertedTree['0'] = char
            return

        for entry in counterData:
            # print("Entry", entry)
            char = entry[0]
            freq = entry[1]
            newNode = MinHeapNode(char, freq)
            heapq.heappush(self.MinHeap, newNode)
        
        # print("Len of Min Heap: ", len(self.MinHeap))
        self.mergeFreqNodes()

    def getCounterdata(self, data):
        return Counter(data).most_common()

    def mergeFreqNodes(self):
        while (len(self.MinHeap) > 1):
            node1 = heapq.heappop(self.MinHeap)
            node2 = heapq.heappop(self.MinHeap)

            merged = MinHeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.MinHeap, merged)
        
        rootNode = None
        if len(self.MinHeap) > 0:
            rootNode = heapq.heappop(self.MinHeap)
        return self.buildTree(rootNode, "")
    
    def buildTree(self, root, outputString = ""):
        if(root == None):
            return

        if(root.char != None):
            # print("Root.char", root.char)
            self.tree[root.char] = outputString
            self.invertedTree[outputString] = root.char
            return

        self.buildTree(root.left, outputString + "0")
        self.buildTree(root.right, outputString + "1")


    def huffman_encoding(self, data):
        encoded_data = ""
        for char in data:
            encoded_data += self.tree[char]
        return encoded_data

    def huffman_decoding(self, encoded_data):
        binarycode = ""
        decoded_data = ""

        for bit in encoded_data:
            binarycode += bit

            if (binarycode in self.invertedTree):
                decoded_data += self.invertedTree[binarycode]
                binarycode = ""
        
        return decoded_data

class TestHuffman(unittest.TestCase):

    def test_1(self):
        a_great_sentence = "The quick brown fox jumped over the lazy dog"

        # print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
        # print ("The content of the data is: {}\n".format(a_great_sentence))

        test = HuffmanCoding()
        test.buildHeap(a_great_sentence)
        encoded_data = test.huffman_encoding(a_great_sentence)

        # print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
        # print ("The content of the encoded data is: {}\n".format(encoded_data))

        decoded_data = test.huffman_decoding(encoded_data)

        # print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
        # print ("The content of the encoded data is: {}\n".format(decoded_data))
        self.assertEqual (decoded_data, a_great_sentence)
    
    def test2(self):
        test = HuffmanCoding()
        test_Sentence = ""
        test.buildHeap(test_Sentence)
        encoded_data = test.huffman_encoding(test_Sentence)

        self.assertEqual(encoded_data, test_Sentence)
        self.assertEqual(test.huffman_decoding(encoded_data), test_Sentence)
    
    def test3(self): 
        test = HuffmanCoding()
        input_data = "000000001111" # Code where 0 has higher frequency than 1

        test.buildHeap(input_data)
        encoded_data = test.huffman_encoding(input_data)
        # print ("The content of the encoded data is: {}\n".format(encoded_data))
        self.assertEqual(encoded_data, "111111110000") # Verify that most frequent bit gets lowest binary code
        self.assertEqual(test.huffman_decoding(encoded_data), input_data)
    
    def test4(self):
        test = HuffmanCoding()
        input_data = "AAAAA"
        test.buildHeap(input_data)
        encoded_data = test.huffman_encoding(input_data)
        # print ("The content of the encoded data is: {}\n".format(encoded_data))
        self.assertEqual(test.huffman_decoding(encoded_data), input_data)

    
if __name__ == "__main__":
    unittest.main()
