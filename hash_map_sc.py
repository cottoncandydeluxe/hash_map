# Course: CS261 - Data Structures
# Assignment: #6 Hash Maps (Portfolio Project)
# Due Date: 6/9/23
# Description: Implementation of a HashMap with Separate Chaining 
# Sources Cited: Skeleton code owned and provided by the professors at Oregon State University


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the key already exists,
        its value is replaced by the new value. If the key doesn't exist, 
        a new key/value pair is added.
        """
        if self.table_load() >= 1:
            new_capacity = self._capacity * 2 
            self.resize_table(new_capacity)

        idx = self._hash_function(key) % self._capacity
        ll = self._buckets[idx]
        node = ll.contains(key)
        if node is not None:
            node.value = value  # updates the value if the key exists
        else:
            ll.insert(key, value)  # adds a new key/value if the key DNE
            self._size += 1
 

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        idx = 0 
        empty_buckets = 0
        while idx != self._capacity:
            bucket = self._buckets[idx]
            if bucket.length() == 0:
                empty_buckets += 1
            idx += 1
        
        return empty_buckets


    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        n = self._size # total number of elements stored in the table
        m = self._capacity # total number of buckets
        load_factor = n / m
        return load_factor


    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the
        underlying hash table capacity.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0 


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map, and all hash table links must be rehashed.
        """
        if new_capacity < 1:
            return   
        
        old_length = self._buckets.length()
        old_array = self._buckets
        self._buckets = DynamicArray()
        
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        self._size = 0 # reset before putting in new values

        for _ in range(self._capacity):
            self._buckets.append(LinkedList()) # fill up with empty ll's

        for idx in range(old_length): # fill up with old key/values
            bucket = old_array[idx]
            for node in bucket:
                key = node.key
                value = node.value
                self.put(key, value)


    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        idx = self._hash_function(key) % self._capacity
        ll = self._buckets[idx]
        node = ll.contains(key)
        if node is not None:
            return node.value 


    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        value = self.get(key)
        if value == None:
            return False
        else:
            return True
 

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        idx = self._hash_function(key) % self._capacity
        ll = self._buckets[idx]
        removed = ll.remove(key)
        if removed:
            self._size -= 1 


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """
        dynamic_array = DynamicArray()

        for idx in range(self._capacity):
            ll = self._buckets[idx]
            for node in ll:
                if node is not None:
                    key = node.key
                    value = node.value
                    dynamic_array.append((key, value))

        return dynamic_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds mode(s) and frequency of elements in an unordered DynamicArray 
    by using a HashMap. Returns a tuple containing (a DynamicArray of
    all the modes found, an integer value of their frequency). 
    """
    map = HashMap()

    for idx in range(da.length()): # first store each element as a k/v: element/frequency
        key = da[idx]
        if map.contains_key(key):
            value = map.get(key) 
            value += 1
            map.put(key, value)
        else:
            map.put(key, 1)

    keys_and_values = map.get_keys_and_values() # then find the highest frequency
    frequency = 0 
    for idx in range(keys_and_values.length()):
        key_value = keys_and_values[idx]
        if key_value[1] > frequency:
            frequency = key_value[1]

    mode_array = DynamicArray()

    for idx in range(keys_and_values.length()): # fill up array with mode(s)
        key_value = keys_and_values[idx]
        if key_value[1] == frequency:
            mode_array.append(key_value[0]) 

    return (mode_array, frequency)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":


    # print('-------------------------')
    # print("Michelle's sandbox:")
    # print('-------------------------')
    # hashmap1 = HashMap(5, hash_function_1)
    # # print(f"hashmap's size: {hashmap1.get_size()}")
    # print(hashmap1)

    # hashmap1.put('str3', 25)
    # # print(f"hashmap's size: {hashmap1.get_size()}")
    # print(hashmap1)

    # ll = LinkedList()
    # print(ll)
    # ll.insert(1,'value')
    # print(ll)

#############################################################

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
    # m.get_capacity())


    # ##Michelle
    # ll = LinkedList()
    # ll.insert('key', 5)
    # ll.insert('key2', 6)
    # print(ll)

    # for node in ll:
    #     print(node)

    # m = HashMap(11, hash_function_1)
    # m.put('str107', 500)
    # # m.put('str108', 500)
    # # m.put('str109', 500)
    # # m.put('str110', 500)
    # # m.put('str111', 500)
    # # m.put('str112', 500)
    # # m.put('str1113', 500)
    # # m.put('str114', 500)
    # # m.put('str115', 500)
    # # m.put('str116', 500)
    # print(m)
    # m.resize_table(7)
    # print(m)
    # m.resize_table(30)
    # print(m)
    #print((hash_function_1('str107'))% 53 ) 
    # for i in range(150):
    #     #print('str' + str(i), i *100)
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())



    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())



    # m = HashMap(11, hash_function_2)
    # m.put('str2', 2)
    # print(m)
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())








    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "peach", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    # #print((find_mode(da)))







    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )

    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

