from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models import Revenue, Order

class RevenueView(ViewSet):
    """HHPW revenue view"""

    def list(self, request):
        """Handle GET requests for every Revenue
        
        Returns:
          Response -- JSON serialized Revenues."""
        revenues = Revenue.objects.all()
        serializer = RevenueSerializer(revenues, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialzied Revenue instance"""
        order = Order.objects.get(id=request.data["orderID"])
        
        revenue = Revenue.objects.create(
          total=request.data["total"],
          payment_type=request.data["paymentType"],
          tip=request.data["tip"],
          order_type=request.data["orderType"],
          order=order
        )
        
        serializer = RevenueSerializer(revenue)
        return Response(serializer.data)

class RevenueSerializer(serializers.ModelSerializer):
    """JSON serializer for Revenue"""
    class Meta:
        model = Revenue
        fields = ("id", "total", "date", "payment_type", "tip", "order_type", "order")
