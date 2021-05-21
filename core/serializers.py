from rest_framework import serializers
from .models import *

class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ['id','description','historical_data']

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id','description']

class CustomerSerializer(serializers.ModelSerializer):
    num_professions=serializers.SerializerMethodField()
    data_Sheet=DataSheetSerializer()
    professions=ProfessionSerializer(many=True)
    document_set=serializers.StringRelatedField(many=True)
    class Meta:
        model = Customer
        fields = ['id','name', 'address', 'professions', 'data_Sheet',
                  'active','status_message','num_professions','document_set']

    def get_num_professions(self,obj):
        return obj.num_professions()


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','dtype','doc_number','customers']
