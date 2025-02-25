from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.role_checker import role_required
from core.role_permitter import role_permitter

@role_required(['GET'])
@role_permitter
def test(request, id):
    
    return Response({"test": "test"}, status=200)

def x(request):
    return Response({"tst": "tets"}, status=404)