# MIT License

# Copyright (c) 2021 Pranav Baburaj

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import math
import random

# The array ranges
# like the maximum value
# and the minimum value 
class Ranges():
    def __init__(self, l):
        self.qfjjwjjifjw = l

    def maximum(self):
        if len(self.qfjjwjjifjw) is not 0:
            return max(self.qfjjwjjifjw)

    def minimum(self):
        if len(self.qfjjwjjifjw) is not 0:
            return min(self.qfjjwjjifjw)

class Array():
    def __init__(self, data_type):
        self.members = []  # all the array memebers
        self.data_type = data_type # the array data type
    
    def len(self):
        # grab the length of 
        return len(self.members)

    @staticmethod
    def create(data):
        # Create a  new Single list instance
        # via a static metod
        return SingleList(data)

    # add a new member to the list
    def add(self, d_to_add):
        if isinstance(d_to_add, self.data_type):
            # check the type
            if d_to_add not in self.members:
                self.members.append(d_to_add)
        else:
            """
            Raise a  type Error because the types does not match
            """
            raise TypeError("Invalid type")

    def elementAt(self, i):
        """
        Get the element at the i-th
        index
        => [1, 2, 3], -1
            => 3
        """
        return self.members[i]

    def median(self):
        """
        Get the median of the array

        => [1, 2, 3] => 
            i : floor(len(arr) / 2)
            -> arr[i]
        => [1, 2, 3, 4] =>
            i : floor(len(arr) / 2)
            -> ( arr[i] + arr[i - 1] ) / 2
        """
        if self.data_type == int or self.data_type == float:
            # odd array = [1, 2, 3]
            if len(self.members) % 2 == 0:
                # even aray = [1, 2, 3, 4]
                a_lenght_h = int(len(self.members) / 2)   
                s_sum_of = self.members[a_lenght_h] + self.members[a_lenght_h - 1]
                return s_sum_of / 2
            else:
                return self.members[math.floor(len(self.members) / 2)]
        else:
            raise TypeError("Type not supported for finding the median")

    # delete an element by index
    def delete_index(self, i_t_d):
        return self.members.pop(i_t_d)

    def search_insert_position(self, target):
        """
        Search insert position
        ----------------------
        => if element exists in arr return the
        index

        => else return the index if the element
        has to be appended to a sorted array
        """
        if isinstance(target, self.data_type):
            if target in self.members:
                return self.members.index(target)
            else:
                self.members.append(target)
                return self.members.index(target)
        else:
            raise TypeError("Invalid target type")

    def index(self, e_f_i):
        if e_f_i in self.members:
            return self.members.index(e_f_i)

        return None

    def peak_index(self):
        # The maximum index
        return self.members.index(max(self.members))

    def range(self):
        return Ranges(self.members)

    def all(self):
        """
        Return all the members of the array
        """
        return self.members

    def count(self, i):
        if i in self.members:
            return self.members.count(i)

        return None

    def sort(self):
        self.members.sort()
        return self.members

    def find(self, d_t_f):
        indexes = []
        for x in range(len(self.members)):
            if self.members[x] == d_t_f:
                indexes.append(x)

        return indexes

    def delete(self, data_to_delete):
        access_data_indexes = []
        for index in range(len(self.members)):
            if self.members[index] == data_to_delete:
                access_data_indexes.append(index)
        
        for i in range(len(access_data_indexes)):
            del self.members[access_data_indexes[i]]
        
        return self.members

    def clear(self):
        self.members = []
        return self.members

    def reverse(self):
        self.members.reverse()
        return self.members

    def alternate_indexes(self):
        v_a_r = [[],[]]
        for x in range(len(self.members)):
            if x % 2 == 0:
                v_a_r[0].append(x)
            else:
                v_a_r[-1].append(x)

        return v_a_r

    def choice(self): 
        """
        Returns a randome element from the array
        """
        return self.members[random.randint(0, len(self.members))]
