
from django.shortcuts import render

# Create your views here.


def grouped_list(group_list, group_size=4):
    my_list = []
    for i in range(0, len(group_list), group_size):
        my_list.append(group_list[i:i+group_size])
    return my_list


def most_visited(request):
    x_forwarded_for = request.META.get('HTTP-X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


