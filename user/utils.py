from rest_framework import pagination, status
from rest_framework.response import Response


class ResponseInfo(object):
    """
    Class for setting how API should send response.
    """

    def __init__(self, user=None, **args):
        self.response = {
            "status_code": args.get('status', 200),
            "error": args.get('error', None),
            "data": args.get('data', []),
            "message": [args.get('message', 'Success')]
        }


class CustomPagination(pagination.PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            "status_code": status.HTTP_200_OK,
            "error": None,
            "data": [{
                'links': {
                    'total_pages': self.page.paginator.num_pages,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'count': self.page.paginator.count,
                'results': data
            }],
            "message": "Success"
        })