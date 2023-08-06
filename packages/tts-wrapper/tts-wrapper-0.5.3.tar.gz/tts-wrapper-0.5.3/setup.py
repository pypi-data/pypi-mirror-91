# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tts_wrapper']

package_data = \
{'': ['*']}

extras_require = \
{'google': ['google-cloud-texttospeech==2.2.0'],
 'microsoft': ['requests==2.22.0'],
 'polly': ['boto3==1.11.3'],
 'watson': ['ibm-watson==4.3.0']}

setup_kwargs = {
    'name': 'tts-wrapper',
    'version': '0.5.3',
    'description': 'A hassle-free Python library that allows one to use text-to-speech APIs with the same interface',
    'long_description': '# TTS-Wrapper\n\n![](https://github.com/mediatechlab/tts-wrapper/workflows/Python%20package/badge.svg)\n\n_TTS-Wrapper_ is a hassle-free Python library that allows one to use text-to-speech APIs with the same interface.\n\nCurrently the following services are supported:\n\n- AWS Polly\n- Google TTS\n- Microsoft TTS\n- IBM Watson\n\n## Installation\n\nInstall using pip.\n\n```sh\npip install TTS-Wrapper\n```\n\n**Note: for each service you want to use, you have to install the required packages.**\n\nExample: to use `google` and `watson`:\n\n```sh\npip install TTS-Wrapper[google, watson]\n```\n\n## Usage\n\nSimply instantiate an object from the desired service and call `synth()`.\n\n```Python\nfrom tts_wrapper import PollyTTS\n\ntts = PollyTTS()\ntts.synth(\'Hello, world!\', \'hello.wav\')\n```\n\n### Selecting a Voice\n\nYou can change the default voice by specifying the voice name and the language code:\n\n```Python\ntts = PollyTTS(voice_name=\'Camila\', lang=\'pt-BR\')\n```\n\nCheck out the list of available voices for [Polly](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html), [Google](https://cloud.google.com/text-to-speech/docs/voices), [Microsoft](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices), and [Watson](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices).\n\n### SSML\n\nYou can also use [SSML](https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language) markup to control the output, like so:\n\n```Python\ntts.synth(\'Hello, <break time="3s"/> world!\')\n```\n\n**You don\'t need to wrap it with the `<speak></speak>` tag as it is automatically used with the required parameters for each TTS service.**\n\nLearn which tags are available for each service: [Polly](https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html), [Google](https://cloud.google.com/text-to-speech/docs/ssml), [Microsoft](https://docs.microsoft.com/en-us/cortana/skills/speech-synthesis-markup-language), and [Watson](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-ssml).\n\n### Credentials\n\nYou need to setup credentials to access each service.\n\n#### Polly\n\nIf you don\'t explicitly define credentials, `boto3` will try to find them in your system\'s credentials file or your environment variables. However, you can specify them with:\n\n```Python\nfrom tts_wrapper import PollyTTS, AwsCredentials\n\ntts = PollyTTS(creds=AwsCredentials(\'AWS_KEY_ID\', \'AWS_ACCESS_KEY\'))\n```\n\n#### Google\n\nPoint to your [Oauth 2.0 credentials file](https://developers.google.com/identity/protocols/OAuth2) path:\n\n```Python\nfrom tts_wrapper import GoogleTTS\n\ntts = GoogleTTS(creds=\'path/to/creds.json\')\n```\n\n#### Microsoft\n\nJust provide your [subscription key](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#authentication), like so:\n\n```Python\nfrom tts_wrapper import MicrosoftTTS\n\ntts = MicrosoftTTS(creds=\'TOKEN\')\n```\n\nIf your region is not "useast", you must change it like so:\n\n```Python\ntts = MicrosoftTTS(creds=\'TOKEN\', region=\'brazilsouth\')\n```\n\n#### Watson\n\nPass your [API key and URL](https://cloud.ibm.com/apidocs/text-to-speech/text-to-speech#authentication) to the initializer:\n\n```Python\nfrom tts_wrapper import WatsonTTS\n\ntts = WatsonTTS(api_key=\'API_KEY\', api_url=\'API_URL\')\n```\n\n## License\n\nLicensed under the [MIT License](./LICENSE).\n',
    'author': 'Giulio Bottari',
    'author_email': 'giuliobottari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mediatechlab/tts-wrapper',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
