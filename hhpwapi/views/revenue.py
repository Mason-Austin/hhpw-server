from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models import Revenue, Order, OrderItem

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
        total_amount = 0

        order = Order.objects.get(id=request.data["orderId"])

        order_items = OrderItem.objects.filter(order=order)

        for order_item in order_items:
            total_amount += order_item.item.price
        total_amount += request.data["tip"]

        revenue = Revenue.objects.create(
          total=total_amount,
          payment_type=request.data["paymentType"],
          tip=request.data["tip"],
          order_type=order.type,
          order=order
        )

        serializer = RevenueSerializer(revenue)
        return Response(serializer.data)

class RevenueSerializer(serializers.ModelSerializer):
    """JSON serializer for Revenue"""
    class Meta:
        model = Revenue
        fields = ("id", "total", "date", "payment_type", "tip", "order_type", "order")
