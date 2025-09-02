# upload_to_s3.py
import os
from django.core.files import File
from main.models import Group, Tifo

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")

def upload_group_logos():
    for group in Group.objects.all():
        if group.logo and not group.logo.url.startswith("http"):
            local_path = os.path.join(MEDIA_ROOT, group.logo.name)
            if os.path.exists(local_path):
                print(f"Uploading logo for {group.name}...")
                with open(local_path, "rb") as f:
                    group.logo.save(os.path.basename(local_path), File(f), save=True)

def upload_tifo_pictures():
    for tifo in Tifo.objects.all():
        if tifo.picture and not tifo.picture.url.startswith("http"):
            local_path = os.path.join(MEDIA_ROOT, tifo.picture.name)
            if os.path.exists(local_path):
                print(f"Uploading tifo for match {tifo.match}...")
                with open(local_path, "rb") as f:
                    tifo.picture.save(os.path.basename(local_path), File(f), save=True)

if __name__ == "__main__":
    upload_group_logos()
    upload_tifo_pictures()
    print("✅ Migration complete! All files pushed to S3.")
