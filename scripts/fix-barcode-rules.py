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

    wanted_rule_id = 12  # Price Look Up Codes (PLU Codes)
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

        internal_reference = product.default_code
        barcode_base = product.barcode_base

        if internal_reference:
            if int(barcode_base) != int(internal_reference):
                logger.info('Going to update barcode_base from {0} to {1}'.format(barcode_base, internal_reference))
                if dry:
                    logger.debug('Not saving changes')
                else:
                    product.barcode_base = internal_reference

        barcode_rule_id = product.barcode_rule_id
        if barcode_rule_id and barcode_rule_id.id == wanted_rule_id:
            logger.debug('Already a rule id {0}'.format(barcode_rule_id.od))
        else:
            logger.debug('Going to fix barcode_rule_id to {0}'.format(wanted_rule_id))
            if dry:
                logger.debug('Not saving changes')
            else:
                product.barcode_rule_id = wanted_rule_id
    logger.del_loop_logger()


if __name__ == "__main__":
    fix_barcode()
