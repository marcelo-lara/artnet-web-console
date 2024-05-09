from libs.artNetNodeInstance import ArtNetNodeInstance
from libs.fixture import Channel
from libs.parCan import ParCan
from libs.head import Head

fixture_types = {
    'Head': Head,
    'ParCan': ParCan
}

def create_fixture(data):
    fixture_type = data.get('type')
    if fixture_type in fixture_types:
        return fixture_types[fixture_type](**data)
    else:
        raise ValueError(f"Unknown fixture type: {fixture_type}")