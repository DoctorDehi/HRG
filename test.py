from pigeon_app import add_otec, pigeon_app


with pigeon_app.app_context_processor:
    add_otec("1-AT514-20")