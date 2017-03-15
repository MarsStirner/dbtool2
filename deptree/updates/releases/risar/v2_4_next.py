# coding: utf-8
"""
Следующая разрабатываемая версия.
"""
from deptree.internals.base import DBToolBaseNode


class Risar_v2_4_next(DBToolBaseNode):
    name = None  # 'risar-v2.4.'
    depends = [
        'risar-v2.4.44',
        'rimis-2012',
        # risk scales
        'rimis-1885.regional_common', 'rimis-1885.new_factors_from_tomsk',
        'rimis-2157.new_factors_from_saratov',
        'rimis-2093'
        #
        'rimis-1885.diags_mkb_details_content', 'rimis-1885.diags_mkb_details',

    ]
