# -*- coding: utf-8 -*-


def update_context_processor(sender, instance, created, **kwargs):
    """
    Update context processor so to introduced in the next refresh.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    print instance