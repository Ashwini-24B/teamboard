from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Count, Sum

from .models import KBEntry, QueryLog
from .serializers import KBEntrySerializer, RegistrationSerializer
from .permissions import IsAdminUser


# User registration
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


# List and create knowledge base entries
class KBEntryListCreateView(generics.ListCreateAPIView):
    queryset = KBEntry.objects.all().order_by('-created_at')
    serializer_class = KBEntrySerializer


# Retrieve, update, or delete a knowledge base entry
class KBEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KBEntry.objects.all()
    serializer_class = KBEntrySerializer


# Search the knowledge base and log each query
class KBQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        search_term = request.data.get('search', '').strip()

        if not search_term:
            return Response(
                {'error': 'Search term is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = KBEntry.objects.filter(
            Q(question__icontains=search_term) |
            Q(answer__icontains=search_term)
        )

        result_count = results.count()

        QueryLog.objects.create(
            company=request.user.company,
            search_term=search_term,
            results_count=result_count
        )

        serializer = KBEntrySerializer(results, many=True)

        return Response({
            'search': search_term,
            'count': result_count,
            'results': serializer.data
        }, status=status.HTTP_200_OK)


# Admin-only usage summary
class UsageSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_queries = QueryLog.objects.count()

        total_results = QueryLog.objects.aggregate(
            total=Sum('results_count')
        )['total'] or 0

        company_usage = QueryLog.objects.values(
            'company__company_name'
        ).annotate(
            total_queries=Count('id'),
            total_results=Sum('results_count')
        ).order_by('-total_queries')

        return Response({
            'total_queries': total_queries,
            'total_results': total_results,
            'company_usage': list(company_usage)
        }, status=status.HTTP_200_OK)