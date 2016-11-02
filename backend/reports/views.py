from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .permissions import IsReportOwner
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Report
from .serializers import ReportSerializer


class ReportCreateReadView(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_queryset(self):
        """
        if user is a superuser or a "Agente" return all reports or
        if it is an "Agente" return only Reports that is in analysis or sent
        """
        user = self.request.user
        if user.is_superuser:
            return Report.objects.all()
        else:
            try:
                if user.groups.get(id=1).name == 'Agente':
                    return Report.objects.filter(Q(status=1) | Q(status=2))
            except Group.DoesNotExist:
                return Report.objects.filter(user=user)

class ReportReadUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated, IsReportOwner, )
    authentication_classes = (JSONWebTokenAuthentication, )
