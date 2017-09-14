from flask_marshmallow.fields import URLFor
from marshmallow.fields import Float

from mass_server.core.models import ContactedBySampleRelation
from mass_server.core.models import DroppedBySampleRelation
from mass_server.core.models import ResolvedBySampleRelation
from mass_server.core.models import RetrievedBySampleRelation
from mass_server.core.models import Sample
from mass_server.core.models import SampleRelation
from mass_server.core.models import SsdeepSampleRelation
from .base import BaseSchema
from .base import ForeignReferenceField


class SampleRelationSchema(BaseSchema):
    url = URLFor('.sample_relation_detail', id='<id>', _external=True)
    sample = ForeignReferenceField(endpoint='.sample_detail', model_class=Sample, query_parameter='id')
    other = ForeignReferenceField(endpoint='.sample_detail', model_class=Sample, query_parameter='id')

    class Meta(BaseSchema.Meta):
        model = SampleRelation
        dump_only = [
                'id',
                '_cls'
                ]

class DroppedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = DroppedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only


class ResolvedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = ResolvedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only


class ContactedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = ContactedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only


class RetrievedBySampleRelationSchema(SampleRelationSchema):
    class Meta(BaseSchema.Meta):
        model = RetrievedBySampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only


class SsdeepSampleRelationSchema(SampleRelationSchema):
    match = Float()

    class Meta(BaseSchema.Meta):
        model = SsdeepSampleRelation
        dump_only = SampleRelationSchema.Meta.dump_only
