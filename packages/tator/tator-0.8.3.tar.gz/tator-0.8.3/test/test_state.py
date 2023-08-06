import datetime
import random
import uuid
import time

import tator
from ._common import assert_close_enough

def random_state(project, state_type, video_obj, post=False):
    attributes = {
        'test_bool': random.choice([False, True]),
        'test_int': random.randint(-1000, 1000),
        'test_float': random.uniform(-1000.0, 1000.0),
        'test_enum': random.choice(['a', 'b', 'c']),
        'test_string': str(uuid.uuid1()),
        'test_datetime': datetime.datetime.now().isoformat(),
        'test_geopos': [random.uniform(-180.0, 180.0), random.uniform(-90.0, 90.0)],
    }
    out = {
        'project': project,
        'type': state_type,
        'media_ids': [video_obj.id],
        'frame': random.randint(0, video_obj.num_frames - 1),
    }
    if post:
        out = {**out, **attributes}
    else:
        out['attributes'] = attributes
    return out

def test_state_crud(host, token, project, video_type, video, state_type):
    tator_api = tator.get_api(host, token)
    video_obj = tator_api.get_media(video)

    # These fields will not be checked for object equivalence after patch.
    exclude = ['project', 'type', 'media_ids', 'id', 'meta', 'user', 'frame']

    # Test bulk create.
    num_states = random.randint(2000, 10000)
    states = [
        random_state(project, state_type, video_obj, post=True)
        for _ in range(num_states)
    ]
    state_ids = []
    for response in tator.util.chunked_create(tator_api.create_state_list,
                                         project, state_spec=states):
        state_ids += response.id
    assert len(state_ids) == len(states)
    print(f"Created {len(state_ids)} states!")

    # Test single create.
    state = random_state(project, state_type, video_obj, post=True)
    response = tator_api.create_state_list(project, state_spec=[state])
    assert isinstance(response, tator.models.CreateListResponse)
    print(response.message)
    state_id = response.id[0]

    # Patch single state.
    patch = random_state(project, state_type, video_obj)
    response = tator_api.update_state(state_id, state_update=patch)
    assert isinstance(response, tator.models.MessageResponse)
    print(response.message)

    # Get single state.
    updated_state = tator_api.get_state(state_id)
    assert isinstance(updated_state, tator.models.State)
    assert_close_enough(patch, updated_state, exclude)

    # Get state by ID.
    state_by_id = tator_api.get_state_list_by_id(project, [state_id])[0]
    assert_close_enough(updated_state, state_by_id, exclude)
    
    # Delete single state.
    response = tator_api.delete_state(state_id)
    assert isinstance(response, tator.models.MessageResponse)
    print(response.message)

    # ES can be slow at indexing so wait for a bit.
    time.sleep(2)
    params = {'media_id': [video], 'type': state_type}
    assert(tator_api.get_state_count(project, **params) == len(states))

    # Bulk update state attributes.
    bulk_patch = random_state(project, state_type, video_obj)
    bulk_patch = {'attributes': bulk_patch['attributes']}
    response = tator_api.update_state_list(project, **params,
                                           attribute_bulk_update=bulk_patch)
    assert isinstance(response, tator.models.MessageResponse)
    print(response.message)

    # Verify all states have been updated.
    states = tator_api.get_state_list(project, **params)
    dataframe = tator.util.to_dataframe(states)
    assert(len(states)==len(dataframe))
    for state in states:
        assert_close_enough(bulk_patch, state, exclude)
    
    # Clone states to same media.
    version_mapping = {version.id: version.id for version in tator_api.get_version_list(project)}
    generator = tator.util.clone_state_list(tator_api, {**params, 'project': project},
                                            project, version_mapping, {video:video}, {},
                                            {state_type:state_type}, tator_api)
    for num_created, num_total, response, id_map in generator:
        print(f"Created {num_created} of {num_total} states...")
    print(f"Finished creating {num_created} states!")
    time.sleep(2)
    assert(tator_api.get_state_count(project, **params) == 2 * len(states))
    
    # Delete all states.
    response = tator_api.delete_state_list(project, **params)
    assert isinstance(response, tator.models.MessageResponse)
    time.sleep(2)

    # Verify all states are gone.
    states = tator_api.get_state_list(project, **params)
    assert states == []
