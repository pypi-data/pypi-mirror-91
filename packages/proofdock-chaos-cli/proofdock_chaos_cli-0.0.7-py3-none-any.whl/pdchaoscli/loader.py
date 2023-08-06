import json
import os

from chaoslib.exceptions import ChaosException
from logzero import logger

import pdchaoscli.api.attacks as attacks
import pdchaoscli.api.scenarios as scenarios
from pdchaoscli.api.session import client_session


def load_attack_or_scenario(settings, definition, from_file):
    """Load the attack or scenario safely."""
    attack = None

    if from_file:
        attack = _load_from_file(from_file)

    if definition:
        attack = _load_from_endpoint(definition, settings)

    return attack


def _load_from_file(from_file):
    """Parse JSON, if possible"""
    with open(from_file) as json_file:
        data = json.load(json_file)
        return data


def _load_from_endpoint(definition_id, settings):
    """Load from Proofdock Cloud, if possible"""
    result = None
    with client_session(verify_tls=False, settings=settings) as session:
        try:
            result = attacks.get_attack(definition_id, session)
        except Exception:
            logger.debug('No attack definition found.', exc_info=1)
            # fallback to scenario definition
            try:
                result = scenarios.get_definition(definition_id, session)
            except Exception:
                logger.debug('No scenario definition found.', exc_info=1)
                raise ChaosException('Unable to get the attack/scenario definition.')
    return result


def load_endpoint():
    return {
        'url': _get_variable_or_default('PROOFDOCK_API_URL', None),
        'token': _get_variable_or_default('PROOFDOCK_API_TOKEN', None)
    }


def _get_variable_or_default(var: str, default: str):
    if var in os.environ and os.environ[var]:
        return os.environ[var]
    else:
        return default
