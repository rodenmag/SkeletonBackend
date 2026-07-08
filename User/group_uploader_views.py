import csv

from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import MainGroup, GroupUser
from .serializers import GroupCSVUploadSerializer


class GroupCSVUploadViewSet(viewsets.ModelViewSet):

    parser_classes = [MultiPartParser, FormParser]
    serializer_class = GroupCSVUploadSerializer

    queryset = MainGroup.objects.none()

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES['csv_file']
        name = serializer.validated_data['name']

        # Use existing group or create a new one
        group, group_created = MainGroup.objects.get_or_create(
            name=name
        )

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for row in reader:

            first_name = row.get('First Name', '').strip()
            last_name = row.get('Last Name', '').strip()

            email = row.get(
                'E-mail 1 - Value',
                ''
            ).strip().lower()

            if not email:
                skipped_count += 1
                continue

            full_name = f"{first_name} {last_name}".strip()

            user = User.objects.filter(
                email__iexact=email
            ).first()

            if not user:
                skipped_count += 1
                continue

            group_user, created = GroupUser.objects.get_or_create(
                group_id=group,
                email=email,
                defaults={
                    'user_id': user,
                    'name': full_name
                }
            )

            if created:
                created_count += 1
            else:
                updated_fields = []

                if group_user.name != full_name:
                    group_user.name = full_name
                    updated_fields.append('name')

                if group_user.user_id != user:
                    group_user.user_id = user
                    updated_fields.append('user_id')

                if updated_fields:
                    group_user.save(update_fields=updated_fields)
                    updated_count += 1

        return Response({
            'success': 'CSV uploaded successfully',
            'group': group.name,
            'group_created': group_created,
            'created_count': created_count,
            'updated_count': updated_count,
            'skipped_count': skipped_count
        }, status=status.HTTP_201_CREATED)