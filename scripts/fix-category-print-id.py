#!/usr/bin/env python
# -*-coding:utf-8 -*

import logging
import click

from alkivi.logger import Logger
from alkivi.odoo import client as odoo

# Define the global logger
logger = Logger(min_log_level_to_mail=None,
                min_log_level_to_save=logging.DEBUG,
                min_log_level_to_print=logging.DEBUG)


@click.command()
@click.option('--endpoint', prompt='Odoo conf to use :', default='sqq-recette', help='Section of ~/.odoo.conf to use')
@click.option('--dry', prompt='Activate dry mode ?', default=False, is_flag=True, help='Do not commit shit')
def fix_category_print(endpoint, dry):
    """Fix Odoo BarCode."""
    odoo_client = odoo.Client(logger=logger, endpoint=endpoint)

    category_id = 1

    search_args = [('category_print_id', '=', None)]
    product_ids = odoo_client.search('product.product', search_args)
    if not product_ids:
        logger.info('No product at all')
        return

    logger.new_loop_logger()
    for product_id in product_ids:
        product = odoo_client.browse('product.product', product_id)
        logger.new_iteration(prefix='id={0} name={1}'.format(product_id,
                                                             product.name))
        category = product.category_print_id

        if category and category_id == category_id:
            logger.debug('Category already OK')
        else:
            logger.info('Going to update category_print_id')
            if dry:
                logger.debug('Not saving changes')
            else:
                product.category_print_id = category_id
    logger.del_loop_logger()


if __name__ == "__main__":
    fix_category_print()
