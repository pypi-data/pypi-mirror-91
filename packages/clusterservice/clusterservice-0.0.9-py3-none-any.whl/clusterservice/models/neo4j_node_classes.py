from neomodel import (
    FloatProperty,
    IntegerProperty,
    Relationship,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Sentiment(StructuredNode):
    sentiment = IntegerProperty(required=True)


class Comment(StructuredNode):
    uid = StringProperty(required=True)
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty(required=True)
    avg_sentiment = Relationship(Sentiment, 'HAS_AVG_SENTIMENT')


class Sentence(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty(required=True)
    comment = Relationship(Comment, 'DECOMPOSES')
    sentiment = Relationship(Sentiment, 'HAS_SENTIMENT')


class Question(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty(required=True)


class ClusterHead(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    similarity_score = FloatProperty(required=True)
    element_count = IntegerProperty()
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty(required=True)
    question = Relationship(Question, 'ANSWERS')


class ClusterElement(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty(required=True)
    sentences = Relationship(Sentence, 'DERIVES_FROM')
    cluster_head = Relationship(ClusterHead, 'DECOMPOSES')
