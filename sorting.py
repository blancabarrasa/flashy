#we can use any of the sort algos below
def sort(list):
    return sort_bubble(list)


def sort_bubble(list):
    n = len(list)

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(n - i - 1):
            # Swap if the element found is greater than the next element
            if list[j]["subject"] > list[j + 1]["subject"]:
                list[j], list[j + 1] = list[j + 1], list[j]

    return list


def insertion_sort_string(lst):
    # Traverse through the list starting from the second element
    for i in range(1, len(lst)):
        # Store the current element and its index
        current_element = lst[i]
        j = i - 1

        # Shift all elements to the right of the current element that are greater than it
        while j >= 0 and lst[j] > current_element:
            lst[j + 1] = lst[j]
            j -= 1

        # Insert the current element at the correct position
        lst[j + 1] = current_element

    return lst




def linear_search_string(target_str, string_list):
    # Traverse through all elements in the list
    for element in string_list:
        # If the target string is found in the list, return True
        if element == target_str:
            return True
    # If the target string is not found in the list, return False
    return False


#def binary_search_string(target_str, string_list):
    # Get the lower and upper bounds of the search space
    #left, right = 0, len(string_list) - 1

    # Continue searching until the search space is empty
    #while left <= right:
        # Calculate the midpoint of the search space
        #mid = (left + right) // 2

        # If the target string is found at the midpoint, return True
        #if string_list[mid] == target_str:4
            #return True

        # If the target string is smaller than the midpoint, search the left half
       # elif string_list[mid] > target_str:
            #right = mid - 1

        # If the target string is larger than the midpoint, search the right half
        #else:
            #left = mid + 1

    # If the target string is not found in the list, return False
    #return False


