from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def create(self, validated_data):
        # Ensure required fields are present in the data
        # Fields such as on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate should be calculated upon the status changing to 'completed'.
        fields_not_allowed = {'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate'}
        non_updatable_fields = [key for key in validated_data.keys() if key in fields_not_allowed]
        if non_updatable_fields:
            raise serializers.ValidationError({"message" : f"{non_updatable_fields} are computed keys"})
        return Vendor.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        custom = CustomUpdates(instance, validated_data)
        """
        Fields such as on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate should be calculated upon the status changing to 'completed'.
        Feilds such as created_at and updated_at should be part of ORM and has to be defined when a object is created and updated respectively.
        """
        allowed_fields = {'name', 'contact_details', 'address', 'vendor_code'}
        return custom.update_data(allowed_fields)

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
    
    def update(self, instance, validated_data):

        if validated_data.get('status') == 'completed':
            # Status cannot be set as Done unless all the fields have value, because status cannot be set done without user acknowledging
            combined_data = {**instance.__dict__, **validated_data}
            print(instance.__dict__)
            print(validated_data)
            print(combined_data)
            missing_fields = [key for key, value in combined_data.items() if not value]
            if missing_fields:
                response = {"message" : f"Missing or empty fields: {missing_fields}"}
                print(response)
                raise serializers.ValidationError(response)


        custom = CustomUpdates(instance, validated_data)
        """
        The order_date should be the datetime when the order was placed, and it should not be changed after creation.
        The acknowledgment_date should represent the time when the vendor acknowledges the order, and has to be updated by system not by user/api.
        Therefore, changing order_date and acknowledgment_date is not allowed.
        Feilds such as created_at and updated_at should be part of ORM and has to be defined when a object is created and updated respectively.
        allowed_fields can be further expaned/shortend based on the Bussiness requirements and management decisions
        """
        
        allowed_fields = {'po_number', 'vendor', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date'}
        return custom.update_data(allowed_fields)

class VendorPerformanceSerializer(serializers.ModelSerializer):
    vender_name = serializers.PrimaryKeyRelatedField(source='name', read_only=True)
    class Meta:
        model = Vendor
        fields = ('vender_name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')


class CustomUpdates():
    def __init__(self, instance=None, validated_data=None):
        self.instance = instance
        self.validated_data = validated_data
        pass

    def update_data(self, allowed_fields):
        '''
        To mitigate the risk of fraudulent activities, 
        only specific fields cab be permitted for modification, ensuring data integrity and security.
        '''
        updates = {"success":[], "failures":[]}
        for field, value in self.validated_data.items():
            updates["success"].append(field) if field in allowed_fields else updates["failures"].append(field)
            setattr(self.instance, field, value) if field in allowed_fields else None
        self.instance.save()

        if updates["failures"]:
            updates["message"] = f"Only {allowed_fields} fields are allowed for PATCH/PUT methods"
            raise serializers.ValidationError(updates)
        
        return self.instance
