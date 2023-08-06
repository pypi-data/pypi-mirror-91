#!/usr/bin/env python3
#
# Copyright (C) 2020 Guillaume Bernard <contact@guillaume-bernard.fr>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import abc
from datetime import datetime
from enum import Enum
from typing import Set, List

from newseyevent import newseye_languages
from wikivents.models import Event, ISO6391LanguageCode


class DocumentType(Enum):
    ARTICLE = "Article"
    ISSUE = "Issue"

    def __str__(self):
        return str(self.value)


class SolrQueryParser(Enum):
    """
    .. note:: In order to use OR and AND operators, LUCENE is required.
    """
    LUCENE = "lucene"
    DISMAX = "dismax"
    EDISMAX = "edismax"


class SolrDefaultField:
    """
    The default field that is used to search for data.
    """
    field_name = "df"

    def __init__(self, default_field: str, query_parser: SolrQueryParser = SolrQueryParser.LUCENE):
        """
        :param default_field: the default field name used for the q Solr parameter
        """
        self.default_field = default_field
        self.query_parser = query_parser

    def __str__(self):
        return f"defType={self.query_parser.value}&{self.field_name}={self.default_field}"


class SolrFilterQueryParameter:
    """
    This is a standard filter query parameter.
    """

    query_parameter = "fq"

    def __str__(self):
        return f"{self.query_parameter}="

    def __repr__(self):
        return str(self)


class SolrDateField(SolrFilterQueryParameter):
    """
    This is a the date field, which starts and end at the specified dates.
    """
    field_name = "date_created_ssi"

    def __init__(self, start_date: datetime, end_date: datetime):
        """
        :param start_date: the start date for the date field
        :param end_date: the end date for the date field
        """
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"{SolrFilterQueryParameter.__str__(self)}{self.field_name}:" \
               f"[{self.start_date.strftime('%Y-%m-%d')}%20TO%20{self.end_date.strftime('%Y-%m-%d')}]"


class SolrLanguageField(SolrFilterQueryParameter):
    """
    The language field to search for data.
    Languages given should be string representation of language using the ISO-639-1 representation.
    """
    field_name = "language_ssi"

    def __init__(self, language: str):
        self.language = language

    def __str__(self):
        return f"{SolrFilterQueryParameter.__str__(self)}{self.field_name}%3A{self.language}"


class SolrModelField(SolrFilterQueryParameter):
    """
    This is the model field, in order to indicate which type of document should be queried. Articles and Issues can
    be queried.
    """
    field_name = "has_model_ssim"

    def __init__(self, document_type: DocumentType):
        self.document_type = document_type

    def __str__(self):
        return f"{SolrFilterQueryParameter.__str__(self)}{self.field_name}%3A{self.document_type.value}"


class SolrSortField:
    class SortOrder(Enum):
        ASC = "asc"
        DESC = "desc"

    field_name = "sort"

    def __init__(self, sort_field: str, order: SortOrder.ASC):
        self.sort_field = sort_field
        self.order = order

    def __str__(self):
        return f"{self.field_name}={self.sort_field}%20{self.order.value}"


class SolrEntityQueryField:
    """
    This is a query field that includes entities and their alternative names.
    """

    def __init__(self, entity_representations: Set[str], entity_weight: int = 1):
        """
        :param entity_representations: the set of entity names to include in this query field.
        :param entity_weight: the importance of this entity for solr
        """
        self.entities = entity_representations
        self.boost = entity_weight

    def __str__(self):
        return "%20OR%20".join(
            [f"%22{entity}%22^{self.boost ** 2}" for entity in self.entities]
        ) if len(self.entities) > 0 else str()


