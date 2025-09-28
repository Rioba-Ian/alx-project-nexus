from .models import CustomUser, Job, Company, JobApplication, Favorite
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone", "role", "password"]
        read_only_fields = ["role"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
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
            "experience",
            "min_experience_years",
            "max_experience_years",
            "mode",
            "salary",
            "salary_currency",
            "category",
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

    experience_display = serializers.CharField(
        source="get_experience_display", read_only=True
    )
    mode_display = serializers.CharField(source="get_mode_display", read_only=True)
    salary_currency_display = serializers.CharField(
        source="get_salary_currency_display", read_only=True
    )

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
            "experience_display",
            "mode_display",
            "salary_currency_display",
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
