"""
Run with ENABLE_DEBUG_TOOLBAR unset
"""
import os
import pytest


toolbar_enabled = pytest.mark.skipif(
    os.getenv('ENABLE_DEBUG_TOOLBAR') != 'true',
    reason="debug toolbar disabled")

toolbar_disabled = pytest.mark.skipif(
    os.getenv('ENABLE_DEBUG_TOOLBAR') == 'true',
    reason="debug toolbar enabled")


@toolbar_disabled
def test_toolbar_app_absent(settings):
    assert 'debug_toolbar' not in settings.INSTALLED_APPS


@toolbar_disabled
def test_toolbar_middleware_absent(settings):
    assert 'debug_toolbar.middleware.DebugToolbarMiddleware' not in \
           settings.MIDDLEWARE_CLASSES


@toolbar_enabled
def test_toolbar_app_present(settings):
    assert 'debug_toolbar' in settings.INSTALLED_APPS


@toolbar_enabled
def test_toolbar_middleware_present(settings):
    assert 'debug_toolbar.middleware.DebugToolbarMiddleware' in \
           settings.MIDDLEWARE_CLASSES
