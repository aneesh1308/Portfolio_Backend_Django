from django.contrib import admin
from .models import CustomUser, Resume, Experience, Certification, Education, TechSkill, SoftSkill, Hobby, SliderGallery, Blog, BlogBlock
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(Education)
admin.site.register(TechSkill)
admin.site.register(SoftSkill)
admin.site.register(Hobby)
admin.site.register(SliderGallery)
admin.site.register(Blog)
admin.site.register(BlogBlock)