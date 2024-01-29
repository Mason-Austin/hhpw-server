from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models import Item


class ItemView(ViewSet):
    """hhpw item view"""
    def retrieve(self, request, pk):
        """Handle GET requests for a single item type
        
        returns:
        Response -- JSON Serialzied item"""
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for every Item

        Returns:
          Response -- JSON serialized Items"""
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for Item"""
    class Meta:
        model = Item
        fields = ("id", "name", "price")
