from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .permissions import IsReportOwner
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Report
from .serializers import ReportSerializer


class ReportCreateReadView(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )


class ReportReadUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated, IsReportOwner, )
    authentication_classes = (JSONWebTokenAuthentication, )