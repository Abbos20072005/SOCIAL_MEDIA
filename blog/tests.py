from django.test import TestCase

posts = [
    {
        'id': 1,
        'title': 'a'
    },
    {
        'id': 2,
        'title': 'b'
    },
    {
        'id': 3,
        'title': 'c'
    },
    {
        'id': 4,
        'title': 'd'
    },
]

comments = [
    {
        'post_id': 1,
        'message': 'A'
    },
    {
        'post_id': 1,
        'message': 'B'
    },
    {
        'post_id': 1,
        'message': 'B'
    },
    {
        'post_id': 2,
        'message': 'A'
    },
    {
        'post_id': 3,
        'message': 'A'
    },
    {
        'post_id': 4,
        'message': 'A'
    },
    {
        'post_id': 4,
        'message': 'A'
    },
    {
        'post_id': 4,
        'message': 'A'
    },
]

...

result = [
    {
        'id': 1,
        'title': 'a',
        'comments': [
            {
                'post_id': 1,
                'message': 'A'
            },
            {
                'post_id': 1,
                'message': 'B'
            },
        ]
    },
    {
        'id': 2,
        'title': 'b',
        'comments': [
            {
                'post_id': 2,
                'message': 'A'
            }
        ]
    },
    {
        'id': 3,
        'title': 'c',
        'comments': [
            {
                'post_id': 3,
                'message': 'A'
            },
        ]
    },
    {
        'id': 4,
        'title': 'd',
        'comments': [
            {
                'post_id': 4,
                'message': 'A'
            },
            {
                'post_id': 4,
                'message': 'A'
            },
            {
                'post_id': 4,
                'message': 'A'
            },
        ]
    },
]


for i in posts:
    lts = []
    for j in comments:
        if i['id'] == j['post_id']:
            lts.append(j)
            i['comments'] = lts
            if i not in lst:
                lst.append(i)
print(f'result = {lst}')
