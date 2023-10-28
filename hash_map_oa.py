# Course: CS261 - Data Structures
# Assignment: #6 Hash Maps (Portfolio Project)
# Due Date: 6/9/23
# Description: Implementation of a Hashmap with Open Addressing
# Sources Cited: Skeleton code owned and provided by the professors at Oregon State University

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2 
            self.resize_table(new_capacity)

        idx = self._hash_function(key) % self._capacity
        hash_entry = HashEntry(key, value)
        j = 0
        probe_idx = (idx + (j * j)) % self._capacity  # quad probing

        while self._buckets[probe_idx] != hash_entry:
            probe_idx = (idx + (j * j)) % self._capacity
            if self._buckets[probe_idx] is None or self._buckets[probe_idx].is_tombstone: 
                self._buckets[probe_idx] = hash_entry
                self._size += 1
            if self._buckets[probe_idx].key == key:
                self._buckets[probe_idx] = hash_entry
            j += 1


    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        n = self._size # total number of elements stored in the table
        m = self._capacity # total number of buckets
        load_factor = n / m
        return load_factor


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        idx = 0 
        empty_buckets = 0
        while idx != self._capacity:
            bucket = self._buckets[idx]
            if bucket is None or bucket.is_tombstone:
                empty_buckets += 1
            idx += 1
        
        return empty_buckets


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        """
        if new_capacity < self._size:
            return
        
        old_size = self._buckets.length()
        old_array = self._buckets
        self._buckets =DynamicArray()
        
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        self._size = 0 #reset before putting in new values

        for _ in range(self._capacity):
            self._buckets.append(None)

        for idx in range(old_size):
            if old_array[idx] is not None and old_array[idx].is_tombstone is False:
                key = old_array[idx].key
                value = old_array[idx].value
                self.put(key, value)


    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """
        idx = self._hash_function(key) % self._capacity
        j = 0
        probe_idx = (idx + (j * j)) % self._capacity # quad probing

        while self._buckets[probe_idx] is not None: 
            probe_idx = (idx + (j * j)) % self._capacity
            if self._buckets[probe_idx] is None: 
                return
            if self._buckets[probe_idx].key == key and self._buckets[probe_idx].is_tombstone is False:
                return self._buckets[probe_idx].value
            j += 1


    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map,
        otherwise it returns False.
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
        j = 0
        probe_idx = (idx + (j * j)) % self._capacity # quad probing

        while self._buckets[probe_idx] is not None: 
            probe_idx = (idx + (j * j)) % self._capacity 
            if self._buckets[probe_idx] is None: 
                return
            if self._buckets[probe_idx].key == key and self._buckets[probe_idx].is_tombstone is False:
                self._buckets[probe_idx].is_tombstone = True
                self._size -= 1
            j += 1

   
    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0 


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """
        dynamic_array = DynamicArray()

        for idx in range(self._capacity):
            bucket = self._buckets[idx]
            if bucket is not None and bucket.is_tombstone is False:
                key = bucket.key
                value = bucket.value
                dynamic_array.append((key, value))

        return dynamic_array


    def __iter__(self):
        """
        Lets the hash map iterate across itself.
        """
        self._index = 0
        return self


    def __next__(self):
        """
        Returns the next item in the hash map, based on the current location of theiterator.
        """
        try: 
            while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone: 
                self._index += 1
            if self._buckets[self._index] is not None:
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration
        
        self._index += 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":


    # ###Michelle's sandbox
    # print('------------------')
    # print("Michelle's Sandbox")
    # print('------------------')
    # m = HashMap(107, hash_function_1)
    # print(m)
    # m.put('key30', 1)
    # m.put('key17', 2)
    # m.put('key39', 1)
    # m.put('key58', 1)
    # m.put('key76', 5)
    # m.put('key221', 5)
    # m.put('key331', 5)
    # m.put('key223', 5)
    # m.put('key720', 5)
    # m.put('key361', 5)
    # m.put('key614', 5)
    # m.put('key236', 5)
    # m.put('key238', 5)
    # m.put('key743', 5)
    # m.put('key591', 5)
    # m.put('key169', 5)
    # m.put('key943', 5)
    # m.put('key486', 5)
    # m.put('key919', 5)
    # m.put('key496', 5)
    # m.put('key944', 5)
    # m.put('key697', 5)
    # m.put('key241', 5)
    # m.put('key968', 5)
    # m.put('key718', 5)
    # m.put('key387', 5)
    # m.put('key156', 5)
    # m.put('key151', 5)
    # m.put('key251', 5)
    # m.put('key525', 5)
    # m.put('key520', 5)
    # m.put('key912', 5)

    # print(f'size: {m._size}, capacity: {m._capacity}')
    # print(m)
    # m.resize_table(10)
    # print(f'size: {m._size}, capacity: {m._capacity}')
    # print(m)
    # hash_entry = HashEntry("str1", 1)
    # print(hash_entry)

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     #print(m)
    #     #print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
   

    # print((hash_function_1('str14'))% 53)

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

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(25, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    # m = HashMap(11, hash_function_1)
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

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)

    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
