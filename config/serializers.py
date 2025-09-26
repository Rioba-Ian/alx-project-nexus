from .models import CustomUser, Job, Company, JobApplication, Favorite
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone", "role"]
        read_only_fields = ["role"]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.role = CustomUser.USER
        user.save()
        return user


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "description",
            "website",
            "owner",
            "created_at",
        ]


class JobCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source="company",
        queryset=Company.objects.all(),
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "company_id",
            "location",
            "is_active",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["posted_by"] = user
        return super().create(validated_data)


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField(read_only=True)
    resume = serializers.FileField(required=False)

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job",
            "applicant",
            "resume",
            "cover_letter",
            "status",
            "created_at",
        ]
        read_only_fields = ["status", "applicant", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["applicant"] = user
        return super().create(validated_data)


class JobApplicationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication
        fields = ["status"]


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source="company",
        queryset=Company.objects.all(),
    )

    posted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "company",
            "company_id",
            "location",
            "posted_by",
            "created_at",
            "updated_at",
            "is_active",
            "experience",
            "min_experience_years",
            "max_experience_years",
            "mode",
            "salary",
            "salary_currency",
            "category",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    job = serializers.StringRelatedField(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source="job",
        queryset=Job.objects.all(),
    )

    class Meta:
        model = Favorite
        fields = ["id", "user", "job", "job_id", "created_at"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.USERNAME_FIELD

    def validate(self, attrs):
        credentials = {
            "email": attrs.get("email"),
            "password": attrs.get("password"),
        }

        return super().validate(credentials)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token


class CustomerTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
