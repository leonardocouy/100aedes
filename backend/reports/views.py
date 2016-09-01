from .permissions import IsReportOwner
from django.contrib.auth import login

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as JSONResponse
from .models import Report
from .serializers import ReportSerializer


class ReportCreateReadView(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)


class ReportReadUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated, IsReportOwner, )

# @api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, IsOwnerOrReadOnly))
# def report_list(request):
#     if request.method == 'GET':
#         reports = Report.objects.all()
#         serializer = ReportSerializer(reports, many=True)
#         return JSONResponse(serializer.data)
#     elif request.method == 'POST':
#         data = request.POST
#         serializer = ReportSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes((IsAuthenticated, IsOwnerOrReadOnly,))
# def report_detail(request, pk):
#     report = get_object_or_404(Report, pk=pk)
#
#     if request.method == 'GET':
#         serializer = ReportSerializer(report)
#         return JSONResponse(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ReportSerializer(report, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         else:
#             return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         report.delete()
#         return JSONResponse(status=status.HTTP_204_NO_CONTENT)