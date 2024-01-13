from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from ..models import Order, User, Item, OrderItem
class OrderView(ViewSet):
    """hhpw order view"""
    @action(methods=['post'], detail=True)
    def add_item_to_order(self, request, pk):
        order = Order.objects.get(pk=pk)
        item = Item.objects.get(id=request.data['item'])
        OrderItem.objects.create(
            order=order,
            item=item
        )


        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @action(methods=['delete'], detail=True)
    def remove_item_from_order(self, request, pk):
        order = Order.objects.get(pk=pk)
        order_item = OrderItem.objects.get(id=request.data["orderItemId"])
        order_item.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data)

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

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized order instance
        """
        user = User.objects.get(id=request.data["userId"])

        order = Order.objects.create(
          name=request.data["name"],
          customer_phone=request.data["customerPhone"],
          customer_email=request.data["customerEmail"],
          type=request.data["type"],
          user=user,
        )

        items = request.data["items"]

        for item in items:
            item = Item.objects.get(id=item)
            OrderItem.objects.create(
                order=order,
                item=item
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a order

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.name=request.data["name"]
        order.open=request.data["open"]
        order.customer_phone=request.data["customerPhone"]
        order.customer_email=request.data["customerEmail"]
        order.type=request.data["type"]
        order.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class OrderItemSerializer(serializers.ModelSerializer):
    """JSON serializer for OrderItem"""
    
    price = serializers.ReadOnlyField(source='item.price')
    name = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = OrderItem
        fields = ('id', 'price', 'name')

class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for Order"""
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id", "name", "open", "customer_phone", "customer_email", "type", "user", "items")
        depth = 1
