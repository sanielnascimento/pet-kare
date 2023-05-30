from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Request, Response, status
from groups.models import Group
from traits.models import Trait
from pets.models import Pet
from rest_framework.pagination import PageNumberPagination
from pets.serializers import PetSerializer


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request):
        serializer = PetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        group_data = serializer.validated_data.pop("group")
        trait_data = serializer.validated_data.pop("traits")

        group = Group.objects.filter(
            scientific_name=group_data["scientific_name"]
        ).first()

        if not group:
            group = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data, group=group)

        for trait in trait_data:
            traits = Trait.objects.filter(name__iexact=trait["name"]).first()

            if not traits:
                traits = Trait.objects.create(**trait)

                pet.traits.add(traits)
            else:
                pet.traits.add(traits)

        serializer = PetSerializer(pet)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request):
        pet_params = request.query_params.get("trait", None)

        if pet_params:
            pets = Pet.objects.filter(traits__name=pet_params).all()
            page = self.paginate_queryset(pets, request, view=self)
            serializer = PetSerializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        pets = Pet.objects.all()
        page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)


class PetDetailsView(APIView):
    def get(self, __: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        trait_data = serializer.validated_data.pop("traits", None)
        trait_list = []

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        if group_data:
            try:
                group_obj = Group.objects.get(
                    scientific_name=group_data["scientific_name"]
                )
                pet.group = group_obj
            except Group.DoesNotExist:
                group_obj = Group.objects.create(**group_data)
                pet.group = group_obj

        if trait_data:
            for trait in trait_data:
                traits = Trait.objects.filter(
                    name__iexact=trait["name"]
                ).first()

            if not traits:
                traits = Trait.objects.create(**trait)

            trait_list.append(traits)
            pet.traits.set(trait_list)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
