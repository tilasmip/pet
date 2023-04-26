from rest_framework import serializers
from django.db.models import Q
from main.models import Adoption, Adoption, Animal
from main.enums import AdoptionStatus


class SaveAdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['requested_by', 'animal', 'status', 'message',]

    def validate(self, attrs):
        animal = attrs.get('animal')
        if Adoption.objects.filter(Q(animal=animal) & (~Q(status=AdoptionStatus.APPROVED) & ~Q(status=AdoptionStatus.PENDING))).exists():
            raise serializers.ValidationError(
                "The dog is being adopted.")
        return attrs

    def create(self, validated_data):

        adoption = Adoption.objects.create(**validated_data)
        return adoption


class UpdateAdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['message', 'animal', 'status']

    def validate(self, attrs):
        if not Adoption.objects.filter(requested_by=self.context.get('user')):
            raise serializers.ValidationError("Data not found.")
        status = attrs.get('status')
        print(status)
        if status is not None and status != AdoptionStatus.CANCELED:
            raise serializers.ValidationError("Unknown command.")
        return attrs

    def update(self, instance, validated_data):
        if (validated_data.get('status') is not None):
            print(instance.status)
            instance.status = validated_data.get('status')
        instance.message = validated_data.get('message')
        instance.save()
        return instance


class AcceptAdoptionSerializer(serializers.Serializer):
    animal = None

    def validate(self, attrs):
        if self.instance.animal.adopted == True:
            raise serializers.ValidationError("No longer in hold.")

        self.animal = self.instance.animal
        if self.animal is None:
            raise serializers.ValidationError("Animal not found.")
        return attrs

    def update(self, instance, validated_data):
        requests = Adoption.objects.filter(
            Q(animal=self.animal) & (id != instance.id))
        for request in requests:
            request.status = AdoptionStatus.REJECTED
            request.save()
        instance.status = AdoptionStatus.APPROVED
        instance.save()
        return instance


class RejectAdoptionSerializer(serializers.Serializer):
    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.status = AdoptionStatus.REJECTED
        instance.save()
        return instance


class DeleteAdoptionSerializer(serializers.Serializer):
    adoption = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.adoption = Adoption.objects.get(
                id=id, requested_by=self.context.get('user_id'))
            if self.adoption is None:
                raise serializers.ValidationError(
                    {'msg': 'Adoption doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'Adoption doesn\'t exist.'})
        return attrs

    def delete_adoption(self):
        name = self.context.get('id')
        self.adoption.delete()