class SolrQuery(abc.ABC):

    @property
    @abc.abstractmethod
    def processed_field_name(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass


class SolrQueryEventArticlesInLanguage(SolrQuery):

    @property
    def processed_field_name(self):
        return self._default_field_name

    def __init__(self, event: Event, iso_639_1_language_code: ISO6391LanguageCode = "en"):
        if iso_639_1_language_code not in newseye_languages:
            raise ValueError(f"Language {iso_639_1_language_code} is not supported in the NewsEye project. Please "
                             f"use one of the following languages: {newseye_languages}")
        self._event = event
        self._iso_639_1_language_code = iso_639_1_language_code
        self._document_type = DocumentType.ARTICLE
        self._default_field_name = f"all_text_t{iso_639_1_language_code}_siv"
        self._sort_field = "score"

    def render(self) -> str:
        return f"{self._get_base_filter_query_parameters_string()}&" \
               f"q={self._get_string_of_entities_and_types_queries()}"

    def _get_base_filter_query_parameters_string(self):
        return "&".join([
            str(SolrSortField(self._sort_field, SolrSortField.SortOrder.DESC)),
            str(SolrModelField(self._document_type)),
            str(SolrLanguageField(self._iso_639_1_language_code)),
            str(SolrDefaultField(self._default_field_name))
        ])

    def _get_string_of_entities_and_types_queries(self) -> str:
        return '%20OR%20'.join(
            str(query) for query in self._get_entities_queries()
            if len(str(query)) > 0
        )

    def _get_entities_queries(self) -> List[SolrEntityQueryField]:
        solr_entities_query_fields = []
        for participating_entity in self._event.gpe + self._event.per + self._event.org:
            solr_entities_query_fields.append(
                SolrEntityQueryField(
                    entity_representations=participating_entity.entity.names(self._iso_639_1_language_code),
                    entity_weight=participating_entity.count
                )
            )
        return solr_entities_query_fields

    def _get_type_queries(self) -> List[SolrEntityQueryField]:
        solr_entities_query_fields = []
        for event_type in self._event.types():
            solr_entities_query_fields.append(
                SolrEntityQueryField(
                    entity_representations=event_type.names(self._iso_639_1_language_code),
                    entity_weight=int((self._event.nb_of_processed_languages / 2) ** 2)
                )
            )
        return solr_entities_query_fields

    def _get_label_query(self):
        return f"{self._event.label.get(self._iso_639_1_language_code)}"


class SolrQueryEventArticlesInLanguageDateRange(SolrQueryEventArticlesInLanguage):

    def __init__(self, event: Event, iso_639_1_language_code: ISO6391LanguageCode,
                 begin_date: datetime, end_date: datetime):
        super().__init__(event, iso_639_1_language_code)
        self.begin_date = begin_date
        self.end_date = end_date

    def render(self) -> str:
        return f"{super().render()}&{SolrDateField(self.begin_date, self.end_date)}"


class SolrInstance:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port


class SolrCollection:

    def __init__(self, solr_instance: SolrInstance, collection_name: str):
        self.instance = solr_instance
        self.collection = collection_name
        self.request_handler = "select"

    def query(self, solr_query: SolrQueryEventArticlesInLanguage):
        return f"{self.__base_full_solr_query_for_this_endpoint(solr_query)}&q{solr_query.render()}"

    def __build_a_full_solr_query_for_this_endpoint_for_a_specific_date_range(
        self, solr_query: SolrQueryEventArticlesInLanguage
    ) -> str:
        return f"{self.__base_full_solr_query_for_this_endpoint(solr_query)}" \
               f"&q{solr_query.render()}"

    def __base_full_solr_query_for_this_endpoint(self, solr_query: SolrQueryEventArticlesInLanguage) -> str:
        return f"http://{self.instance.host}:{self.instance.port}/solr/" \
               f"{self.collection}/{self.request_handler}?fl=" \
               f"id,language_ssi,date_created_dtsi,member_of_collection_ids_ssi,from_issue_ssi," \
               f"linked_entities_ssim,linked_persons_ssim,score,{solr_query.processed_field_name}"
