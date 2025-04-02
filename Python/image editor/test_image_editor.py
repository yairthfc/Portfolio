from image_editor import *

def test_turn_channel_gray():
    assert turn_channel_gray([100,180,240]) == 163