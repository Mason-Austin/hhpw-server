from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models import Order
class OrderView(ViewSet):
    """hhpw order view"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single order type
      
        returns:
        Response -- JSON Serialzied order"""
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
          
    def list(self, request):
        """Handle GET requests for every Order

        Returns:
            Response -- JSON serialized Orders
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for Order"""
    class Meta:
        model = Order
        fields = ("id", "name", "open", "customer_phone", "customer_email", "type", "user")
        depth = 1
