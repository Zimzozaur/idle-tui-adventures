from idle_tui_adventures.config import IdleTuiConfig


def test_init_new_config(test_config, test_config_file_path):
    assert "database" in test_config.config.sections()
    assert "character.active" in test_config.config.sections()
    assert test_config_file_path.exists()

    assert test_config.active_character_id == 0
    assert not test_config.skip_screen
    assert test_config.show_damage


def test_IdleTuiConfig(test_config, test_config_file_path):
    test_config.active_character_id = 1
    test_config.skip_screen = True
    test_config.show_damage = False

    assert test_config.active_character_id == 1
    assert test_config.skip_screen
    assert not test_config.show_damage

    updated_cfg = IdleTuiConfig(config_path=test_config_file_path)
    assert updated_cfg.active_character_id == 1
    assert updated_cfg.skip_screen
    assert not updated_cfg.show_damage
