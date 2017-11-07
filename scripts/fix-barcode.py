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
def fix_barcode(endpoint, dry):
    """Fix Odoo BarCode."""
    odoo_client = odoo.Client(logger=logger, endpoint=endpoint)

    search_args = [('to_weight', '=', True)]
    product_ids = odoo_client.search('product.product', search_args)
    if not product_ids:
        logger.info('No product at all')
        return

    logger.new_loop_logger()
    for product_id in product_ids:
        product = odoo_client.browse('product.product', product_id)
        logger.new_iteration(prefix='id={0} name={1}'.format(product_id,
							     product.name))
        old_barcode = product.barcode

        if not old_barcode:
            logger.warning('No barcode for product')
            continue

        if old_barcode.startswith('02'):
            logger.info('Barecode {0} already OK'.format(old_barcode))
            continue

        new_barcode = '0{0}'.format(old_barcode)
        logger.info('Going to update barcode from {0} to {1}'.format(old_barcode, new_barcode))
        if dry:
            logger.debug('Not saving changes')
        else:
            product.barcode = new_barcode
    logger.del_loop_logger()




if __name__ == "__main__":
    fix_barcode()
