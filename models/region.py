from collections import defaultdict

from flask import url_for
from sqlalchemy import Column, func, String, Unicode
from sqlalchemy.sql.expression import and_, bindparam
from database import Base

from database import db_session
from models.person import Person
from models.election import Election
from models.candidacy import Candidacy

class Region(Base):
    __tablename__ = 'region'

    id = Column(String(16), primary_key=True)
    name = Column(Unicode(20), index=True, nullable=False)
    name_cn = Column(Unicode(20))
    name_en = Column(String(80))

    @property
    def officials_grouped_by_age(self):
        officials_ = db_session.query(Person.id, Candidacy.age)\
                     .filter(Candidacy.person_id == Person.id)\
                     .filter(Candidacy.district_id.any(self.id))\
                     .filter(Candidacy.is_elected == True)\
                     .group_by(Person.id, Candidacy.election_id)

        res = defaultdict(list)
        for person_id, age in officials_:
            res[age].append(person_id)
        return res


    @property
    def is_province(self):
        return len(self.id) == 2

    @property
    def is_municipality(self):
        return len(self.id) == 5

    @property
    def is_submunicipality(self):
        return len(self.id) == 7

    @property
    def candidates(self):
        return Person.query\
                     .join(Candidacy)\
                     .filter(Candidacy.person_id == Person.id)\
                     .filter(Candidacy.district_id.any(self.id))\
                     .group_by(Person.id)

    @property
    def residents(self):
        return Person.query\
                     .filter(Person.address_id.any(self.id))\
                     .group_by(Person.id)

    @property
    def fullname(self):
        l_ = list(self.parents) + [self]
        fullname = ' '.join(region.name for region in l_)
        return fullname

    @property
    def fullname_en(self):
        l_ = list(self.parents) + [self]
        fullname = ' '.join(region.name_en for region in l_)
        return fullname

    @property
    def parents(self):
        return Region.query\
                     .filter(and_(
                         bindparam('prefix', self.id).startswith(Region.id),
                         self.id != Region.id))\
                     .order_by(func.length(Region.id))

    @property
    def children(self):
        descendants = Region.query\
                            .filter(and_(
                                Region.id.startswith(self.id),
                                self.id != Region.id))\
                            .order_by(func.length(Region.id)).all()
        try:
            smallest_len = min(len(region.id) for region in descendants)
        except:
            smallest_len = 7
        return (child for child in descendants if len(child.id) == smallest_len)

    @property
    def url(self):
        return url_for('region', region_id=self.id)
