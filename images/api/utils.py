from images.models import Image, Tag
from events.models import Event
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from PIL import Image as Img
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
import os
from django.conf import settings


def create_event(event_type, initiator, content_type, object_id) :
    try :
        assert event_type and initiator and content_type and object_id
        event = Event.objects.create(
            event_type = event_type,
            initiator = initiator,
            content_type = content_type,
            object_id = object_id
        )
        return event
    except AssertionError :
        return

def create_none_existing_tags(tags) :
    to_be_created_tags = [
        Tag(content = tag) for tag in tags if not Tag.objects.filter(content = tag).exists()
    ]

    Tag.objects.bulk_create(to_be_created_tags)
    return tags

def create_thumbnail(row_img_obj,img_after_created,width = 400) :
    img = Img.open(row_img_obj)
    #resized_img = img.resize((width,width))
    img.thumbnail((width,width), Img.ANTIALIAS)
    img_out = BytesIO()
    img.save(img_out,img.format, quality=95)
    img_full_name = row_img_obj.name.split(".")[0] + '.' + img.format
    img_after_created.thumbnail.save(img_full_name,File(img_out))

def upload_img(img_obj,tags,initiator) :

    create_none_existing_tags(tags)
    img = Image.objects.create(
        image = img_obj,
    )

    create_thumbnail(img_obj,img)

    for tag in tags :
        tag_obj_qs = Tag.objects.filter(content = tag)
        if tag_obj_qs.exists() :
            img.tags.add(tag_obj_qs.first())
        else :
            return

    content_type = ContentType.objects.get_for_model(img.__class__)
    event = create_event('upload',initiator,content_type,img.id)
    return img


def create_comment(content,is_parent,content_type,object_id,initiator) :
    comment = Comment.objects.create(
        content = content,
        is_parent = is_parent,
        content_type = content_type,
        object_id = object_id
    )

    content_type = ContentType.objects.get_for_model(comment.__class__)
    event = create_event('comment',initiator,content_type,comment.id)
    return comment
