# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yediemin']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.8', 'django-storages>=1.11', 'djangorestframework>=3.0']

setup_kwargs = {
    'name': 'yediemin',
    'version': '0.1.7',
    'description': 'Bulletproof attachment serving for Django Rest Framework.',
    'long_description': '# Yediemin\n\nA package for bulletproof attachment serving in Django Rest Framework.\n\n## Getting Started\n\n### Requirements\n- Nginx\n- Django Rest Framework\n- Session Authentication\n- Django Storages (S3)\n\n### Installation Steps\n\n1) Install package from [PyPi](https://pypi.org/project/yediemin/).\n\n```sh\npip install yediemin\n```\n\n2) Add the view to `urls.py`\n\n```python\nfrom yediemin import YedieminView\n\nurlpatterns = [\n    re_path(r\'^yediemin/(?P<file_name>\\S+)/$\', YedieminView.as_view(), name=\'yediemin\'),\n]\n```\n\n3) Configure Nginx. Place the configuration below under your server.\n\n```\nlocation /yediemin-files/ {\n            internal;\n            resolver 8.8.8.8;\n            set $redirect_uri "$upstream_http_redirect_uri";\n\n            proxy_buffering off;\n            proxy_pass $redirect_uri;\n}\n```\n\n4) Use `YedieminFileField` in serializer for `FileField`.\n\n```python\nfrom yediemin import YedieminFileField\n\nclass AttachmentSerializer(serializers.ModelSerializer):\n    file = YedieminFileField()\n\n    class Meta:\n        model = Attachment\n        fields = (\n            "id",\n            "file",\n        )\n```\n\n5) Use `PrivateS3Boto3Storage` for the field in `models.py`\n\n```python\nfrom yediemin import PrivateS3Boto3Storage\n\nclass Attachment(models.Model):\n    file = models.FileField(storage=PrivateS3Boto3Storage())\n```\n\n6) Upload files to S3 with `YedieminFileField`. Yediemin requires [presigned object url](https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURL.html).\n\n### Settings\n\n- `YEDIEMIN_HIDDEN_REDIRECT_PATH`\n\nDefault: `yediemin-files`.\nIt should be same with location in nginx configuration.\n\n- `YEDIEMIN_AUTHENTICATION_CLASSES`\n\nDefault: `[rest_framework.authentication.SessionAuthentication]`\n\n- `YEDIEMIN_EXPIRE_IN`\n\nDefault: `604800` seconds which is 1 week. This is the maximum limit provided by AWS. [Using Query Parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html)',
    'author': 'Efe \xc3\x96ge',
    'author_email': 'efe@hipolabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hipo/yediemin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4',
}


setup(**setup_kwargs)
