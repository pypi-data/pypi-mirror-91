"""
    DigiCloud InstanceTypes Service.
"""
from cliff.lister import Lister
from cliff.show import ShowOne

from ..utils import tabulate


class ListInstanceType(Lister):
    """List instance-types."""

    def take_action(self, parsed_args):
        uri = '/instance-types'
        data = self.app.session.get(uri)

        return tabulate(data)


class ShowInstanceType(ShowOne):
    """Show instance-type details."""

    def get_parser(self, prog_name):
        parser = super(ShowInstanceType, self).get_parser(prog_name)
        parser.add_argument(
            'instance_type',
            metavar='<instance type>',
            help='InstanceType name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = f'/instance-types/{parsed_args.instance_type}'
        data = self.app.session.get(uri)

        return tabulate(data)
