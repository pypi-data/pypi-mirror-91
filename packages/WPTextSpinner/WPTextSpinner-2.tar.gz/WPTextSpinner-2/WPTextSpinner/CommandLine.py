# -*- coding: UTF-8 -*-
import argparse

from WPTextSpinner import WPTextSpinner, PostService
from WPTextSpinner.Utils import Utils


def main():
    parser = argparse.ArgumentParser(description='Easily spin wordpress content!')
    parser.add_argument('--config', required=True, type=str, help='Path to the json-config-file')
    parser.add_argument('--template', required=True, type=str, help='Path to the template-file')
    parser.add_argument('--dry_run', action='store_true', help='Path to the template-file')

    args = parser.parse_args()

    Utils.set_config_data_path(args.config)
    template = Utils.read_file(args.template)

    post_service = PostService()
    posts = post_service.get_posts(post_service.post_type)

    spinner = WPTextSpinner()
    spinner.spin_posts(posts, template, dry=args.dry_run)


if __name__ == "__main__":
    main()