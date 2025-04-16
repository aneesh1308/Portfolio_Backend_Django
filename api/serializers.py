import json
import os
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Resume, Experience, Certification, Education, TechSkill, SoftSkill, Hobby, SliderGallery, Blog, BlogBlock
import cloudinary.api
from cloudinary.exceptions import NotFound
from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy
# from .models import Note

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print(f'{user} user created')
        
        if user.is_staff:
            print("creating resume")
            try:
                Resume.objects.create(user=user, email=user.email)
            except Exception as e:
                print(f"Resume creation failed: {e}")
        return user


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ('resume',)

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        exclude = ('resume',)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('resume',)

class TechSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechSkill
        exclude = ('resume',)

class SoftSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        exclude = ('resume',)

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        exclude = ('resume',)

class SliderGallerySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SliderGallery
        fields = ("image",)

    def get_image(self, obj):
        try:
            request = self.context.get("request")
            if obj.image and request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url if obj.image else None
        except Exception as e:
            print(f"Error in get_image: {e}")
            return None


class ResumeSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(use_url=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    education = EducationSerializer(many=True, required=False)
    tech_skills = TechSkillSerializer(many=True, required=False)
    soft_skills = SoftSkillSerializer(many=True, required=False)
    hobbies = HobbySerializer(many=True, required=False)
    slider_gallery = SliderGallerySerializer(many=True, read_only=True, source='gallery')


    def create(self, validated_data):
        # Handle nested data
        request = self.context['request']
        experiences_data = json.loads(request.data.get('experiences', '[]'))
        certifications_data = json.loads(request.data.get('certifications', '[]'))
        education_data = json.loads(request.data.get('education', '[]'))
        tech_skills_data = json.loads(request.data.get('tech_skills', '[]'))
        soft_skills_data = json.loads(request.data.get('soft_skills', '[]'))
        hobbies_data = json.loads(request.data.get('hobbies', '[]'))

        slider_gallery_urls = json.loads(request.data.get('slider_gallery', '[]'))  # URLs from frontend
        slider_gallery_files = request.FILES.getlist('slider_gallery') 

        print("Validated Data:", validated_data)

        resume = Resume.objects.create(**validated_data)

        for experience in experiences_data:
            Experience.objects.create(resume=resume, **experience)

        for cert_data in certifications_data:
            Certification.objects.create(resume=resume, **cert_data)

        for edu_data in education_data:
            Education.objects.create(resume=resume, **edu_data)

        for skill_data in tech_skills_data:
            TechSkill.objects.create(resume=resume, **skill_data)

        for skill_data in soft_skills_data:
            SoftSkill.objects.create(resume=resume, **skill_data)

        for hobby_data in hobbies_data:
            Hobby.objects.create(resume=resume, **hobby_data)

        for gallery_item in slider_gallery_files:
            SliderGallery.objects.create(resume=resume, image=gallery_item)

      
        return resume

    def update(self, instance, validated_data):
        try:
            request = self.context['request']
            profile_image = validated_data.get('profile_image', None)

            if profile_image:
            # Delete old Cloudinary image only if it exists
                if instance.profile_image:
                    old_image_name = instance.profile_image.name
                    if old_image_name:
                        public_id = os.path.splitext(old_image_name)[0]
                        print(f"Deleting Cloudinary image: {public_id}")
                        try:
                            cloudinary.api.resource(public_id)
                            print(f"Resource exists. Deleting Cloudinary image: {public_id}")
                            cloudinary_destroy(public_id)
                        except NotFound:
                            print(f"Cloudinary image {public_id} not found, skipping delete.")
                        except Exception as e:
                            print(f"Unexpected error while deleting Cloudinary image: {e}")


                # Set new image
                instance.profile_image = profile_image

            # Update other fields
            for attr, value in validated_data.items():
                if attr != 'profile_image':
                    setattr(instance, attr, value)

            instance.save()

            experiences_data = json.loads(request.data.get('experiences', '[]'))
            certifications_data = json.loads(request.data.get('certifications', '[]'))
            education_data = json.loads(request.data.get('education', '[]'))
            tech_skills_data = json.loads(request.data.get('tech_skills', '[]'))
            soft_skills_data = json.loads(request.data.get('soft_skills', '[]'))
            hobbies_data = json.loads(request.data.get('hobbies', '[]'))

            slider_gallery_urls = request.data.getlist('slider_gallery_urls') or []
            slider_gallery_files = request.FILES.getlist('slider_gallery') 

            # Clear & re-create related models
            instance.experiences.all().delete()
            for exp_data in experiences_data:
                Experience.objects.create(resume=instance, **exp_data)

            instance.certifications.all().delete()
            for cert_data in certifications_data:
                Certification.objects.create(resume=instance, **cert_data)

            instance.education.all().delete()
            for edu_data in education_data:
                Education.objects.create(resume=instance, **edu_data)

            instance.tech_skills.all().delete()
            for skill_data in tech_skills_data:
                TechSkill.objects.create(resume=instance, **skill_data)

            instance.soft_skills.all().delete()
            for skill_data in soft_skills_data:
                SoftSkill.objects.create(resume=instance, **skill_data)

            instance.hobbies.all().delete()
            for hobby_data in hobbies_data:
                Hobby.objects.create(resume=instance, **hobby_data)

            # Slider gallery logic
            existing_filenames = set(url.split('/')[-1] for url in slider_gallery_urls if isinstance(url, str))

            for slider in instance.gallery.all():
                db_filename = slider.image.name.split('/')[-1]
                if db_filename not in existing_filenames:
                    # Delete from Cloudinary
                    public_id = f"resume_gallery/{os.path.splitext(db_filename)[0]}"
                    try:
                        print(f"Deleting Cloudinary slider image: {public_id}")
                        cloudinary_destroy(public_id)
                    except Exception as e:
                        print(f"Error deleting slider image from Cloudinary: {e}")
                    slider.delete()

            # Upload new slider files to Cloudinary
            for file in slider_gallery_files:
                try:
                    print(f"Uploading to Cloudinary: {file.name}")
                    instance.gallery.create(image=file)
                except Exception as e:
                    print(f"Error uploading slider image to Cloudinary: {e}")

            return instance
        except Exception as e:
            print("Update error:", str(e))
            raise serializers.ValidationError({"detail": str(e)})

    class Meta:
        model = Resume
        fields = (
            "name",
            "title",
            "bio",
            "profile_image",
            "experiences",
            'certifications',
            'education',
            'tech_skills',
            'soft_skills',
            'hobbies',
            'slider_gallery',
        )

class BlogBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogBlock
        fields = ["id", "type", "content", "media_file", "order"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.type in ["image", "video"] and instance.media_file:
            data["content"] = request.build_absolute_uri(instance.media_file.url) if request else instance.media_file.url
        return data


class BlogSerializer(serializers.ModelSerializer):
    blocks = BlogBlockSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = ["id", "user", "title", "description", "category", "cover_image", "tags", "likes_count", "resource_link", "deployed_link", "blocks", "created_at"]

    def create(self, validated_data):
        request = self.context['request']
        blocks_data = json.loads(request.data.get("blocks", "[]"))
        media_files = request.FILES.getlist("blocks_files")
        media_index = 0
        
        blog = Blog.objects.create(**validated_data)
        blocks = []

        for index, block_data in enumerate(blocks_data):
            media_file = None
            if block_data.get("type") in ["image", "video"] and media_index < len(media_files):
                media_file = media_files[media_index]
                media_index += 1

            blocks.append(
                BlogBlock(
                    blog=blog,
                    type=block_data.get("type"),
                    content=block_data.get("content"),
                    media_file=media_file,
                    order=index,
                )
            )
        BlogBlock.objects.bulk_create(blocks)
        return blog

    def update(self, instance, validated_data):
        request = self.context['request']
        blocks_data = json.loads(request.data.get("blocks", "[]"))
        media_files = request.FILES.getlist("blocks_files")
        media_index = 0
        updated_block_ids = []

        for index, block_data in enumerate(blocks_data):
            block_id = block_data.get("id")
            media_file = None

            if block_data.get("type") in ["image", "video"] and media_index < len(media_files):
                media_file = media_files[media_index]
                media_index += 1

            if block_id:
                try:
                    block = BlogBlock.objects.get(id=block_id, blog=instance)
                    block.type = block_data.get("type", block.type)
                    block.content = block_data.get("content", block.content)
                    block.order = index
                    if media_file:
                        if block.media_file:
                            block.media_file.delete(save=False)
                        block.media_file = media_file
                    
                    block.save()

                except BlogBlock.DoesNotExist:
                    block = BlogBlock.objects.create(
                        blog=instance,
                        type=block_data.get("type"),
                        content=block_data.get("content"),
                        media_file=media_file,
                        order=index,
                    )
            else:
                block = BlogBlock.objects.create(
                    blog=instance,
                    type=block_data.get("type"),
                    content=block_data.get("content"),
                    media_file=media_file,
                    order=index,
                )

            updated_block_ids.append(block.id)

        for block in instance.blocks.exclude(id__in=updated_block_ids):
            block.delete()

        return super().update(instance, validated_data)
    
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "description",
            "category",
            "tags",
            "cover_image",
            "created_at",
            "comments",
            "likes_count"
        ]