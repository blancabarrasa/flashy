from oldflashy.sorting import sort_bubble

def test_sort_bubble_subjects():
    # Test sorting an empty list
    lst = []
    sort_bubble(lst)
    assert lst == []

    # Test sorting a list with one element
    lst = ["Math"]
    sort_bubble(lst)
    assert lst == ["Math"]

    # Test sorting a list with two elements
    lst = ["English", "Math"]
    sort_bubble(lst)
    assert lst == ["English", "Math"]

    # Test sorting a list with three elements
    lst = ["Science", "Math", "English"]
    sort_bubble(lst)
    assert lst == ["English", "Math", "Science"]

    # Test sorting a list with repeated elements
    lst = ["Science", "Math", "English", "Math"]
    sort_bubble(lst)
    assert lst == ["English", "Math", "Math", "Science"]

    # Test sorting a list that is already sorted
    lst = ["English", "Math", "Science"]
    sort_bubble(lst)
    assert lst == ["English", "Math", "Science"]

    # Test sorting a large list
    lst = ["Math", "Science", "English", "History", "Geography",
           "Biology", "Chemistry", "Physics", "Art", "Music",
           "Physical Education", "Computing", "Design and Technology", "Foreign Languages", "Religious Education",
           "Citizenship", "Personal, Social and Health Education"]
    sort_bubble(lst)
    assert lst == ["Art", "Biology", "Chemistry", "Citizenship", "Computing",
                   "Design and Technology", "English", "Foreign Languages", "Geography", "History",
                   "Math", "Music", "Personal, Social and Health Education", "Physical Education", "Physics",
                   "Religious Education", "Science"]



test_sort_bubble_subjects()